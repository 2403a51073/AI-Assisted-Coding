from flask import Flask, request, jsonify, send_file
import csv, io
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# ============================================================
# ROUTE: Serve the main HTML file (index2.html) from the folder
# ============================================================
@app.route("/")
def index():
    """Return the main HTML frontend."""
    return send_file("index2.html")


# ============================================================
# HELPER FUNCTION: Read prices from uploaded CSV
# ============================================================
def read_prices_from_file(file_storage):
    """
    Reads uploaded CSV file and extracts numeric prices.
    Assumes last numeric column contains the price.
    Returns list of float values.
    """
    # Convert file stream to text
    stream = io.StringIO(file_storage.stream.read().decode('utf-8', errors='ignore'))

    reader = csv.reader(stream)
    header = next(reader, None)  # Skip header row if exists

    prices = []
    for row in reader:
        if not row:
            continue

        # Parse row from last column backward, pick first numeric cell
        for cell in reversed(row):
            try:
                prices.append(float(cell))
                break
            except:
                continue

    return prices


# ============================================================
# HELPER: Calculate slope using simple linear regression
# ============================================================
def linear_regression_slope(prices):
    """
    Returns slope of best-fit line using simple linear regression.
    Slope determines direction of trend.
    """
    n = len(prices)
    if n < 2:
        return 0.0

    xs = list(range(n))  # X-axis index values
    x_mean = sum(xs) / n
    y_mean = sum(prices) / n

    # ∑(x - mean_x)(y - mean_y)
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, prices))

    # ∑(x - mean_x)^2
    den = sum((x - x_mean) ** 2 for x in xs)

    return num / den if den != 0 else 0.0


# ============================================================
# HELPER: Classify trend using slope and relative change
# ============================================================
def classify_trend(prices):
    """
    Classifies market trend based on slope and relative difference.
    Returns tuple: (trend_name, slope_value)
    """
    if not prices:
        return ("NO DATA", 0.0)

    slope = linear_regression_slope(prices)
    avg = sum(prices)/len(prices) if prices else 0
    rel = slope / avg if avg else 0

    # Strong slope rules
    if rel > 0.002:
        return ("UPWARD TREND", slope)
    if rel < -0.002:
        return ("DOWNWARD TREND", slope)

    # Weak slope → check start vs end price
    if prices[-1] > prices[0] * 1.01:
        return ("UPWARD TREND", slope)
    if prices[-1] < prices[0] * 0.99:
        return ("DOWNWARD TREND", slope)

    return ("SIDEWAYS", slope)


# ============================================================
# HELPER: Generate auto dates for each price point
# ============================================================
def generate_dates_for_prices(n, end=None):
    """
    Generates 'n' dates ending at today's date.
    Returns list of formatted date strings.
    """
    end = end or datetime.utcnow()
    return [(end - timedelta(days=(n - 1 - i))).strftime("%d-%m-%Y") for i in range(n)]


# ============================================================
# ROUTE: Receive uploaded CSV and return full JSON analysis
# ============================================================
@app.route("/analyze", methods=["POST"])
def analyze():
    """Reads uploaded CSV, performs calculations, returns JSON."""

    # Check if user uploaded a file
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files["file"]
    # Extract numeric prices
    prices = read_prices_from_file(f)
    # Determine trend & slope
    trend, slope = classify_trend(prices)
    # Basic stats
    highest = max(prices) if prices else 0
    lowest = min(prices) if prices else 0
    average = sum(prices)/len(prices) if prices else 0
    count = len(prices)
    # Day-to-day changes
    changes = [0.0] + [prices[i] - prices[i - 1] for i in range(1, count)]
    # Auto-generate dates for x-axis
    dates = generate_dates_for_prices(count)
    # Return everything to frontend
    return jsonify({
        "trend": trend,
        "slope": slope,
        "prices": prices,
        "highest": round(highest, 2),
        "lowest": round(lowest, 2),
        "average": round(average, 2),
        "count": count,
        "changes": changes,
        "dates": dates
    })
# ============================================================
# ROUTE: Serve CSS file
# ============================================================
@app.route("/style2.css")
def css():
    """Serve CSS file."""
    return send_file("style2.css")
# ============================================================
# ROUTE: Serve JS file
# ============================================================
@app.route("/app2.js")
def js():
    """Serve JS file."""
    return send_file("app2.js")
# ============================================================
# MAIN PROGRAM ENTRY
# ============================================================
if __name__ == "__main__":
    # debug=True allows auto-reload and error messages
    app.run(debug=True)
