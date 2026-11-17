"""
EcoPrime IoT Gateway Simulator: Sensor State and Relay Telemetry Generator
Greater Noida Institute of Technology (GNIOT) Campus
"""

import time
import random
from typing import Dict, Any, List

class CampusIoTSimulator:
    """
    Simulates edge gateway polling across GNIOT lecture wings and main water conduits.
    """
    def __init__(self):
        self.water_flow_rate = 480.0
        self.leak_active = False
        self.cumulative_saved_kwh = 0.0
        
        self.room_definitions = [
            {
                "id": "room-101",
                "name": "Block A - Room 101",
                "type": "Lecture Theater (Cap: 80)",
                "weekday": {"pir": "Occupied", "timetable": "Class Active", "prediction": 94, "relay": "ON"},
                "weekend": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 5, "relay": "AUTO CUTOFF"},
                "override": False
            },
            {
                "id": "room-102",
                "name": "Block A - Room 102",
                "type": "Tutorial Room (Cap: 40)",
                "weekday": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 12, "relay": "AUTO CUTOFF"},
                "weekend": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 2, "relay": "AUTO CUTOFF"},
                "override": False
            },
            {
                "id": "room-204",
                "name": "Block B - Lab 204",
                "type": "IoT & Systems Lab (Cap: 60)",
                "weekday": {"pir": "Occupied", "timetable": "Class Active", "prediction": 88, "relay": "ON"},
                "weekend": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 18, "relay": "AUTO CUTOFF"},
                "override": False
            },
            {
                "id": "room-301",
                "name": "Block C - Hall 301",
                "type": "Seminar Auditorium (Cap: 250)",
                "weekday": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 24, "relay": "AUTO CUTOFF"},
                "weekend": {"pir": "Vacant", "timetable": "Empty Break", "prediction": 4, "relay": "AUTO CUTOFF"},
                "override": False
            }
        ]

    def get_current_state(self, mode: str = "weekday") -> Dict[str, Any]:
        """Returns snapshot of current edge telemetry."""
        base_saved = 384.2 if mode == "weekday" else 429.5
        total_saved = round(base_saved + self.cumulative_saved_kwh, 1)
        carbon_abated = round(total_saved * 0.82, 1)

        return {
            "mode": mode,
            "timestamp": time.time(),
            "kpis": {
                "daily_energy_saved_kwh": total_saved,
                "daily_carbon_abated_kg": carbon_abated,
                "water_flow_rate_lph": self.water_flow_rate,
                "water_rupture_alert": self.leak_active,
                "ai_occupancy_accuracy_pct": 99.6
            },
            "rooms": self.room_definitions
        }

    def execute_vacancy_cutoff(self) -> Dict[str, Any]:
        """Simulates 15-min vacancy cutoff event."""
        affected = []
        for room in self.room_definitions:
            if not room["override"]:
                affected.append(room["id"])
        
        # Add between 8.5 and 12.7 kWh to counter
        incremental_kwh = round(random.uniform(8.5, 12.7), 2)
        self.cumulative_saved_kwh += incremental_kwh

        return {
            "saved_kwh": incremental_kwh,
            "total_saved_kwh": round(self.cumulative_saved_kwh, 1),
            "affected_rooms": affected
        }

    def inject_hydraulic_rupture(self) -> Dict[str, Any]:
        """Simulates main line leak anomaly."""
        self.leak_active = True
        self.water_flow_rate = 32500.0
        return {
            "leak_active": True,
            "flow_rate_lph": self.water_flow_rate,
            "timestamp": time.time()
        }

    def reset_baseline(self):
        """Resets all simulation parameters."""
        self.water_flow_rate = 480.0
        self.leak_active = False
        self.cumulative_saved_kwh = 0.0
        for r in self.room_definitions:
            r["override"] = False
