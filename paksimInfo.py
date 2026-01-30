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
    <title>🚀 USAMA DHUDDI | Professional SIM Intelligence 🚀</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <style>
        :root {
            --primary: #ff0080;
            --secondary: #00ff9d;
            --dark: #0a0a0f;
            --card: rgba(20, 10, 30, 0.9);
            --glow: 0 0 20px var(--primary);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Rajdhani', sans-serif; background: var(--dark); color: white; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        /* Header */
        .header { background: rgba(15, 10, 25, 0.95); border-bottom: 2px solid var(--primary); padding: 18px 0; }
        .logo { display: flex; align-items: center; gap: 15px; text-decoration: none; }
        .logo-icon { width: 60px; height: 60px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; color: black; font-weight: 900; box-shadow: 0 0 25px var(--primary); animation: logoSpin 3s infinite linear; }
        @keyframes logoSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .logo-text { font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 2rem; background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: 0 0 25px rgba(255, 0, 128, 0.5); }
        
        /* Hero */
        .hero { padding: 80px 0; text-align: center; }
        .hero-title { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; margin-bottom: 15px; background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: 0 0 40px rgba(255, 0, 128, 0.7); animation: titleGlitch 4s infinite; }
        @keyframes titleGlitch { 0%,100% { transform: translateX(0); } 25% { transform: translateX(-5px); text-shadow: 5px 0 var(--secondary), -5px 0 var(--primary); } 50% { transform: translateX(5px); } }
        
        /* Search */
        .search-card { background: rgba(25, 15, 35, 0.9); border: 3px solid var(--primary); border-radius: 25px; padding: 40px; margin: 40px 0; }
        .form-input { width: 100%; padding: 15px; background: rgba(0, 0, 0, 0.5); border: 2px solid var(--primary); border-radius: 12px; color: white; font-size: 1.1rem; margin: 10px 0; }
        .search-btn { width: 100%; padding: 15px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border: none; border-radius: 12px; color: black; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: 900; cursor: pointer; margin-top: 20px; }
        
        /* Results */
        .result-card { background: rgba(0, 0, 0, 0.4); border: 2px solid var(--primary); border-radius: 20px; padding: 20px; margin: 20px 0; }
        .result-field { display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.03); border-radius: 10px; }
        
        /* Footer */
        .footer { background: rgba(15, 10, 25, 0.95); border-top: 2px solid var(--primary); padding: 30px 0; margin-top: 60px; text-align: center; }
        
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .search-card { padding: 20px; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
            <a href="#" class="logo">
                <div class="logo-icon">UD</div>
                <div class="logo-text">USAMA DHUDDI</div>
            </a>
            <div style="padding: 8px 20px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border-radius: 25px; font-weight: 700; color: black;">
                CREATED BY: USAMA DHUDDI
            </div>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <h1 class="hero-title">ADVANCED SIM DATABASE</h1>
            <p style="font-size: 1.3rem; color: var(--secondary); margin-bottom: 40px;">ULTIMATE INTELLIGENCE SYSTEM</p>
            
            <div style="display: flex; justify-content: center; gap: 20px; margin: 40px 0; flex-wrap: wrap;">
                <div style="background: rgba(255,255,255,0.03); border: 2px solid var(--primary); border-radius: 15px; padding: 20px; min-width: 150px;">
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; color: var(--primary);">4.7M+</div>
                    <div style="color: #aaa; font-size: 0.9rem;">RECORDS</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 2px solid var(--primary); border-radius: 15px; padding: 20px; min-width: 150px;">
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; color: var(--primary);">99.8%</div>
                    <div style="color: #aaa; font-size: 0.9rem;">ACCURACY</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 2px solid var(--primary); border-radius: 15px; padding: 20px; min-width: 150px;">
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; color: var(--primary);">24/7</div>
                    <div style="color: #aaa; font-size: 0.9rem;">UPTIME</div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="search-section">
        <div class="container">
            <div class="search-card">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; color: black;">🔍</div>
                    <h2 style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; color: var(--primary);">SIM DATABASE SEARCH</h2>
                    <p style="color: var(--secondary);">Enter mobile number or CNIC to retrieve complete information</p>
                </div>
                
                <form id="searchForm" style="max-width: 600px; margin: 0 auto;">
                    <div>
                        <label style="display: block; margin-bottom: 10px; color: var(--primary); font-weight: 700;">ENTER QUERY</label>
                        <input type="text" id="searchInput" class="form-input" placeholder="03XXXXXXXXX or 13-digit CNIC" required>
                        <p style="color: #777; font-size: 0.9rem; margin-top: 5px;">Enter 11-digit mobile number (03402219264) or CNIC (3520212345671)</p>
                    </div>
                    
                    <button type="submit" class="search-btn">🔍 SEARCH DATABASE</button>
                </form>
                
                <div id="results" style="margin-top: 30px;"></div>
            </div>
        </div>
    </section>
    
    <footer class="footer">
        <div class="container">
            <p>© 2026 USAMA DHUDDI SIM DATABASE</p>
            <p style="color: var(--secondary); font-weight: 700; margin: 10px 0;">Created & Developed by: USAMA DHUDDI</p>
            <p style="color: #777; font-size: 0.9rem;">All Rights Reserved | Professional Intelligence System</p>
        </div>
    </footer>
    
    <script>
        document.getElementById('searchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return;
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--primary);">🔍 Searching database...</div>';
            
            try {
                const response = await fetch('/api/lookup?query=' + encodeURIComponent(query));
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    let html = '<h3 style="color: var(--secondary); margin-bottom: 20px;">📊 SEARCH RESULTS</h3>';
                    data.results.forEach((result, index) => {
                        html += `
                            <div class="result-card">
                                <div class="result-field">
                                    <span style="color: var(--secondary);">📱 MOBILE:</span>
                                    <span>${result.mobile || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span style="color: var(--secondary);">👤 NAME:</span>
                                    <span>${result.name || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span style="color: var(--secondary);">🪪 CNIC:</span>
                                    <span>${result.cnic || 'N/A'}</span>
                                </div>
                                <div class="result-field">
                                    <span style="color: var(--secondary);">📍 ADDRESS:</span>
                                    <span>${result.address || 'N/A'}</span>
                                </div>
                            </div>
                        `;
                    });
                    resultsDiv.innerHTML = html;
                } else {
                    resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--primary);">❌ No data found</div>';
                }
            } catch (error) {
                resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #ff5555;">❌ Search failed</div>';
            }
        });
        
        // Format input
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
    print(f"🚀 Starting USAMA DHUDDI SIM Database on port {port}")
    print(f"👑 Developer: {DEVELOPER}")
    print(f"🌐 Web Interface: http://localhost:{port}")
    print(f"🔗 API Endpoint: http://localhost:{port}/api/lookup?query=03401234567")
    
    app.run(host="0.0.0.0", port=port, debug=False)
