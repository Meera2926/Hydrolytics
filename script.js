const API_BASE = "http://127.0.0.1:5000";

// State
let appState = {
    lastPredictedUsage: 0,
    lastRiskLevel: "N/A",
    lastCarbonKg: 0,
    lastEnergyKwh: 0,
    peakDay: "N/A",
    hasPredicted: false
};

// Global Integrations
let mapInstance = null;
let heatLayer = null; 
let markerLayer = null;
let usageChartInstance = null;
let weatherChartInstance = null;

// Campus Coordinates with Base Capacity
const CAMPUS_LOCATIONS = [
    { id: "hostel", name: "Hostel", lat: 12.9715, lng: 77.5940, baseRatio: 0.50, capacity: 7500 },
    { id: "mess", name: "Mess", lat: 12.9725, lng: 77.5950, baseRatio: 0.30, capacity: 4500 },
    { id: "academic", name: "Academic Block", lat: 12.9705, lng: 77.5930, baseRatio: 0.15, capacity: 2500 },
    { id: "library", name: "Library", lat: 12.9710, lng: 77.5955, baseRatio: 0.05, capacity: 1000 }
];

document.addEventListener("DOMContentLoaded", () => {
    // Check Authentication
    checkAuth();
    setupAuthLogic();

    document.getElementById("date").valueAsDate = new Date();
    
    // Set Chart.js Dark Mode Defaults
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Arial, sans-serif";
    
    // Wire events
    document.getElementById("prediction-form").addEventListener("submit", handlePredict);
    
    fetchInsights(); // Load data initially
});

// ── Authentication System ──
let isLoginMode = true;

function setupAuthLogic() {
    document.getElementById("toggle-auth").addEventListener("click", (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;
        document.getElementById("name-group").classList.toggle("hidden", isLoginMode);
        document.getElementById("auth-name").required = !isLoginMode;
        
        document.getElementById("auth-title").innerText = isLoginMode ? "Welcome Back" : "Create Account";
        document.getElementById("auth-btn").innerText = isLoginMode ? "Authenticate" : "Sign Up";
        e.target.innerText = isLoginMode ? "New user? Create an account" : "Already have an account? Sign In";
        document.getElementById("auth-error").classList.add("hidden");
    });

    document.getElementById("auth-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const user = document.getElementById("auth-user").value.trim();
        const pass = document.getElementById("auth-pass").value.trim();
        const errAlert = document.getElementById("auth-error");
        errAlert.classList.add("hidden");

        let db = JSON.parse(localStorage.getItem('hydroUsers') || '{}');

        if (!isLoginMode) {
            // Sign Up Logic
            const name = document.getElementById("auth-name").value.trim();
            if(db[user]) {
                errAlert.innerText = "Username already exists!";
                errAlert.classList.remove("hidden");
                return;
            }
            db[user] = { pass: pass, name: name };
            localStorage.setItem("hydroUsers", JSON.stringify(db));
            
            // Auto login
            localStorage.setItem("hydroActive", JSON.stringify({user, name}));
            proceedToDashboard(name);

        } else {
            // Login Logic
            if(db[user] && db[user].pass === pass) {
                localStorage.setItem("hydroActive", JSON.stringify({user, name: db[user].name}));
                proceedToDashboard(db[user].name);
            } else {
                errAlert.innerText = "Invalid username or password!";
                errAlert.classList.remove("hidden");
            }
        }
    });
}

function checkAuth() {
    let activeUser = JSON.parse(localStorage.getItem("hydroActive"));
    if (activeUser) {
        proceedToDashboard(activeUser.name);
    }
}

function proceedToDashboard(fullName) {
    document.getElementById("auth-overlay").classList.add("hidden");
    document.getElementById("main-nav").classList.remove("hidden");
    document.getElementById("main-app").classList.remove("hidden");
    
    // Set Navigation Name
    document.getElementById("nav-user-name").innerHTML = `Hello, <b>${fullName}</b>`;

    // Set greeting based on time of day and name
    const hour = new Date().getHours();
    let greet = "Welcome to Hydrolytix Command";
    if(hour < 12) greet = `Good Morning, ${fullName}`;
    else if(hour < 18) greet = `Good Afternoon, ${fullName}`;
    else greet = `Good Evening, ${fullName}`;
    
    document.getElementById("greeting-msg").innerText = greet;

    // We must initialize the map *after* the overlay disappears so Leaflet calculates bounds correctly
    if(!mapInstance) initMap();
}

// Ensure function is exposed globally for HTML onclick
window.logout = function() {
    localStorage.removeItem("hydroActive");
    document.getElementById("auth-form").reset();
    document.getElementById("auth-overlay").classList.remove("hidden");
    document.getElementById("main-nav").classList.add("hidden");
    document.getElementById("main-app").classList.add("hidden");
};


// ── Navigation Logic ──
function switchTab(sectionId, element) {
    document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
    if(element) element.classList.add('active');

    document.querySelectorAll('.page-section').forEach(sec => sec.classList.add('hidden'));
    document.getElementById(sectionId).classList.remove('hidden');

    if (sectionId === 'heatmap' && mapInstance) {
        setTimeout(() => mapInstance.invalidateSize(), 200);
    }
}

// ── API Handlers ──
async function fetchInsights() {
    try {
        const response = await fetch(`${API_BASE}/insights`);
        const data = await response.json();
        
        if (data.status === "ok") {
            appState.peakDay = data.peak_usage_day;
            document.getElementById("ins-peak").innerText = data.peak_usage_day;
            document.getElementById("ins-high").innerText = `${data.highest_usage.toLocaleString()} L`;
            document.getElementById("ins-avg").innerText = `${data.average_usage.toLocaleString()} L`;
            
            buildCharts(data.chart_data);
        }
    } catch (error) {
        console.error("API error", error);
    }
}

async function handlePredict(e) {
    e.preventDefault();
    document.getElementById("loading-txt").classList.remove("hidden");
    
    const d = new Date(document.getElementById("date").value);
    let pyDay = d.getDay() === 0 ? 6 : d.getDay() - 1;
    let isWeekend = (pyDay >= 5) ? 1 : 0;
    let startOfYear = new Date(d.getFullYear(), 0, 0);
    let diff = (d - startOfYear) + ((startOfYear.getTimezoneOffset() - d.getTimezoneOffset()) * 60 * 1000);
    let dayOfYear = Math.floor( diff / 86400000 );

    const payload = {
        temperature: parseFloat(document.getElementById("temperature").value),
        rainfall: parseFloat(document.getElementById("rainfall").value),
        humidity: parseFloat(document.getElementById("humidity").value),
        occupancy: parseInt(document.getElementById("occupancy").value),
        timetable_factor: parseFloat(document.getElementById("timetable_factor").value),
        day_of_week: pyDay, month: d.getMonth() + 1, day_of_year: dayOfYear, is_weekend: isWeekend
    };

    try {
        const [resPredict, resCrisis, resCarbon, resOpt] = await Promise.all([
            fetch(`${API_BASE}/predict`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) }),
            fetch(`${API_BASE}/crisis`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) }),
            fetch(`${API_BASE}/carbon`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) }),
            fetch(`${API_BASE}/optimize`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) })
        ]);

        const [dPredict, dCrisis, dCarbon, dOpt] = await Promise.all([resPredict.json(), resCrisis.json(), resCarbon.json(), resOpt.json()]);

        // State update
        appState.hasPredicted = true;
        appState.lastPredictedUsage = dCrisis.predicted_usage_L;
        appState.lastRiskLevel = dCrisis.crisis_level;
        appState.lastCarbonKg = dCarbon.carbon_footprint_kg_co2;
        appState.lastEnergyKwh = dCarbon.energy_consumption_kwh;

        // UI Updates -> Prediction Quick Panel
        document.getElementById("pred-res-usage").innerText = appState.lastPredictedUsage.toLocaleString();
        
        // UI Updates -> Dashboard Main
        document.getElementById("no-data-alert").classList.add("hidden");
        document.getElementById("dash-usage").innerText = `${appState.lastPredictedUsage.toLocaleString()} L`;
        
        const riskEl = document.getElementById("dash-risk");
        const btnBg = document.getElementById("risk-card-container").querySelector('.bg-risk');
        riskEl.innerText = appState.lastRiskLevel;
        riskEl.className = "val-risk"; btnBg.className = "icon-wrap bg-risk"; 
        
        let hexColor = "#10b981"; 
        if(appState.lastRiskLevel === "Low") { riskEl.classList.add("low"); btnBg.classList.add("low"); }
        else if(appState.lastRiskLevel === "Medium") { riskEl.classList.add("medium"); btnBg.classList.add("medium"); hexColor = "#f59e0b"; }
        else { riskEl.classList.add("high"); btnBg.classList.add("high"); hexColor = "#ef4444"; }

        document.getElementById("dash-carbon").innerText = `${appState.lastCarbonKg} kg`;
        document.getElementById("dash-opt").innerText = dOpt.suggestion;

        // UI Updates -> Dashboard Weather Widget
        document.getElementById("w-temp").innerText = `${payload.temperature} °C`;
        document.getElementById("w-rain").innerText = `${payload.rainfall} mm`;
        document.getElementById("w-hum").innerText = `${payload.humidity} %`;

        // Add Log
        addAlert(`New simulation complete. Volume: ${appState.lastPredictedUsage.toLocaleString()}L. Risk: ${appState.lastRiskLevel}.`);

        // UI Updates -> Carbon Page
        document.getElementById("carb-energy").innerText = `${appState.lastEnergyKwh} kWh`;
        document.getElementById("carb-co2").innerText = `${appState.lastCarbonKg} kg`;
        
        let enPct = Math.min((appState.lastEnergyKwh / 10) * 100, 100).toFixed(0);
        let coPct = Math.min((appState.lastCarbonKg / 5) * 100, 100).toFixed(0);
        
        document.getElementById("energy-bar").style.width = `${enPct}%`;
        document.getElementById("energy-pct-txt").innerText = `${enPct}%`;
        document.getElementById("co2-bar").style.width = `${coPct}%`;
        document.getElementById("co2-pct-txt").innerText = `${coPct}%`;

        // Map updates
        updateMap(appState.lastPredictedUsage, hexColor);

        document.getElementById("loading-txt").classList.add("hidden");
    } catch(err) {
        console.error(err);
        document.getElementById("loading-txt").classList.add("hidden");
        addAlert(`Error: Failed to fetch backend predictions.`);
    }
}

function addAlert(msg) {
    const list = document.getElementById("alerts-list");
    const li = document.createElement("li");
    const icon = msg.includes("Error") ? 'fa-triangle-exclamation text-red' : 'fa-circle-info text-cyan';
    li.innerHTML = `<i class="fa-solid ${icon}"></i> ${msg}`;
    list.prepend(li);
    if(list.children.length > 5) list.lastChild.remove();
}

// ── Leaflet Map Interface ──
function initMap() {
    mapInstance = L.map('map').setView([12.9716, 77.5946], 16);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB',
        maxZoom: 19
    }).addTo(mapInstance);

    markerLayer = L.layerGroup().addTo(mapInstance);
    heatLayer = L.layerGroup().addTo(mapInstance);
    updateMap(0, "#10b981");
}

function updateMap(totalUsage, mainRiskColor) {
    if(!mapInstance) return;
    
    markerLayer.clearLayers();
    heatLayer.clearLayers();

    CAMPUS_LOCATIONS.forEach(loc => {
        let bldUsage = totalUsage * loc.baseRatio;
        
        // Calculate individual risk per building based on local capacity
        let bldRatio = bldUsage / loc.capacity;
        let bldRisk = "Low";
        let bldColor = "#10b981"; // green
        
        if (totalUsage === 0) { bldRisk = "N/A"; bldColor = "#94a3b8"; } 
        else if (bldRatio > 0.9) { bldRisk = "High"; bldColor = "#ef4444"; } 
        else if (bldRatio > 0.7) { bldRisk = "Medium"; bldColor = "#f59e0b"; }
        
        // Custom permanent html marker
        let markerHtml = `
            <div class="custom-map-label" style="border-top: 3px solid ${bldColor};">
                <strong>${loc.name}</strong>
                <span class="risk-badge" style="background:${bldColor}; color:#000;">${bldUsage.toLocaleString('en', {maximumFractionDigits:0})}L | ${bldRisk} RISK</span>
            </div>
        `;
        
        let customIcon = L.divIcon({ className: 'custom-leaflet-icon', html: markerHtml, iconSize: [160, 55], iconAnchor: [80, 27] });
        let marker = L.marker([loc.lat, loc.lng], {icon: customIcon});
        markerLayer.addLayer(marker);

        if(totalUsage > 0) {
            let radius = 20 + (bldUsage / 100); 
            let circle = L.circle([loc.lat, loc.lng], {
                color: bldColor, fillColor: bldColor, fillOpacity: 0.4, radius: Math.min(radius, 120) 
            });
            heatLayer.addLayer(circle);
        }
    });
}

// ── Chatbot Interface ──
function handleChat() {
    const input = document.getElementById("chat-input");
    const msg = input.value.trim().toLowerCase();
    if(!msg) return;

    appendChat(input.value.trim(), "user");
    input.value = "";

    setTimeout(() => {
        let reply = "I am mapping Hydrolytix metrics! Try asking about **demand**, **risk**, or **peak day**.";
        if(msg.includes("demand") || msg.includes("usage")) {
            reply = appState.hasPredicted 
                ? `Current predictive forecast stands at **${appState.lastPredictedUsage.toLocaleString()} Litres**.`
                : `Please generate a prediction in the Prediction tab first!`;
        } else if(msg.includes("risk")) {
            reply = appState.hasPredicted
                ? `System evaluation indicates a **${appState.lastRiskLevel}** risk status at this time.`
                : `Awaiting simulation data to calculate risk levels.`;
        } else if(msg.includes("peak")) {
            reply = `Analysis shows the historical peak usage day consistently falls on **${appState.peakDay}**.`;
        }
        appendChat(reply, "ai");
    }, 500);
}

function appendChat(text, type) {
    const container = document.getElementById("chat-messages");
    const div = document.createElement("div");
    div.className = `msg ${type}`;
    let prefix = type === "ai" ? '<strong><i class="fa-solid fa-robot"></i> System AI:</strong>' : '<strong><i class="fa-solid fa-user"></i> You:</strong>';
    text = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>'); 
    div.innerHTML = `${prefix}<p>${text}</p>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// ── Charts Setup ──
function buildCharts(chartData) {
    const usageCtx = document.getElementById("usageChart").getContext("2d");
    if(usageChartInstance) usageChartInstance.destroy();
    
    usageChartInstance = new Chart(usageCtx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: 'Volume (L)', data: chartData.water_usage,
                borderColor: '#00e5ff', backgroundColor: 'rgba(0, 229, 255, 0.1)',
                fill: true, tension: 0.4
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend:{display:false} } }
    });

    const currCtx = document.getElementById("weatherChart").getContext("2d");
    if(weatherChartInstance) weatherChartInstance.destroy();
    
    weatherChartInstance = new Chart(currCtx, {
        type: 'bar',
        data: {
            labels: chartData.dates,
            datasets: [
                { label: 'Usage (L)', data: chartData.water_usage, type: 'line', borderColor: '#0077ff', yAxisID: 'y', tension:0.3 },
                { label: 'Temp (°C)', data: chartData.temperature, backgroundColor: '#8b5cf6', yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            scales: {
                y: { type: 'linear', position: 'left' },
                y1: { type: 'linear', position: 'right', grid:{drawOnChartArea:false} }
            }
        }
    });
}
