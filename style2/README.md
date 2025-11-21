# ** Stock Market Trend Analyzer  – README**

This is a simple web application that analyzes stock prices from a CSV file.
It uses **Flask** on the backend and **HTML, CSS, JavaScript, Chart.js** on the frontend.

The app shows:

* Overall **trend** (Upward / Downward / Sideways)
* **Slope** using linear regression
* **Highest**, **Lowest**, **Average** price
* Total number of records
* Interactive **price chart**
* A price **history table** with daily changes

---

## ** How to Run the Application**

### **1️⃣ Install Flask**

```bash
pip install flask
```

---

### **2️⃣ Start the App**

Run:

```bash
python app2.py
```

A local server will start at:

```
http://127.0.0.1:5000/
```

Open this link in your browser.

---

## ** How to Use the App**

1. Open the application in your browser.
2. Click **Choose File** and upload a CSV file containing stock prices.
3. Click **Analyze**.
4. The app will show:

   * Trend
   * Slope
   * Highest, Lowest, Average price
   * Count of data points
   * Interactive line chart
   * Full history with daily price changes

The CSV can contain one or multiple columns.
The app automatically reads the **last numeric value in each row**.

---

## ** Technologies Used**

* **Python + Flask**
* **HTML**
* **CSS**
* **JavaScript**
* **Chart.js** (for graph)

---


