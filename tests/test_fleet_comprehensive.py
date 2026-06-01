import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.fleet_db import list_fleet, get_truck
from src.fuel_optimizer.engine import calc_fuel_saving

# All 10-40 ton models
small_fleet = [
    "VOLVO_A25G", "VOLVO_A30G", "VOLVO_A35G", "VOLVO_A40G",
    "CAT_725", "CAT_730", "CAT_735", "CAT_740",
    "HM300_5", "HM400_5", "HD325_8", "HD405_8",
    "DA30_5", "BELL_B40E", "P460",
]

print(f"{'10-40 TON FLEET — SAVING SCENARIOS':^72}")
print(f"{'Grade 12% -> 8%, 1.5 km, 6000 trips/year':^72}")
print()
print(f"{'Model':<18} {'Payload':<10} {'Saving L/yr':<15} {'Cost Saving (Rp)':<20}")
print("-" * 63)
for key in small_fleet:
    t = get_truck(key)
    r = calc_fuel_saving(key, current_grade=12, target_grade=8,
                          distance_m=1500, trips_per_year=6000)
    print(f"{key:<18} {t.payload_tonnes:<10.1f} {r['fuel_saved_L_per_year']:<15,.0f} {r['total_saving_Rp_per_year']:<20,.0f}")
