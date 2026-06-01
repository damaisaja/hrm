"""
Fuel consumption calculation engine based on published research.

Key references:
  [1] Hasan & Octariando (2022). "The Effect of Road Grade on Dump Truck
      Fuel Consumption." SAE Technical Paper 2022-01-5030.
      DOI: 10.4271/2022-01-5030

  [2] Saptarini et al. (2024). "Effect of Transport Road Slope on Fuel
      Consumption of Coal Mine Transport Truck." E3S Web of Conferences.

  [3] Soofastaei et al. "Rolling Resistance in Haul Truck Operations."
      Mining3, University of Queensland.

  [4] Caterpillar Performance Handbook, Edition 29.
  [5] Komatsu Performance Handbook.
"""

import numpy as np
from src.utils.fleet_db import DumpTruck, FLEET_DB

GRAVITY = 9.81  # m/s²
DIESEL_ENERGY = 38.6  # MJ/L — energy content of diesel
ROLLING_RESISTANCE_COEFF_DEFAULT = 0.025  # typical mine haul road
ENGINE_EFFICIENCY = 0.35  # typical diesel engine efficiency


def _grade_to_radians(grade_pct: float) -> float:
    return np.arctan(grade_pct / 100.0)


def calc_tractive_force(
    gvw_kg: float,
    grade_pct: float,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF_DEFAULT,
) -> float:
    """
    Total tractive force required (N).

    F_total = (RR × cosθ + sinθ) × m × g

    [4] Caterpillar Performance Handbook.
    """
    theta = _grade_to_radians(grade_pct)
    rr_force = rolling_resistance * np.cos(theta) * gvw_kg * GRAVITY
    grade_force = np.sin(theta) * gvw_kg * GRAVITY
    return rr_force + grade_force


def calc_power_required(
    gvw_kg: float,
    grade_pct: float,
    speed_ms: float,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF_DEFAULT,
) -> float:
    """
    Power required at wheels (kW).

    P = F_total × v

    [4] Caterpillar Performance Handbook, Section 9 (Construction & Mining Trucks).
    """
    force = calc_tractive_force(gvw_kg, grade_pct, rolling_resistance)
    return force * speed_ms / 1000.0


def calc_fuel_consumption_rate(
    power_at_wheels_kw: float,
    engine_efficiency: float = ENGINE_EFFICIENCY,
    diesel_energy_mj_per_l: float = DIESEL_ENERGY,
) -> float:
    """
    Fuel consumption rate (L/s) based on engine power demand.

    Fuel rate = P / (η × E_diesel)

    [4] Caterpillar Performance Handbook — owning & operating costs.
    """
    return power_at_wheels_kw / (engine_efficiency * diesel_energy_mj_per_l * 1000.0)


def calc_fuel_per_trip(
    truck: DumpTruck,
    grade_pct: float,
    distance_m: float,
    speed_ms: float = 8.0,
    payload_tonnes: float | None = None,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF_DEFAULT,
) -> dict:
    """
    Hitung konsumsi bahan bakar per trip berdasarkan grade dan jarak.

    Parameters
    ----------
    truck : DumpTruck — spesifikasi dump truck
    grade_pct : float — kemiringan jalan dalam persen (contoh: 10 berarti 10%)
    distance_m : float — jarak tempuh dalam meter
    speed_ms : float — kecepatan rata-rata (default 8 m/s ≈ 29 km/jam)
    payload_tonnes : float | None — muatan aktual (default = rated payload)
    rolling_resistance : float — koefisien rolling resistance (default 0.025)

    Returns
    -------
    dict dengan rincian:
        - fuel_L: total konsumsi (liter)
        - fuel_per_km: konsumsi per km (L/km)
        - fuel_per_hour: konsumsi per jam (L/hr)
        - power_kw: daya yang dibutuhkan (kW)
        - power_pct: persentase daya terhadap rated engine
        - grade_force_N: gaya akibat grade (N)
        - rr_force_N: gaya rolling resistance (N)
        - cycle_time_s: waktu tempuh (detik)
    """
    if payload_tonnes is None:
        payload_tonnes = truck.payload_tonnes

    gvw_kg = (truck.empty_weight_tonnes + payload_tonnes) * 1000.0
    cycle_time_s = distance_m / speed_ms

    theta = _grade_to_radians(grade_pct)
    rr_force = rolling_resistance * np.cos(theta) * gvw_kg * GRAVITY
    grade_force = np.sin(theta) * gvw_kg * GRAVITY
    total_force = rr_force + grade_force

    power_kw = total_force * speed_ms / 1000.0
    power_pct = (power_kw / truck.engine_power_kw) * 100.0

    fuel_rate_L_per_s = calc_fuel_consumption_rate(power_kw)
    fuel_L = fuel_rate_L_per_s * cycle_time_s
    fuel_per_hour = fuel_L / (cycle_time_s / 3600.0) if cycle_time_s > 0 else 0
    fuel_per_km = fuel_L / (distance_m / 1000.0) if distance_m > 0 else 0

    return {
        "fuel_L": round(fuel_L, 2),
        "fuel_per_km": round(fuel_per_km, 2),
        "fuel_per_hour": round(fuel_per_hour, 2),
        "power_kw": round(power_kw, 1),
        "power_pct": round(power_pct, 1),
        "grade_force_N": round(grade_force, 0),
        "rr_force_N": round(rr_force, 0),
        "cycle_time_s": round(cycle_time_s, 0),
    }


def calc_round_trip(
    truck: DumpTruck,
    grade_pct: float,
    distance_m: float,
    speed_ms: float = 8.0,
    rolling_resistance: float = ROLLING_RESISTANCE_COEFF_DEFAULT,
) -> dict:
    r_laden = calc_fuel_per_trip(truck, grade_pct, distance_m, speed_ms,
                                  payload_tonnes=truck.payload_tonnes,
                                  rolling_resistance=rolling_resistance)
    r_empty = calc_fuel_per_trip(truck, -grade_pct, distance_m, speed_ms,
                                  payload_tonnes=0,
                                  rolling_resistance=rolling_resistance)
    fuel_round = r_laden["fuel_L"] + r_empty["fuel_L"]
    return {
        "fuel_laden_L": r_laden["fuel_L"],
        "fuel_empty_L": r_empty["fuel_L"],
        "fuel_round_L": round(fuel_round, 2),
        "fuel_round_per_km": round(fuel_round / (distance_m / 1000), 2),
        "power_laden_kw": r_laden["power_kw"],
        "power_empty_kw": r_empty["power_kw"],
        "power_laden_pct": r_laden["power_pct"],
        "power_empty_pct": r_empty["power_pct"],
        "cycle_time_s": r_laden["cycle_time_s"] + r_empty["cycle_time_s"],
    }


def calc_fuel_saving(
    truck_key: str,
    current_grade: float,
    target_grade: float,
    distance_m: float,
    trips_per_year: int,
    speed_ms: float = 8.0,
) -> dict:
    """
    Hitung potensi penghematan bahan bakar jika grade diperbaiki.

    Parameters
    ----------
    truck_key : str — kunci model di FLEET_DB (contoh: "HD785_7")
    current_grade : float — grade eksisting (%)
    target_grade : float — grade target setelah perbaikan (%)
    distance_m : float — panjang segmen jalan (m)
    trips_per_year : int — jumlah trip per tahun
    speed_ms : float — kecepatan rata-rata (m/s)

    Returns
    -------
    dict dengan rincian penghematan
    """
    truck = FLEET_DB[truck_key]

    current = calc_fuel_per_trip(truck, current_grade, distance_m, speed_ms)
    target = calc_fuel_per_trip(truck, target_grade, distance_m, speed_ms)

    fuel_saved_per_trip = current["fuel_L"] - target["fuel_L"]
    fuel_saved_per_year = fuel_saved_per_trip * trips_per_year

    co2_factor = 2.68  # kg CO2 per liter diesel [3]
    fuel_price_rp = 12000  # IDR per liter solar
    carbon_price_rp = 336000  # IDR per ton CO2

    co2_reduction_kg = fuel_saved_per_year * co2_factor
    co2_reduction_ton = co2_reduction_kg / 1000.0
    fuel_cost_saving_rp = fuel_saved_per_year * fuel_price_rp
    carbon_cost_saving_rp = co2_reduction_ton * carbon_price_rp

    return {
        "truck": truck_key,
        "segment_length_m": distance_m,
        "current_grade_pct": current_grade,
        "target_grade_pct": target_grade,
        "fuel_current_L_per_trip": current["fuel_L"],
        "fuel_target_L_per_trip": target["fuel_L"],
        "fuel_saved_L_per_trip": round(fuel_saved_per_trip, 2),
        "fuel_saved_L_per_year": round(fuel_saved_per_year, 0),
        "fuel_cost_saving_Rp_per_year": round(fuel_cost_saving_rp, 0),
        "co2_reduction_kg_per_year": round(co2_reduction_kg, 0),
        "co2_reduction_ton_per_year": round(co2_reduction_ton, 2),
        "carbon_cost_saving_Rp_per_year": round(carbon_cost_saving_rp, 0),
        "total_saving_Rp_per_year": round(
            fuel_cost_saving_rp + carbon_cost_saving_rp, 0
        ),
    }


def grade_impact_factor(
    truck_key: str,
    base_grade: float = 0.0,
    grade_step: float = 1.0,
    max_grade: float = 15.0,
) -> dict:
    """
    Hitung faktor dampak grade terhadap konsumsi bahan bakar.

    Menggunakan metodologi [1] Hasan & Octariando (2022):
      - CAT 773D: setiap 1% grade → +21.95% fuel (laden)
      - HD465-7: setiap 1% grade → +23.64% fuel (laden)
      - Volvo A40E: setiap 1% grade → +13.29% fuel (laden)

    Returns
    -------
    dict mapping grade -> fuel consumption multiplier
    """
    impact_factors = {
        "CAT_773D": 0.2195,
        "HD465_7": 0.2364,
        "A40E": 0.1329,
    }
    factor = impact_factors.get(truck_key, 0.20)
    grades = np.arange(base_grade, max_grade + grade_step, grade_step)
    result = {}
    for g in grades:
        result[round(g, 1)] = round(1.0 + factor * g, 3)
    return result
