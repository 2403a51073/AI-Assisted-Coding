// ================================
// Get form and chart canvas elements
// ================================
const form = document.getElementById("uploadForm");
const chartCanvas = document.getElementById("chart");

// Chart instance (will be used to destroy old chart before drawing new one)
let chart = null;

// ========================================================
// EVENT LISTENER: Handle form submission (CSV Upload)
// ========================================================
form.addEventListener("submit", async e => {
    
    // Prevent the form from reloading the page
    e.preventDefault();

    // Get the uploaded CSV file
    const file = document.getElementById("file").files[0];
    if (!file) return alert("Choose CSV");

    // Create a FormData object to send file in POST request
    const fd = new FormData();
    fd.append("file", file);

    // Send file to Flask backend using Fetch API
    const res = await fetch("/analyze", {
        method: "POST",
        body: fd
    });

    // Parse JSON response from backend
    const data = await res.json();

    // ===================================
    // Update Trend and Statistics in UI
    // ===================================
    document.getElementById("trend").textContent = data.trend;
    document.getElementById("slope").textContent = "Slope: " + data.slope.toFixed(4);
    document.getElementById("highest").textContent = data.highest;
    document.getElementById("lowest").textContent = data.lowest;
    document.getElementById("average").textContent = data.average;
    document.getElementById("count").textContent = data.count;

    // Extract values for chart and table
    const prices = data.prices;
    const labels = data.dates;

    // ===================================
    // DRAW / UPDATE CHART
    // ===================================
    // If chart already exists, destroy before drawing new one
    if (chart) chart.destroy();

    // Create new Chart.js line chart
    chart = new Chart(chartCanvas, {
        type: "line",
        data: {
            labels,  // Dates
            datasets: [{
                label: "Price",
                data: prices,      // Price values
                borderWidth: 2,    // Line thickness
                tension: 0.2       // Smooth curved line
            }]
        },
        options: {
            plugins: {
                legend: { display: false }   // Hide legend
            },
            scales: {
                x: { display: true },  // Show X-axis
                y: { display: true }   // Show Y-axis
            }
        }
    });

    // ===================================
    // UPDATE HISTORY TABLE
    // ===================================
    const tbody = document.querySelector("#historyTable tbody");
    tbody.innerHTML = ""; // Clear old rows

    // Loop through each price entry and create a table row
    for (let i = 0; i < prices.length; i++) {

        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${labels[i]}</td>          <!-- Date -->
            <td>${prices[i]}</td>          <!-- Price -->
            <td>${i === 0 ? "-" : data.changes[i].toFixed(2)}</td>  <!-- Change -->
        `;

        tbody.appendChild(tr);
    }
});
