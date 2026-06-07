from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class IoTReading:
    sensor_id: str
    farm_id: str
    farm_name: str
    timestamp: str
    tank_temperature_c: float
    milk_volume_liters: float
    tank_capacity_liters: float
    ambient_temperature_c: float
    humidity_percent: float
    thi: float
    milk_quality_risk: str
    thermal_stress_risk: str
    collection_priority: str
    gps_lat: float
    gps_lng: float
    reading_source: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class IoTAlert:
    id: str
    farm_id: str
    severity: str
    message: str
    created_at: str
    recommended_action: str
    source: str

    def to_dict(self) -> dict:
        return asdict(self)
