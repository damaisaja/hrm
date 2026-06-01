"""Test 10-40 ton dump trucks in the fleet database."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.fleet_db import list_fleet, get_truck
from src.fuel_optimizer.engine import calc_fuel_per_trip

print("=" * 80)
print(f"{'DUMP TRUCK 10-40 TON — FLEET DATABASE':^80}")
print("=" * 80)

# List all 10-40 ton models
small_models = [k for k in list_fleet() if k.startswith(("VOLVO_", "CAT_7", "HM3", "HM4", "HD3", "HD4", "DA30", "BELL"))]
print(f"\n{'Model':<20} {'Payload(t)':<12} {'Power(kW)':<12} {'Fuel(L/hr)':<14} {'GVW(t)':<10}")
print("-" * 68)
for key in small_models:
    t = get_truck(key)
    print(f"{key:<20} {t.payload_tonnes:<12.1f} {t.engine_power_kw:<12.0f} {t.fuel_consumption_L_per_hr_min}-{t.fuel_consumption_L_per_hr_max:<8.0f} {t.gvw_tonnes:<10.1f}")

# Test fuel calculation at grade 10%, 1 km
print(f"\n{'=' * 80}")
print(f"{'FUEL CALCULATION @ GRADE 10%, DISTANCE 1 KM — LADEN':^80}")
print(f"{'=' * 80}")
print(f"\n{'Model':<20} {'Grade%':<10} {'Fuel(L/trip)':<15} {'Fuel(L/km)':<12} {'Power(kW)':<12} {'Power%':<10}")
print("-" * 79)
for key in small_models:
    t = get_truck(key)
    r = calc_fuel_per_trip(t, grade_pct=10, distance_m=1000)
    print(f"{key:<20} 10{'%':<8} {r['fuel_L']:<15.2f} {r['fuel_per_km']:<12.2f} {r['power_kw']:<12.1f} {r['power_pct']:<10.1f}")
