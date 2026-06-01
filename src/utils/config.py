from pydantic import BaseModel
from typing import Optional


class FleetSpec(BaseModel):
    name: str
    empty_weight_kg: float
    payload_kg: float
    engine_power_kw: float
    fuel_consumption_L_per_hour: float


class ProcessingConfig(BaseModel):
    voxel_size: float = 0.5
    ground_classification: int = 2
    max_slope_pct: float = 15.0


FLEET_DB = {
    "CAT_777": FleetSpec(
        name="CAT 777",
        empty_weight_kg=62000,
        payload_kg=90000,
        engine_power_kw=634,
        fuel_consumption_L_per_hour=45.0,
    ),
    "HD785": FleetSpec(
        name="HD785",
        empty_weight_kg=63000,
        payload_kg=91000,
        engine_power_kw=649,
        fuel_consumption_L_per_hour=46.5,
    ),
    "EH3500": FleetSpec(
        name="EH3500",
        empty_weight_kg=68000,
        payload_kg=100000,
        engine_power_kw=700,
        fuel_consumption_L_per_hour=48.0,
    ),
}

CO2_FACTOR = 2.68  # kg CO2 per liter diesel
FUEL_PRICE_RP = 12000  # Rp per liter solar
CARBON_PRICE_RP = 336000  # Rp per ton CO2 (estimasi)
