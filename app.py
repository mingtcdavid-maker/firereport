import io
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "docx_template" / "SCDF_Fire_Investigation_Report_TEMPLATE.docx"

app = Flask(__name__)


def clean(value):
    return (value or "").strip()


def build_context(form):
    context = {
        "investigator_rank_and_name": clean(form.get("investigator_name")),
        "investigator": {
            "name": clean(form.get("investigator_name")),
            "appointment": clean(form.get("investigator_appointment")),
            "station": clean(form.get("investigator_station")),
        },
        "incident_no": clean(form.get("incident_no")),
        "date_of_fire": clean(form.get("date_of_fire")),
        "time_of_call": clean(form.get("time_of_call")),
        "address_of_fire": clean(form.get("address_of_fire")),
        "fire_involved": clean(form.get("fire_involved")),
        "method_of_extinguishment": clean(form.get("method_of_extinguishment")),
        "damages_sustained": clean(form.get("damages_sustained")),
        "ignition_source": clean(form.get("ignition_source")),
        "ignition_fuels": clean(form.get("ignition_fuels")),
        "events_leading_to_incident": clean(form.get("events_leading_to_incident")),
        "burn_patterns_observed": clean(form.get("burn_patterns_observed")),
        "evidence_at_scene": clean(form.get("evidence_at_scene")),
        "insured_mark_no": "",
        "other_information": "",
    }

    eyewitness_fields = {
        "name": clean(form.get("eyewitness_name")),
        "designation": clean(form.get("eyewitness_designation")),
        "nric": clean(form.get("eyewitness_nric")),
        "nationality": clean(form.get("eyewitness_nationality")),
        "address": clean(form.get("eyewitness_address")),
        "contact": clean(form.get("eyewitness_contact")),
    }
    # Only include fields that were actually filled in, so the template's
    # {{ eyewitness.x|default('NIL') }} falls back correctly for the rest.
    context["eyewitness"] = {k: v for k, v in eyewitness_fields.items() if v}

    return context


def safe_filename(incident_no):
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", incident_no.strip()) if incident_no else ""
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Fire_Investigation_Report_{name}.docx"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    required_fields = [
        "investigator_name",
        "investigator_appointment",
        "investigator_station",
        "incident_no",
        "date_of_fire",
        "time_of_call",
        "address_of_fire",
        "fire_involved",
        "method_of_extinguishment",
        "damages_sustained",
        "ignition_source",
        "ignition_fuels",
        "events_leading_to_incident",
        "burn_patterns_observed",
        "evidence_at_scene",
    ]
    missing = [f for f in required_fields if not clean(request.form.get(f))]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    if not TEMPLATE_PATH.exists():
        return jsonify({"error": "Report template not found on server"}), 500

    context = build_context(request.form)

    doc = DocxTemplate(str(TEMPLATE_PATH))
    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    filename = safe_filename(context["incident_no"])
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
