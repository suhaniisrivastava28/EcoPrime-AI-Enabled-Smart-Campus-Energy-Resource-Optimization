"""
EcoPrime AI Engine: Occupancy Forecasting, Hydraulic Anomaly Detection, & ESG Calculations
Greater Noida Institute of Technology (GNIOT)
"""

import math
import random
from typing import Tuple, Dict, Any

class CampusOccupancyPredictor:
    """
    Predictive model fusing timetable metadata and PIR motion sensor feeds
    to forecast 30-minute room occupancy probabilities.
    """
    def __init__(self):
        # Baseline model priors calibrated for GNIOT academic schedule
        self.academic_blocks = {
            "room-101": {"base_capacity": 80, "weight_timetable": 0.65, "weight_pir": 0.35},
            "room-102": {"base_capacity": 40, "weight_timetable": 0.70, "weight_pir": 0.30},
            "room-204": {"base_capacity": 60, "weight_timetable": 0.60, "weight_pir": 0.40},
            "room-301": {"base_capacity": 250, "weight_timetable": 0.80, "weight_pir": 0.20},
        }

    def predict_occupancy_percentage(
        self,
        room_id: str,
        timetable_active: bool,
        hour: int,
        pir_count: int
    ) -> int:
        """
        Calculates occupancy likelihood in percentage (0-100%).
        """
        config = self.academic_blocks.get(room_id, {"base_capacity": 50, "weight_timetable": 0.6, "weight_pir": 0.4})
        
        # Factor 1: Timetable expectation
        timetable_score = 0.85 if timetable_active else 0.05
        
        # Factor 2: Temporal diurnal curve (bell curve peaking at 11 AM - 3 PM)
        time_factor = math.exp(-0.5 * ((hour - 13.0) / 4.0) ** 2)
        
        # Factor 3: PIR sensor intensity ratio
        pir_intensity = min(1.0, pir_count / max(1, config["base_capacity"]))
        
        # Weighted fusion score
        raw_score = (
            config["weight_timetable"] * timetable_score +
            config["weight_pir"] * pir_intensity
        ) * (0.8 + 0.2 * time_factor)
        
        # Add slight natural jitter
        jitter = (random.random() - 0.5) * 0.04
        final_pct = max(0, min(100, int((raw_score + jitter) * 100)))
        return final_pct


class WaterAnomalyDetector:
    """
    Statistical anomaly detector for real-time ultrasonic water telemetry.
    Flags sudden surges matching pipe bursting or line fractures.
    """
    def __init__(self, baseline_mean: float = 480.0, baseline_std: float = 45.0):
        self.mean = baseline_mean
        self.std = baseline_std
        self.critical_z_threshold = 4.5  # Surge cutoff

    def evaluate_flow_rate(self, current_flow: float) -> Tuple[bool, float]:
        """
        Evaluates current flow in L/hr.
        Returns: (is_anomaly: bool, z_score: float)
        """
        z_score = (current_flow - self.mean) / self.std
        is_anomaly = z_score > self.critical_z_threshold
        return is_anomaly, round(z_score, 2)

    def reset(self):
        """Restores nominal parameters."""
        self.mean = 480.0
        self.std = 45.0


class CarbonEnergyLedger:
    """
    ESG accounting engine implementing Central Electricity Authority (CEA)
    grid emission factors for Northern Regional Grid (India).
    """
    def __init__(self, emission_factor_kg_per_kwh: float = 0.82):
        self.emission_factor = emission_factor_kg_per_kwh

    def calculate_carbon_reduction(self, saved_kwh: float) -> float:
        """
        Converts avoided kilowatt-hours into kg CO2 equivalent avoided.
        Formula: Carbon (kg CO2e) = kWh * Grid Emission Factor
        """
        return round(saved_kwh * self.emission_factor, 2)

    def get_benchmark_report(self, weekday_saved: float = 384.2, weekend_saved: float = 429.5) -> Dict[str, Any]:
        """Generates comprehensive campus sustainability metrics."""
        return {
            "weekday": {
                "energy_saved_kwh": weekday_saved,
                "carbon_abated_kg_co2e": round(weekday_saved * self.emission_factor, 1),
                "equivalent_trees_planted": round((weekday_saved * self.emission_factor) / 21.77, 1)
            },
            "weekend": {
                "energy_saved_kwh": weekend_saved,
                "carbon_abated_kg_co2e": round(weekend_saved * self.emission_factor, 1),
                "equivalent_trees_planted": round((weekend_saved * self.emission_factor) / 21.77, 1)
            }
        }
