from pydantic import BaseModel


class DumpTruck(BaseModel):
    model: str
    manufacturer: str
    engine_power_kw: float
    engine_power_hp: float
    payload_tonnes: float
    gvw_tonnes: float
    empty_weight_tonnes: float
    fuel_consumption_L_per_hr_min: float
    fuel_consumption_L_per_hr_max: float
    fuel_tank_L: int
    top_speed_kmh: float


FLEET_DB: dict[str, DumpTruck] = {
    "CAT_773D": DumpTruck(
        model="773D", manufacturer="Caterpillar",
        engine_power_kw=485, engine_power_hp=650,
        payload_tonnes=43.7, gvw_tonnes=99.3,
        empty_weight_tonnes=39.5,
        fuel_consumption_L_per_hr_min=38, fuel_consumption_L_per_hr_max=48,
        fuel_tank_L=700, top_speed_kmh=66,
    ),
    "CAT_773E": DumpTruck(
        model="773E", manufacturer="Caterpillar",
        engine_power_kw=500, engine_power_hp=671,
        payload_tonnes=50.0, gvw_tonnes=104.3,
        empty_weight_tonnes=43.0,
        fuel_consumption_L_per_hr_min=38, fuel_consumption_L_per_hr_max=48,
        fuel_tank_L=700, top_speed_kmh=66,
    ),
    "CAT_773G": DumpTruck(
        model="773G", manufacturer="Caterpillar",
        engine_power_kw=615, engine_power_hp=825,
        payload_tonnes=56.0, gvw_tonnes=102.7,
        empty_weight_tonnes=46.0,
        fuel_consumption_L_per_hr_min=32, fuel_consumption_L_per_hr_max=42,
        fuel_tank_L=700, top_speed_kmh=68,
    ),
    "HD465_7": DumpTruck(
        model="HD465-7", manufacturer="Komatsu",
        engine_power_kw=551, engine_power_hp=739,
        payload_tonnes=55.0, gvw_tonnes=99.7,
        empty_weight_tonnes=43.1,
        fuel_consumption_L_per_hr_min=35, fuel_consumption_L_per_hr_max=48,
        fuel_tank_L=780, top_speed_kmh=70,
    ),
    "HD785_7": DumpTruck(
        model="HD785-7", manufacturer="Komatsu",
        engine_power_kw=895, engine_power_hp=1200,
        payload_tonnes=91.7, gvw_tonnes=163.8,
        empty_weight_tonnes=72.0,
        fuel_consumption_L_per_hr_min=55, fuel_consumption_L_per_hr_max=75,
        fuel_tank_L=1308, top_speed_kmh=65,
    ),
    "EH3500": DumpTruck(
        model="EH3500AC-3", manufacturer="Hitachi",
        engine_power_kw=1491, engine_power_hp=2000,
        payload_tonnes=181.0, gvw_tonnes=322.0,
        empty_weight_tonnes=141.0,
        fuel_consumption_L_per_hr_min=120, fuel_consumption_L_per_hr_max=160,
        fuel_tank_L=2839, top_speed_kmh=56,
    ),
    "A40E": DumpTruck(
        model="A40E", manufacturer="Volvo",
        engine_power_kw=350, engine_power_hp=469,
        payload_tonnes=39.0, gvw_tonnes=69.2,
        empty_weight_tonnes=30.2,
        fuel_consumption_L_per_hr_min=22, fuel_consumption_L_per_hr_max=32,
        fuel_tank_L=545, top_speed_kmh=57,
    ),
    "T282B": DumpTruck(
        model="T282B", manufacturer="Liebherr",
        engine_power_kw=2720, engine_power_hp=3650,
        payload_tonnes=363.0, gvw_tonnes=592.0,
        empty_weight_tonnes=237.0,
        fuel_consumption_L_per_hr_min=200, fuel_consumption_L_per_hr_max=280,
        fuel_tank_L=3800, top_speed_kmh=64,
    ),
    "P460": DumpTruck(
        model="P460 B8X4 HT", manufacturer="Scania",
        engine_power_kw=338, engine_power_hp=460,
        payload_tonnes=35.0, gvw_tonnes=60.0,
        empty_weight_tonnes=25.0,
        fuel_consumption_L_per_hr_min=15, fuel_consumption_L_per_hr_max=25,
        fuel_tank_L=450, top_speed_kmh=70,
    ),
    # === 10-40 TON DUMP TRUCKS ===
    "VOLVO_A25G": DumpTruck(
        model="A25G", manufacturer="Volvo",
        engine_power_kw=237, engine_power_hp=318,
        payload_tonnes=25.0, gvw_tonnes=47.7,
        empty_weight_tonnes=22.7,
        fuel_consumption_L_per_hr_min=14, fuel_consumption_L_per_hr_max=19,
        fuel_tank_L=400, top_speed_kmh=53,
    ),
    "VOLVO_A30G": DumpTruck(
        model="A30G", manufacturer="Volvo",
        engine_power_kw=265, engine_power_hp=355,
        payload_tonnes=28.0, gvw_tonnes=52.0,
        empty_weight_tonnes=24.0,
        fuel_consumption_L_per_hr_min=15, fuel_consumption_L_per_hr_max=20,
        fuel_tank_L=480, top_speed_kmh=55,
    ),
    "VOLVO_A35G": DumpTruck(
        model="A35G", manufacturer="Volvo",
        engine_power_kw=336, engine_power_hp=451,
        payload_tonnes=33.5, gvw_tonnes=62.7,
        empty_weight_tonnes=29.2,
        fuel_consumption_L_per_hr_min=22, fuel_consumption_L_per_hr_max=30,
        fuel_tank_L=480, top_speed_kmh=57,
    ),
    "VOLVO_A40G": DumpTruck(
        model="A40G", manufacturer="Volvo",
        engine_power_kw=336, engine_power_hp=451,
        payload_tonnes=39.0, gvw_tonnes=69.7,
        empty_weight_tonnes=30.7,
        fuel_consumption_L_per_hr_min=24, fuel_consumption_L_per_hr_max=32,
        fuel_tank_L=480, top_speed_kmh=57,
    ),
    "CAT_725": DumpTruck(
        model="725", manufacturer="Caterpillar",
        engine_power_kw=257, engine_power_hp=345,
        payload_tonnes=24.0, gvw_tonnes=46.7,
        empty_weight_tonnes=22.7,
        fuel_consumption_L_per_hr_min=14, fuel_consumption_L_per_hr_max=20,
        fuel_tank_L=380, top_speed_kmh=55,
    ),
    "CAT_730": DumpTruck(
        model="730", manufacturer="Caterpillar",
        engine_power_kw=242, engine_power_hp=325,
        payload_tonnes=28.0, gvw_tonnes=50.9,
        empty_weight_tonnes=22.9,
        fuel_consumption_L_per_hr_min=16, fuel_consumption_L_per_hr_max=22,
        fuel_tank_L=380, top_speed_kmh=55,
    ),
    "CAT_735": DumpTruck(
        model="735", manufacturer="Caterpillar",
        engine_power_kw=316, engine_power_hp=424,
        payload_tonnes=32.0, gvw_tonnes=61.8,
        empty_weight_tonnes=29.8,
        fuel_consumption_L_per_hr_min=20, fuel_consumption_L_per_hr_max=28,
        fuel_tank_L=440, top_speed_kmh=55,
    ),
    "CAT_740": DumpTruck(
        model="740", manufacturer="Caterpillar",
        engine_power_kw=336, engine_power_hp=451,
        payload_tonnes=39.5, gvw_tonnes=71.9,
        empty_weight_tonnes=32.4,
        fuel_consumption_L_per_hr_min=24, fuel_consumption_L_per_hr_max=34,
        fuel_tank_L=480, top_speed_kmh=57,
    ),
    "HM300_5": DumpTruck(
        model="HM300-5", manufacturer="Komatsu",
        engine_power_kw=248, engine_power_hp=332,
        payload_tonnes=28.0, gvw_tonnes=53.4,
        empty_weight_tonnes=25.4,
        fuel_consumption_L_per_hr_min=16, fuel_consumption_L_per_hr_max=24,
        fuel_tank_L=450, top_speed_kmh=56,
    ),
    "HM400_5": DumpTruck(
        model="HM400-5", manufacturer="Komatsu",
        engine_power_kw=353, engine_power_hp=473,
        payload_tonnes=40.0, gvw_tonnes=75.1,
        empty_weight_tonnes=35.1,
        fuel_consumption_L_per_hr_min=22, fuel_consumption_L_per_hr_max=30,
        fuel_tank_L=520, top_speed_kmh=56,
    ),
    "HD325_8": DumpTruck(
        model="HD325-8", manufacturer="Komatsu",
        engine_power_kw=383, engine_power_hp=514,
        payload_tonnes=36.5, gvw_tonnes=66.5,
        empty_weight_tonnes=30.0,
        fuel_consumption_L_per_hr_min=22, fuel_consumption_L_per_hr_max=30,
        fuel_tank_L=500, top_speed_kmh=65,
    ),
    "HD405_8": DumpTruck(
        model="HD405-8", manufacturer="Komatsu",
        engine_power_kw=383, engine_power_hp=514,
        payload_tonnes=40.0, gvw_tonnes=72.0,
        empty_weight_tonnes=32.0,
        fuel_consumption_L_per_hr_min=24, fuel_consumption_L_per_hr_max=32,
        fuel_tank_L=500, top_speed_kmh=65,
    ),
    "DA30_5": DumpTruck(
        model="DA30-5", manufacturer="Doosan",
        engine_power_kw=276, engine_power_hp=370,
        payload_tonnes=28.0, gvw_tonnes=52.0,
        empty_weight_tonnes=24.0,
        fuel_consumption_L_per_hr_min=16, fuel_consumption_L_per_hr_max=22,
        fuel_tank_L=335, top_speed_kmh=55,
    ),
    "BELL_B40E": DumpTruck(
        model="B40E", manufacturer="Bell",
        engine_power_kw=320, engine_power_hp=429,
        payload_tonnes=36.5, gvw_tonnes=63.2,
        empty_weight_tonnes=26.7,
        fuel_consumption_L_per_hr_min=20, fuel_consumption_L_per_hr_max=28,
        fuel_tank_L=450, top_speed_kmh=55,
    ),
}


def list_fleet() -> list[str]:
    return list(FLEET_DB.keys())


def get_truck(model_key: str) -> DumpTruck:
    if model_key not in FLEET_DB:
        raise KeyError(f"Fleet model '{model_key}' not found. Available: {list_fleet()}")
    return FLEET_DB[model_key]
