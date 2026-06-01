import numpy as np

CO2_PER_LITER = 2.68
CARBON_PRICE_RP_PER_TON = 336_000
DIESEL_PRICE_RP_PER_LITER = 12_900


def calc_co2(fuel_L):
    return fuel_L * CO2_PER_LITER / 1000


def calc_carbon_cost(co2_ton):
    return co2_ton * CARBON_PRICE_RP_PER_TON


def calc_total_cost(fuel_L, co2_ton=None):
    if co2_ton is None:
        co2_ton = calc_co2(fuel_L)
    return fuel_L * DIESEL_PRICE_RP_PER_LITER + calc_carbon_cost(co2_ton)


def esg_report(segments_df, fleet_key="HD785_7", trips_per_year=6000,
               diesel_price=None, carbon_price=None):
    from src.fuel_optimizer.engine import calc_round_trip
    from src.utils.fleet_db import get_truck

    dp = diesel_price if diesel_price is not None else DIESEL_PRICE_RP_PER_LITER
    cp = carbon_price if carbon_price is not None else CARBON_PRICE_RP_PER_TON

    truck = get_truck(fleet_key)
    if "grade_pct" not in segments_df.columns:
        raise ValueError("segments_df must have 'grade_pct' column — run process_road() first")

    df = segments_df.dropna(subset=["grade_pct"]).copy()

    fuel_current = 0.0
    fuel_ideal = 0.0
    for _, row in df.iterrows():
        g = row["grade_pct"]
        r = calc_round_trip(truck, grade_pct=g, distance_m=20)
        r_ideal = calc_round_trip(truck, grade_pct=min(g, 8), distance_m=20)
        fuel_current += r["fuel_round_L"]
        fuel_ideal += r_ideal["fuel_round_L"]

    fuel_waste_per_trip = max(0, fuel_current - fuel_ideal)
    fuel_waste_year = fuel_waste_per_trip * trips_per_year

    co2_actual = calc_co2(fuel_current * trips_per_year)
    co2_ideal = calc_co2(fuel_ideal * trips_per_year)
    co2_reduction = max(0, co2_actual - co2_ideal)

    high_grade = int((df["grade_pct"] > 10).sum())
    moderate_grade = int(((df["grade_pct"] > 8) & (df["grade_pct"] <= 10)).sum())

    return {
        "fleet": fleet_key,
        "road_length_m": float(df["chainage"].max()),
        "segments_total": len(df),
        "segments_high_grade": high_grade,
        "segments_moderate_grade": moderate_grade,
        "max_grade_pct": float(df["grade_pct"].max()),
        "mean_grade_pct": float(df["grade_pct"].mean()),
        "fuel_per_trip_L": round(fuel_current, 2),
        "fuel_ideal_per_trip_L": round(fuel_ideal, 2),
        "fuel_waste_per_trip_L": round(fuel_waste_per_trip, 2),
        "fuel_waste_per_year_L": round(fuel_waste_year, 0),
        "trips_per_year": trips_per_year,
        "co2_actual_ton_per_year": round(co2_actual, 0),
        "co2_ideal_ton_per_year": round(co2_ideal, 0),
        "co2_reduction_ton_per_year": round(co2_reduction, 0),
        "fuel_cost_waste_Rp_per_year": round(fuel_waste_year * dp, 0),
        "carbon_credit_value_Rp_per_year": round(co2_reduction * cp, 0),
        "total_saving_Rp_per_year": round(fuel_waste_year * dp + co2_reduction * cp, 0),
    }
