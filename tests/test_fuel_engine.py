from src.fuel_optimizer.engine import calc_fuel_saving

scenarios = [
    ("HD785_7", 14, 8, 1500, 5000),
    ("HD785_7", 12, 8, 2000, 5000),
    ("CAT_773G", 13, 8, 1200, 6000),
    ("HD465_7", 11, 8, 1800, 5500),
    ("P460", 10, 6, 1000, 8000),
]

print(f"{'Truck':<15} {'Grade':<12} {'Saving L/yr':<15} {'Cost Saving Rp/yr':<22} {'CO2 ton/yr':<12}")
print("-" * 76)
for truck, curr, tgt, dist, trips in scenarios:
    r = calc_fuel_saving(truck, curr, tgt, dist, trips)
    print(
        f"{r['truck']:<15} {curr}%->{tgt}%    "
        f"{r['fuel_saved_L_per_year']:<15,.0f} "
        f"{r['total_saving_Rp_per_year']:<22,.0f} "
        f"{r['co2_reduction_ton_per_year']:<12,.1f}"
    )
