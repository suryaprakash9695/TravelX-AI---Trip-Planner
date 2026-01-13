from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sitemapper import Sitemapper
import datetime
import os
import re
import requests
from dotenv import load_dotenv

# Local AI (Ollama)
from local_ai import generate_itinerary

# Road Route
from route_map import get_road_route

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

        # ---------------- Save Session ----------------
        session["itinerary"] = format_plan_to_html(plan_text)
        session["destination"] = destination
        session["weather_data"] = weather_data
        session["route_data"] = route_data

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
        plan=session.get("itinerary"),
        destination=session.get("destination"),
        weather_data=session.get("weather_data"),
        route_data=session.get("route_data"),
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
