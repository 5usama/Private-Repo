import os
import re
import time
import json
import requests
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# ==================== CONFIGURATION ====================
TARGET_BASE = os.getenv("TARGET_BASE", "https://pakistandatabase.com")
TARGET_PATH = os.getenv("TARGET_PATH", "/databases/sim.php")
MIN_INTERVAL = float(os.getenv("MIN_INTERVAL", "1.0"))
LAST_CALL = {"ts": 0.0}
DEVELOPER = os.getenv("DEVELOPER", "USAMA DHUDDI")

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Usama's Database  --  Sim Owner Details</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            transition: all 0.3s ease;
        }
        
        body.light-theme {
            background-color: #f8f9fa;
            color: #333;
        }
        
        body.dark-theme {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Header */
        .header {
            padding: 20px 0;
            border-bottom: 1px solid;
            background-color: inherit;
        }
        
        .light-theme .header {
            border-bottom-color: #e0e0e0;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .dark-theme .header {
            border-bottom-color: #333;
            background-color: #1e1e1e;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: #007bff;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 18px;
        }
        
        .light-theme .logo-icon {
            background: #007bff;
        }
        
        .dark-theme .logo-icon {
            background: #0d6efd;
        }
        
        .logo-text {
            font-size: 22px;
            font-weight: 600;
        }
        
        .light-theme .logo-text {
            color: #007bff;
        }
        
        .dark-theme .logo-text {
            color: #0d6efd;
        }
        
        .theme-switch {
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            border: 1px solid;
            transition: all 0.3s ease;
            background: transparent;
        }
        
        .light-theme .theme-switch {
            border-color: #ddd;
            color: #666;
        }
        
        .light-theme .theme-switch:hover {
            background-color: #f8f9fa;
        }
        
        .dark-theme .theme-switch {
            border-color: #444;
            color: #aaa;
        }
        
        .dark-theme .theme-switch:hover {
            background-color: #2d2d2d;
        }
        
        /* Hero Section */
        .hero {
            padding: 60px 0 40px;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .light-theme .hero h1 {
            color: #2c3e50;
        }
        
        .dark-theme .hero h1 {
            color: #e0e0e0;
        }
        
        .hero p {
            font-size: 18px;
            color: #666;
            max-width: 600px;
            margin: 0 auto 40px;
        }
        
        .dark-theme .hero p {
            color: #aaa;
        }
        
        /* Stats */
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 40px 0;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 25px;
            border-radius: 10px;
            min-width: 150px;
        }
        
        .light-theme .stat-item {
            background: white;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .dark-theme .stat-item {
            background: #1e1e1e;
            border: 1px solid #333;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .light-theme .stat-value {
            color: #007bff;
        }
        
        .dark-theme .stat-value {
            color: #0d6efd;
        }
        
        .stat-label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .dark-theme .stat-label {
            color: #888;
        }
        
        /* Search Section */
        .search-section {
            padding: 40px 0;
        }
        
        .search-card {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            border-radius: 12px;
        }
        
        .light-theme .search-card {
            background: white;
            border: 1px solid #e0e0e0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        
        .dark-theme .search-card {
            background: #1e1e1e;
            border: 1px solid #333;
        }
        
        .search-header {
            text-align: center;
            margin-bottom: 35px;
        }
        
        .search-header h2 {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .light-theme .search-header h2 {
            color: #2c3e50;
        }
        
        .dark-theme .search-header h2 {
            color: #e0e0e0;
        }
        
        .search-header p {
            color: #666;
            font-size: 16px;
        }
        
        .dark-theme .search-header p {
            color: #aaa;
        }
        
        /* Form */
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 16px;
        }
        
        .light-theme .form-label {
            color: #444;
        }
        
        .dark-theme .form-label {
            color: #ccc;
        }
        
        .form-input {
            width: 100%;
            padding: 14px 18px;
            font-size: 16px;
            border: 2px solid;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .light-theme .form-input {
            background: white;
            border-color: #ddd;
            color: #333;
        }
        
        .light-theme .form-input:focus {
            border-color: #007bff;
            outline: none;
            box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
        }
        
        .dark-theme .form-input {
            background: #2d2d2d;
            border-color: #444;
            color: #e0e0e0;
        }
        
        .dark-theme .form-input:focus {
            border-color: #0d6efd;
            outline: none;
            box-shadow: 0 0 0 3px rgba(13,110,253,0.15);
        }
        
        .form-hint {
            font-size: 14px;
            margin-top: 8px;
        }
        
        .light-theme .form-hint {
            color: #666;
        }
        
        .dark-theme .form-hint {
            color: #888;
        }
        
        .search-btn {
            width: 100%;
            padding: 16px;
            font-size: 17px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .light-theme .search-btn {
            background: #007bff;
            color: white;
        }
        
        .light-theme .search-btn:hover {
            background: #0056b3;
        }
        
        .dark-theme .search-btn {
            background: #0d6efd;
            color: white;
        }
        
        .dark-theme .search-btn:hover {
            background: #0b5ed7;
        }
        
        /* Results */
        #results {
            margin-top: 40px;
        }
        
        .results-header {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid;
        }
        
        .light-theme .results-header {
            color: #2c3e50;
            border-bottom-color: #e0e0e0;
        }
        
        .dark-theme .results-header {
            color: #e0e0e0;
            border-bottom-color: #333;
        }
        
        .result-card {
            margin-bottom: 20px;
            padding: 25px;
            border-radius: 10px;
        }
        
        .light-theme .result-card {
            background: white;
            border: 1px solid #e0e0e0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }
        
        .dark-theme .result-card {
            background: #1e1e1e;
            border: 1px solid #333;
        }
        
        .result-field {
            display: flex;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid;
        }
        
        .light-theme .result-field {
            border-bottom-color: #f0f0f0;
        }
        
        .dark-theme .result-field {
            border-bottom-color: #333;
        }
        
        .result-field:last-child {
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }
        
        .field-label {
            width: 120px;
            font-weight: 600;
            color: #666;
        }
        
        .dark-theme .field-label {
            color: #aaa;
        }
        
        .field-value {
            flex: 1;
            color: #333;
        }
        
        .dark-theme .field-value {
            color: #e0e0e0;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .dark-theme .loading {
            color: #aaa;
        }
        
        .error {
            text-align: center;
            padding: 40px;
            color: #dc3545;
            background: #f8d7da;
            border-radius: 8px;
            border: 1px solid #f5c6cb;
        }
        
        .dark-theme .error {
            color: #f8d7da;
            background: #842029;
            border-color: #6a1a21;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        .dark-theme .no-results {
            color: #aaa;
            background: #2d2d2d;
            border-color: #333;
        }
        
        /* Footer */
        .footer {
            padding: 40px 0;
            margin-top: 60px;
            text-align: center;
            border-top: 1px solid;
        }
        
        .light-theme .footer {
            background: white;
            border-top-color: #e0e0e0;
            color: #666;
        }
        
        .dark-theme .footer {
            background: #1e1e1e;
            border-top-color: #333;
            color: #888;
        }
        
        .footer p {
            margin-bottom: 10px;
        }
        
        .developer {
            font-weight: 600;
            margin: 15px 0;
            color: #007bff;
        }
        
        .dark-theme .developer {
            color: #0d6efd;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 28px;
            }
            
            .search-card {
                padding: 25px 20px;
            }
            
            .stat-item {
                min-width: 120px;
                padding: 20px;
            }
            
            .result-card {
                padding: 20px;
            }
            
            .field-label {
                width: 100px;
            }
        }
    </style>
</head>
<body class="light-theme">
    <header class="header">
        <div class="container">
            <div class="header-content">
                <a href="#" class="logo">
                    <div class="logo-icon">UD</div>
                    <div class="logo-text">Usama's Database</div>
                </a>
                <button class="theme-switch" id="themeToggle">
                    <i class="fas fa-moon"></i> Dark Mode
                </button>
            </div>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <h1>Professional SIM Database Lookup</h1>
            <p>Accurate and reliable SIM information retrieval service for Pakistan</p>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">4.7M+</div>
                    <div class="stat-label">Records</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">99.8%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">24/7</div>
                    <div class="stat-label">Service</div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="search-section">
        <div class="container">
            <div class="search-card">
                <div class="search-header">
                    <h2>Search Database</h2>
                    <p>Enter mobile number or CNIC to retrieve complete information</p>
                </div>
                
                <form id="searchForm">
                    <div class="form-group">
                        <label class="form-label">Search Query</label>
                        <input type="text" id="searchInput" class="form-input" placeholder="03401234567 or 3520212345671" required>
                        <div class="form-hint">Enter 11-digit mobile number (03402219264) or CNIC (3520212345671)</div>
                    </div>
                    
                    <button type="submit" class="search-btn">
                        <i class="fas fa-search"></i> Search Database
                    </button>
                </form>
                
                <div id="results"></div>
            </div>
        </div>
    </section>
    
    <footer class="footer">
        <div class="container">
            <p>© 2024 SIM Database Lookup Service</p>
            <p class="developer">Developed by: USAMA DHUDDI</p>
            <p>All Rights Reserved | Professional Information System</p>
        </div>
    </footer>
    
    <script>
        // Theme Toggle
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;
        
        themeToggle.addEventListener('click', () => {
            if (body.classList.contains('light-theme')) {
                body.classList.remove('light-theme');
                body.classList.add('dark-theme');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
            } else {
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
                themeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
            }
        });
        
        // Search Form
        document.getElementById('searchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return;
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Searching database...</div>';
            
            try {
                const response = await fetch('/api/lookup?query=' + encodeURIComponent(query));
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    let html = '<h3 class="results-header">Search Results</h3>';
                    data.results.forEach((result, index) => {
                        html += `
                            <div class="result-card">
                                <div class="result-field">
                                    <span class="field-label">Mobile:</span>
                                    <span class="field-value">${result.mobile || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span class="field-label">Name:</span>
                                    <span class="field-value">${result.name || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span class="field-label">CNIC:</span>
                                    <span class="field-value">${result.cnic || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span class="field-label">Address:</span>
                                    <span class="field-value">${result.address || 'N/A'}</span>
                                </div>
                            </div>
                        `;
                    });
                    resultsDiv.innerHTML = html;
                } else {
                    resultsDiv.innerHTML = '<div class="no-results">No matching records found in the database</div>';
                }
            } catch (error) {
                resultsDiv.innerHTML = '<div class="error">Search failed. Please try again later.</div>';
            }
        });
        
        // Format input - only allow numbers
        document.getElementById('searchInput').addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    </script>
</body>
</html>
'''

# ==================== HELPER FUNCTIONS ====================
def is_mobile(value: str) -> bool:
    return bool(re.fullmatch(r"92\d{10}", value))

def is_local_mobile(value: str) -> bool:
    return bool(re.fullmatch(r"03\d{9}", value))

def is_cnic(value: str) -> bool:
    return bool(re.fullmatch(r"\d{13}", value))

def normalize_mobile(value: str) -> str:
    value = value.strip()
    if is_mobile(value):
        return value
    if is_local_mobile(value):
        return "92" + value[1:]
    return value

def classify_query(value: str):
    v = value.strip()
    if is_cnic(v):
        return "cnic", v

    normalized = normalize_mobile(v)
    if is_mobile(normalized):
        return "mobile", normalized

    raise ValueError(
        "Invalid query. Use CNIC (13 digits) or mobile (03XXXXXXXXX / 92XXXXXXXXXX)."
    )

def rate_limit_wait():
    now = time.time()
    elapsed = now - LAST_CALL["ts"]
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    LAST_CALL["ts"] = time.time()

def fetch_upstream(query_value: str):
    rate_limit_wait()

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": TARGET_BASE.rstrip("/") + "/",
        "Accept-Language": "en-US,en;q=0.9",
    }

    url = TARGET_BASE.rstrip("/") + TARGET_PATH
    data = {"search_query": query_value}

    resp = session.post(url, headers=headers, data=data, timeout=20)
    resp.raise_for_status()
    return resp.text

def parse_table(html: str):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "api-response"}) or soup.find("table")
    if not table:
        return []

    tbody = table.find("tbody")
    if not tbody:
        return []

    results = []
    seen = set()

    for tr in tbody.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        mobile = cols[0] if len(cols) > 0 else None
        name = cols[1] if len(cols) > 1 else None
        cnic = cols[2] if len(cols) > 2 else None
        address = cols[3] if len(cols) > 3 else None

        key = (mobile, cnic, name)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "mobile": mobile,
            "name": name,
            "cnic": cnic,
            "address": address
        })

    return results

def make_response_object(query, qtype, results):
    return {
        "query": query,
        "query_type": qtype,
        "results_count": len(results),
        "results": results,
        "developer": DEVELOPER,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def respond_json(obj, pretty=False):
    text = json.dumps(obj, indent=2 if pretty else None, ensure_ascii=False)
    return Response(text, mimetype="application/json; charset=utf-8")

# ==================== ROUTES ====================
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/lookup", methods=["GET"])
def api_lookup_get():
    q = request.args.get("query") or request.args.get("q") or request.args.get("value")
    pretty = request.args.get("pretty") in ("1", "true", "True")

    if not q:
        return respond_json({"error": "Use ?query=<mobile or cnic>", "developer": DEVELOPER}, pretty), 400

    try:
        qtype, normalized = classify_query(q)
        html = fetch_upstream(normalized)
        results = parse_table(html)
        return respond_json(make_response_object(normalized, qtype, results), pretty)
    except Exception as e:
        return respond_json({"error": "Fetch failed", "detail": str(e), "developer": DEVELOPER}, pretty), 500

@app.route("/health", methods=["GET"])
def health():
    return respond_json({"status": "ok", "developer": DEVELOPER, "service": "SIM Database API"})

# ==================== MAIN ====================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"🚀 Starting SIM Database on port {port}")
    print(f"👑 Developer: {DEVELOPER}")
    print(f"🌐 Web Interface: http://localhost:{port}")
    print(f"🔗 API Endpoint: http://localhost:{port}/api/lookup?query=03401234567")
    
    app.run(host="0.0.0.0", port=port, debug=False)
