"""
EcoPrime: AI-Enabled Campus Sustainability Prototype | GNIOT
Flask Backend & REST API Service
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from ai_engine import CampusOccupancyPredictor, WaterAnomalyDetector, CarbonEnergyLedger
from iot_simulator import CampusIoTSimulator

app = Flask(__name__, static_folder=".")

# Initialize AI & IoT Engines
predictor = CampusOccupancyPredictor()
anomaly_detector = WaterAnomalyDetector()
ledger = CarbonEnergyLedger()
simulator = CampusIoTSimulator()

@app.route("/")
def serve_dashboard():
    return send_from_directory(".", "index.html")

@app.route("/api/telemetry", methods=["GET"])
def get_telemetry():
    """Returns current real-time telemetry from GNIOT edge sensors."""
    mode = request.args.get("mode", "weekday")
    data = simulator.get_current_state(mode=mode)
    return jsonify(data)

@app.route("/api/predict-occupancy", methods=["POST"])
def predict_occupancy():
    """Predicts 30-minute lookahead occupancy using trained ML regressor."""
    payload = request.get_json() or {}
    room_id = payload.get("room_id", "room-101")
    timetable_active = payload.get("timetable_active", True)
    hour = payload.get("hour", 14)
    pir_count = payload.get("pir_count", 45)
    
    prob = predictor.predict_occupancy_percentage(
        room_id=room_id,
        timetable_active=timetable_active,
        hour=hour,
        pir_count=pir_count
    )
    return jsonify({
        "room_id": room_id,
        "predicted_occupancy_pct": prob,
        "recommendation": "MAINTAIN_POWER" if prob > 30 else "TRIGGER_AUTO_CUTOFF"
    })

@app.route("/api/simulate-cutoff", methods=["POST"])
def simulate_cutoff():
    """Executes AI 15-min vacancy cutoff across idle wings."""
    result = simulator.execute_vacancy_cutoff()
    energy_saved = result["saved_kwh"]
    carbon_abated = ledger.calculate_carbon_reduction(energy_saved)
    
    return jsonify({
        "status": "SUCCESS",
        "action": "AUTO_CUTOFF_APPLIED",
        "saved_kwh": energy_saved,
        "abated_kg_co2e": carbon_abated,
        "affected_rooms": result["affected_rooms"]
    })

@app.route("/api/simulate-leak", methods=["POST"])
def simulate_leak():
    """Simulates high-velocity hydraulic rupture in campus main riser."""
    surge_data = simulator.inject_hydraulic_rupture()
    is_anomaly, score = anomaly_detector.evaluate_flow_rate(surge_data["flow_rate_lph"])
    
    return jsonify({
        "status": "ALERT",
        "flow_rate_lph": surge_data["flow_rate_lph"],
        "anomaly_flag": is_anomaly,
        "anomaly_score": score,
        "automated_actuator": "SOLENOID_V12_TRIPPED",
        "message": "Critical hydraulic rupture detected. Automated isolation initiated."
    })

@app.route("/api/reset", methods=["POST"])
def reset_system():
    """Resets simulator and model states to nominal baseline."""
    simulator.reset_baseline()
    anomaly_detector.reset()
    return jsonify({"status": "RESET_COMPLETE", "message": "Campus metrics restored to baseline."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[*] Starting EcoPrime AI Campus Gateway at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
