from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sitemapper import Sitemapper
import datetime
import os
import re
import requests
from dotenv import load_dotenv
import io

# Local AI (Ollama)
from local_ai import generate_itinerary

# Road Route
from route_map import get_road_route

# New modules
from budget_calculator import estimate_budget, get_budget_tips, compare_budgets
from database import (
    save_trip, get_trip_history, get_trip_by_id, 
    update_trip_rating, delete_trip, get_trip_statistics,
    add_favorite_destination, get_favorite_destinations
)
from export_utils import export_to_json, export_to_ical, export_to_markdown

# ------------------ LOAD ENV ------------------
load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not FLASK_SECRET_KEY:
    raise RuntimeError("FLASK_SECRET_KEY not set in .env")

# ------------------ FLASK APP ------------------
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# ------------------ SITEMAP ------------------
sitemapper = Sitemapper(app=app)

# ------------------ SECURITY (CSP) ------------------
@app.after_request
def add_csp_header(response):
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self' https://*.openstreetmap.org https://router.project-osrm.org; "

    )
    response.headers["Content-Security-Policy"] = csp
    return response

# ------------------ WEATHER API ------------------
def get_weather_data(api_key, location, start_date, end_date):
    if not api_key:
        return None

    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
        f"timeline/{location}/{start_date}/{end_date}"
        f"?unitGroup=metric&include=days&key={api_key}&contentType=json"
    )

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Weather API Error:", e)
        return None

# ------------------ FORMAT AI OUTPUT ------------------
def format_plan_to_html(text):
    text = text.replace("\n", "<br>")
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    return text

# ------------------ ROUTES ------------------

@sitemapper.include()
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        source = request.form.get("source")
        destination = request.form.get("destination")
        start_date = request.form.get("date")
        end_date = request.form.get("return")
        budget_type = request.form.get("budget_type", "moderate")
        travelers = int(request.form.get("travelers", 1))

        if not all([source, destination, start_date, end_date]):
            flash("All fields are required!", "danger")
            return redirect(url_for("index"))

        try:
            days = (
                datetime.datetime.strptime(end_date, "%Y-%m-%d")
                - datetime.datetime.strptime(start_date, "%Y-%m-%d")
            ).days + 1
        except Exception:
            flash("Invalid date format.", "danger")
            return redirect(url_for("index"))

        if days <= 0:
            flash("Return date must be after travel date.", "danger")
            return redirect(url_for("index"))

        # ---------------- AI Itinerary ----------------
        plan_text = generate_itinerary(
            source, destination, start_date, end_date, days
        )

        if not plan_text:
            flash("Failed to generate itinerary.", "danger")
            return redirect(url_for("index"))

        # ---------------- Weather ----------------
        weather_data = get_weather_data(
            WEATHER_API_KEY, destination, start_date, end_date
        )

        # ---------------- Road Route ----------------
        route_data = get_road_route(source, destination)

        # ---------------- Budget Calculation ----------------
        budget_data = estimate_budget(days, budget_type, "default", travelers)
        budget_tips = get_budget_tips(budget_type)

        # ---------------- Save to Database ----------------
        trip_id = save_trip(
            source, destination, start_date, end_date, days,
            format_plan_to_html(plan_text), weather_data, route_data
        )

        # ---------------- Save Session ----------------
        session["trip_id"] = trip_id
        session["source"] = source
        session["itinerary"] = format_plan_to_html(plan_text)
        session["destination"] = destination
        session["start_date"] = start_date
        session["end_date"] = end_date
        session["days"] = days
        session["weather_data"] = weather_data
        session["route_data"] = route_data
        session["budget_data"] = budget_data
        session["budget_tips"] = budget_tips
        session["travelers"] = travelers

        return redirect(url_for("dashboard"))

    return render_template("index.html")

# ------------------ DASHBOARD ------------------
@sitemapper.include()
@app.route("/dashboard")
def dashboard():
    if "itinerary" not in session:
        flash("Session expired. Please plan again.", "warning")
        return redirect(url_for("index"))

    return render_template(
        "dashboard.html",
        trip_id=session.get("trip_id"),
        source=session.get("source"),
        plan=session.get("itinerary"),
        destination=session.get("destination"),
        start_date=session.get("start_date"),
        end_date=session.get("end_date"),
        days=session.get("days"),
        weather_data=session.get("weather_data"),
        route_data=session.get("route_data"),
        budget_data=session.get("budget_data"),
        budget_tips=session.get("budget_tips"),
        travelers=session.get("travelers", 1)
    )

# ------------------ STATIC PAGES ------------------
@sitemapper.include()
@app.route("/about")
def about():
    return render_template("about.html")

@sitemapper.include()
@app.route("/contact")
def contact():
    return render_template("contact.html")

@sitemapper.include()
@app.route("/features")
def features():
    return render_template("features.html")

# ------------------ NEW ROUTES ------------------

# Trip History
@app.route("/history")
def history():
    trips = get_trip_history(limit=20)
    stats = get_trip_statistics()
    return render_template("history.html", trips=trips, stats=stats)

# View specific trip
@app.route("/trip/<int:trip_id>")
def view_trip(trip_id):
    trip = get_trip_by_id(trip_id)
    if not trip:
        flash("Trip not found.", "danger")
        return redirect(url_for("history"))
    return render_template("view_trip.html", trip=trip)

# Rate trip
@app.route("/rate-trip/<int:trip_id>", methods=["POST"])
def rate_trip(trip_id):
    rating = request.form.get("rating")
    notes = request.form.get("notes")
    
    if rating:
        update_trip_rating(trip_id, int(rating), notes)
        flash("Trip rated successfully!", "success")
    
    return redirect(url_for("view_trip", trip_id=trip_id))

# Delete trip
@app.route("/delete-trip/<int:trip_id>", methods=["POST"])
def delete_trip_route(trip_id):
    delete_trip(trip_id)
    flash("Trip deleted successfully.", "success")
    return redirect(url_for("history"))

# Export trip as JSON
@app.route("/export/<int:trip_id>/json")
def export_json(trip_id):
    trip = get_trip_by_id(trip_id)
    if not trip:
        flash("Trip not found.", "danger")
        return redirect(url_for("history"))
    
    json_data = export_to_json(trip)
    
    buffer = io.BytesIO()
    buffer.write(json_data.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name=f'trip_{trip["destination"]}_{trip["start_date"]}.json'
    )

# Export trip as iCal
@app.route("/export/<int:trip_id>/ical")
def export_ical(trip_id):
    trip = get_trip_by_id(trip_id)
    if not trip:
        flash("Trip not found.", "danger")
        return redirect(url_for("history"))
    
    ical_data = export_to_ical(trip)
    
    buffer = io.BytesIO()
    buffer.write(ical_data.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/calendar',
        as_attachment=True,
        download_name=f'trip_{trip["destination"]}_{trip["start_date"]}.ics'
    )

# Export trip as Markdown
@app.route("/export/<int:trip_id>/markdown")
def export_markdown(trip_id):
    trip = get_trip_by_id(trip_id)
    if not trip:
        flash("Trip not found.", "danger")
        return redirect(url_for("history"))
    
    md_data = export_to_markdown(trip)
    
    buffer = io.BytesIO()
    buffer.write(md_data.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/markdown',
        as_attachment=True,
        download_name=f'trip_{trip["destination"]}_{trip["start_date"]}.md'
    )

# Budget comparison
@app.route("/budget-compare")
def budget_compare():
    days = request.args.get("days", 7, type=int)
    travelers = request.args.get("travelers", 1, type=int)
    region = request.args.get("region", "default")
    
    comparison = compare_budgets(days, region, travelers)
    return jsonify(comparison)

# Add to favorites
@app.route("/add-favorite", methods=["POST"])
def add_favorite():
    destination = request.form.get("destination")
    reason = request.form.get("reason")
    
    if destination:
        add_favorite_destination(destination, reason)
        flash(f"{destination} added to favorites!", "success")
    
    return redirect(request.referrer or url_for("index"))

# View favorites
@app.route("/favorites")
def favorites():
    favs = get_favorite_destinations()
    return render_template("favorites.html", favorites=favs)

# ------------------ SEO ------------------
@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return sitemapper.generate()

# ------------------ ERRORS ------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# ------------------ GLOBAL ------------------
@app.context_processor
def inject_now():
    return {"now": datetime.datetime.now()}

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
