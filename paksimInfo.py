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
        /* ====== VARIABLES ====== */
        :root {
            --primary: #00ff9d;      /* Neon Green */
            --secondary: #ff0080;    /* Hot Pink */
            --accent: #0095ff;       /* Blue */
            --dark: #0a0a0f;
            --darker: #050508;
            --card: rgba(20, 25, 40, 0.85);
            --glow: 0 0 20px var(--primary);
            --pink-glow: 0 0 20px var(--secondary);
            --blue-glow: 0 0 20px var(--accent);
        }

        /* ====== RESET & BASE ====== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            background: var(--dark);
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.6;
        }

        /* ====== ANIMATED BACKGROUND ====== */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            background: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 157, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255, 0, 128, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(0, 149, 255, 0.05) 0%, transparent 50%);
        }

        .matrix-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 157, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 157, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: -1;
            pointer-events: none;
            animation: gridMove 20s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: translateY(0) translateX(0); }
            100% { transform: translateY(50px) translateX(50px); }
        }

        /* ====== CONTAINER ====== */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* ====== HEADER - BUBBLE EFFECT ====== */
        .header {
            background: rgba(10, 10, 20, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid transparent;
            padding: 15px 0;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
            box-shadow: 0 5px 30px rgba(0, 0, 0, 0.5);
            border-image: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent)) 1;
            animation: borderGlow 3s infinite alternate;
        }

        @keyframes borderGlow {
            0% { box-shadow: 0 5px 20px rgba(0, 255, 157, 0.3); }
            50% { box-shadow: 0 5px 30px rgba(255, 0, 128, 0.4); }
            100% { box-shadow: 0 5px 25px rgba(0, 149, 255, 0.3); }
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* LOGO - 3D BUBBLE */
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
            position: relative;
        }

        .logo-bubble {
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: black;
            font-weight: 900;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 0 30px var(--primary),
                inset 0 5px 10px rgba(255, 255, 255, 0.3);
            animation: bubbleFloat 6s ease-in-out infinite;
            transform-style: preserve-3d;
        }

        .logo-bubble::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            border-radius: 50%;
            animation: shine 3s infinite;
        }

        @keyframes bubbleFloat {
            0%, 100% { 
                transform: translateY(0) rotate(0deg);
                box-shadow: 0 0 30px var(--primary);
            }
            50% { 
                transform: translateY(-15px) rotate(5deg);
                box-shadow: 0 10px 40px var(--secondary);
            }
        }

        @keyframes shine {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .logo-text {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 2.2rem;
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 157, 0.5);
            letter-spacing: 2px;
            position: relative;
        }

        .logo-text::after {
            content: 'SIM INTELLIGENCE';
            position: absolute;
            bottom: -18px;
            left: 0;
            font-size: 0.7rem;
            color: var(--accent);
            letter-spacing: 3px;
            text-transform: uppercase;
            font-weight: 700;
        }

        /* HEADER BUTTONS - BUBBLE STYLE */
        .header-controls {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .bubble-btn {
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--primary);
            border-radius: 50%;
            color: var(--primary);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
        }

        .bubble-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: var(--primary);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .bubble-btn:hover::before {
            width: 100px;
            height: 100px;
        }

        .bubble-btn:hover {
            color: black;
            transform: scale(1.1) rotate(90deg);
            box-shadow: var(--glow);
            border-color: var(--secondary);
        }

        .bubble-btn i {
            position: relative;
            z-index: 1;
        }

        .owner-badge {
            padding: 12px 25px;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            border-radius: 30px;
            font-weight: 900;
            color: black;
            font-size: 0.9rem;
            letter-spacing: 1px;
            box-shadow: 0 0 25px rgba(0, 255, 157, 0.5);
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .owner-badge:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 40px rgba(255, 0, 128, 0.6);
            background: linear-gradient(45deg, var(--secondary), var(--primary));
        }

        /* ====== HERO SECTION ====== */
        .hero {
            padding: 150px 0 80px;
            text-align: center;
            position: relative;
        }

        .hero-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 4.5rem;
            font-weight: 900;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 50px rgba(0, 255, 157, 0.7);
            letter-spacing: 3px;
            animation: titleGlitch 5s infinite;
            position: relative;
            display: inline-block;
        }

        .hero-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            animation: lineGlow 2s infinite;
        }

        @keyframes titleGlitch {
            0%, 100% { 
                transform: translateX(0);
                text-shadow: 0 0 50px rgba(0, 255, 157, 0.7);
            }
            25% { 
                transform: translateX(-5px);
                text-shadow: 5px 0 var(--secondary), -5px 0 var(--accent);
            }
            50% { 
                transform: translateX(5px);
                text-shadow: -5px 0 var(--primary), 5px 0 var(--secondary);
            }
            75% { 
                transform: translateX(-3px);
                text-shadow: 3px 0 var(--accent), -3px 0 var(--primary);
            }
        }

        @keyframes lineGlow {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }

        .hero-subtitle {
            font-size: 1.5rem;
            color: var(--accent);
            margin-bottom: 30px;
            text-shadow: 0 0 15px rgba(0, 149, 255, 0.5);
            font-weight: 600;
        }

        .hero-tagline {
            font-size: 1.2rem;
            color: #aaa;
            max-width: 800px;
            margin: 0 auto 50px;
            line-height: 1.8;
        }

        /* STATS - BUBBLE CARDS */
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 50px 0;
            flex-wrap: wrap;
        }

        .stat-bubble {
            background: var(--card);
            backdrop-filter: blur(10px);
            border: 2px solid transparent;
            border-radius: 25px;
            padding: 30px;
            min-width: 200px;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .stat-bubble::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
            border-radius: 25px;
            z-index: -1;
            opacity: 0.5;
            filter: blur(15px);
            animation: borderRotate 4s linear infinite;
        }

        @keyframes borderRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .stat-bubble:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: var(--glow);
        }

        .stat-bubble:hover::before {
            opacity: 0.8;
            filter: blur(20px);
        }

        .stat-number {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: block;
            line-height: 1;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }

        /* ====== SEARCH SECTION ====== */
        .search-section {
            margin: 60px 0;
        }

        .search-card {
            background: var(--card);
            backdrop-filter: blur(20px);
            border: 2px solid transparent;
            border-radius: 30px;
            padding: 60px;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .search-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                from 0deg,
                transparent,
                var(--primary),
                var(--secondary),
                var(--accent),
                transparent 30%
            );
            animation: borderSpin 6s linear infinite;
            z-index: 1;
        }

        @keyframes borderSpin {
            100% { transform: rotate(360deg); }
        }

        .search-card > * {
            position: relative;
            z-index: 2;
        }

        .search-header {
            text-align: center;
            margin-bottom: 50px;
        }

        .search-icon {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
            color: black;
            box-shadow: 
                0 0 60px var(--primary),
                inset 0 5px 15px rgba(255, 255, 255, 0.3);
            animation: iconPulse 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        .search-icon::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            background: radial-gradient(circle, transparent 60%, rgba(255, 255, 255, 0.1) 100%);
            border-radius: 50%;
            animation: ripple 2s infinite;
        }

        @keyframes iconPulse {
            0%, 100% { 
                transform: scale(1) rotate(0deg);
                box-shadow: 0 0 60px var(--primary);
            }
            50% { 
                transform: scale(1.1) rotate(180deg);
                box-shadow: 0 0 80px var(--secondary);
            }
        }

        @keyframes ripple {
            0% { transform: scale(0.8); opacity: 1; }
            100% { transform: scale(1.5); opacity: 0; }
        }

        .search-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 157, 0.5);
        }

        .search-subtitle {
            font-size: 1.3rem;
            color: var(--accent);
            opacity: 0.9;
            font-weight: 600;
        }

        /* SEARCH FORM */
        .search-form {
            max-width: 700px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 30px;
        }

        .form-label {
            display: block;
            margin-bottom: 15px;
            color: var(--primary);
            font-weight: 900;
            font-size: 1.2rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
        }

        .input-with-icon {
            position: relative;
        }

        .input-icon {
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--primary);
            font-size: 1.5rem;
            z-index: 1;
        }

        .form-input {
            width: 100%;
            padding: 25px 25px 25px 70px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid transparent;
            border-radius: 20px;
            color: white;
            font-size: 1.2rem;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            transition: all 0.3s;
            outline: none;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .form-input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        .form-input:focus {
            border-image: linear-gradient(45deg, var(--primary), var(--secondary)) 1;
            box-shadow: 
                0 0 40px rgba(0, 255, 157, 0.3),
                inset 0 0 20px rgba(0, 255, 157, 0.1);
            background: rgba(0, 0, 0, 0.5);
            transform: translateY(-2px);
        }

        .form-hint {
            display: block;
            margin-top: 10px;
            color: #777;
            font-size: 0.9rem;
            padding-left: 10px;
        }

        /* SEARCH BUTTON - BUBBLE EFFECT */
        .search-btn {
            width: 100%;
            padding: 25px;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 20px;
            color: black;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            font-weight: 900;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 30px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0, 255, 157, 0.3);
        }

        .search-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: 0.6s;
        }

        .search-btn:hover::before {
            left: 100%;
        }

        .search-btn:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 
                0 20px 60px rgba(255, 0, 128, 0.5),
                0 0 100px rgba(0, 255, 157, 0.3);
            background: linear-gradient(45deg, var(--secondary), var(--primary));
            letter-spacing: 4px;
        }

        .search-btn:active {
            transform: translateY(0) scale(0.98);
        }

        .search-btn i {
            margin-right: 10px;
            font-size: 1.6rem;
        }

        /* ====== RESULTS SECTION ====== */
        .results-section {
            margin: 60px 0;
            display: none;
        }

        .results-card {
            background: var(--card);
            backdrop-filter: blur(20px);
            border: 2px solid transparent;
            border-radius: 30px;
            padding: 50px;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .results-card::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--accent), var(--primary), var(--secondary));
            border-radius: 30px;
            z-index: -1;
            opacity: 0.3;
            filter: blur(20px);
            animation: borderPulse 3s infinite alternate;
        }

        @keyframes borderPulse {
            0% { opacity: 0.3; filter: blur(20px); }
            100% { opacity: 0.5; filter: blur(30px); }
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 25px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }

        .results-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            background: linear-gradient(45deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
        }

        .results-meta {
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .results-count {
            padding: 12px 25px;
            background: rgba(0, 255, 157, 0.1);
            border: 2px solid var(--primary);
            border-radius: 25px;
            font-weight: 900;
            color: var(--primary);
            font-size: 1.1rem;
            letter-spacing: 1px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
        }

        .results-content {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }

        /* RESULT CARD - BUBBLE STYLE */
        .result-card {
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid transparent;
            border-radius: 25px;
            padding: 30px;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .result-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 8px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
            border-radius: 4px 0 0 4px;
        }

        .result-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 
                var(--glow),
                0 15px 40px rgba(0, 0, 0, 0.4);
            border-image: linear-gradient(45deg, var(--primary), var(--secondary)) 1;
        }

        .result-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            transition: all 0.3s;
        }

        .result-field:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(10px);
            border-left: 3px solid var(--primary);
        }

        .field-label {
            color: var(--primary);
            font-weight: 900;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .field-label i {
            font-size: 1.2rem;
            color: var(--secondary);
        }

        .field-value {
            color: white;
            font-weight: 700;
            text-align: right;
            max-width: 60%;
            word-break: break-word;
            font-size: 1.1rem;
        }

        /* LOADING ANIMATION */
        .loading {
            text-align: center;
            padding: 80px;
            grid-column: 1 / -1;
        }

        .loading-spinner {
            width: 80px;
            height: 80px;
            border: 5px solid rgba(255, 255, 255, 0.1);
            border-top-color: var(--primary);
            border-radius: 50%;
            margin: 0 auto 25px;
            animation: spin 1s linear infinite;
            position: relative;
        }

        .loading-spinner::before {
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            border: 5px solid transparent;
            border-top-color: var(--secondary);
            border-radius: 50%;
            animation: spin 1.5s linear infinite reverse;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* ====== FOOTER ====== */
        .footer {
            background: rgba(10, 10, 20, 0.95);
            border-top: 2px solid transparent;
            padding: 50px 0;
            margin-top: 80px;
            position: relative;
            overflow: hidden;
        }

        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
            animation: footerGlow 3s infinite alternate;
        }

        @keyframes footerGlow {
            0% { box-shadow: 0 0 20px var(--primary); }
            50% { box-shadow: 0 0 30px var(--secondary); }
            100% { box-shadow: 0 0 25px var(--accent); }
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 40px;
        }

        .footer-logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .footer-logo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(45deg, var(--primary), var(--accent));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: black;
            font-weight: 900;
            box-shadow: 0 0 20px var(--primary);
        }

        .footer-logo-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: var(--primary);
            font-weight: 900;
        }

        .copyright {
            color: #777;
            text-align: center;
            flex: 1;
        }

        .owner-credits {
            color: var(--secondary);
            font-weight: 900;
            font-size: 1.3rem;
            margin: 15px 0;
            text-shadow: 0 0 10px rgba(255, 0, 128, 0.5);
        }

        .footer-links {
            display: flex;
            gap: 15px;
        }

        .footer-link {
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--primary);
            border-radius: 50%;
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 1.2rem;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
        }

        .footer-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--primary);
            transform: scale(0);
            border-radius: 50%;
            transition: transform 0.3s;
        }

        .footer-link:hover::before {
            transform: scale(1);
        }

        .footer-link:hover {
            color: black;
            transform: translateY(-5px) rotate(15deg);
            box-shadow: var(--glow);
            border-color: var(--secondary);
        }

        .footer-link i {
            position: relative;
            z-index: 1;
        }

        /* ====== RESPONSIVE DESIGN ====== */
        @media (max-width: 992px) {
            .hero-title { font-size: 3.5rem; }
            .search-card { padding: 40px 30px; }
            .results-content { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
            .hero-title { font-size: 2.8rem; }
            .search-card { padding: 30px 20px; }
            .results-content { grid-template-columns: 1fr; }
            .footer-content { flex-direction: column; text-align: center; }
            .stats { gap: 20px; }
            .stat-bubble { min-width: 160px; padding: 25px; }
            .header-controls { flex-wrap: wrap; justify-content: center; }
            .logo-text { font-size: 1.8rem; }
        }

        @media (max-width: 480px) {
            .hero-title { font-size: 2.2rem; }
            .search-title { font-size: 2.2rem; }
            .stat-bubble { min-width: 140px; padding: 20px; }
            .stat-number { font-size: 2.8rem; }
            .logo-bubble { width: 50px; height: 50px; font-size: 22px; }
            .logo-text { font-size: 1.5rem; }
        }

        /* ====== SCROLLBAR STYLING ====== */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: var(--darker);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--primary), var(--secondary));
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(var(--secondary), var(--primary));
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="matrix-grid"></div>
    
    <!-- HEADER -->
    <header class="header">
        <div class="container header-content">
            <a href="#" class="logo">
                <div class="logo-bubble">UD</div>
                <div class="logo-text">USAMA DHUDDI</div>
            </a>
            
            <div class="header-controls">
                <div class="owner-badge">
                    <i class="fas fa-crown"></i> CREATED BY: USAMA DHUDDI
                </div>
                
                <button class="bubble-btn" id="themeToggle" title="Toggle Theme">
                    <i class="fas fa-adjust"></i>
                </button>
                
                <button class="bubble-btn" id="menuToggle" title="Menu">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
        </div>
    </header>
    
    <!-- HERO SECTION -->
    <section class="hero">
        <div class="container">
            <h1 class="hero-title">ADVANCED SIM DATABASE</h1>
            <p class="hero-subtitle">ULTIMATE INTELLIGENCE SYSTEM</p>
            
            <p class="hero-tagline">
                Professional SIM information retrieval system with 4.7M+ records database. 
                Search by mobile number or CNIC for complete verified information.
            </p>
            
            <div class="stats">
                <div class="stat-bubble">
                    <span class="stat-number">4.7M+</span>
                    <span class="stat-label">RECORDS</span>
                </div>
                
                <div class="stat-bubble">
                    <span class="stat-number">99.8%</span>
                    <span class="stat-label">ACCURACY</span>
                </div>
                
                <div class="stat-bubble">
                    <span class="stat-number">24/7</span>
                    <span class="stat-label">UPTIME</span>
                </div>
                
                <div class="stat-bubble">
                    <span class="stat-number">0.5s</span>
                    <span class="stat-label">RESPONSE</span>
                </div>
            </div>
        </div>
    </section>
    
    <!-- SEARCH SECTION -->
    <section class="search-section">
        <div class="container">
            <div class="search-card">
                <div class="search-header">
                    <div class="search-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    
                    <h2 class="search-title">SIM DATABASE SEARCH</h2>
                    <p class="search-subtitle">Enter mobile number or CNIC to retrieve complete information</p>
                </div>
                
                <form id="searchForm" class="search-form">
                    <div class="form-group">
                        <label class="form-label">ENTER QUERY</label>
                        
                        <div class="input-with-icon">
                            <i class="fas fa-search input-icon"></i>
                            <input type="text" id="searchInput" class="form-input" 
                                   placeholder="03XXXXXXXXX or 13-digit CNIC" 
                                   maxlength="20" 
                                   required
                                   autocomplete="off">
                        </div>
                        
                        <span class="form-hint">
                            <i class="fas fa-info-circle"></i>
                            Enter 11-digit mobile number (03402219264) or CNIC (3520212345671)
                        </span>
                    </div>
                    
                    <button type="submit" class="search-btn">
                        <i class="fas fa-database"></i> SEARCH DATABASE
                    </button>
                </form>
            </div>
        </div>
    </section>
    
    <!-- RESULTS SECTION -->
    <section id="resultsSection" class="results-section">
        <div class="container">
            <div class="results-card">
                <div class="results-header">
                    <h3 class="results-title">
                        <i class="fas fa-search"></i> SEARCH RESULTS
                    </h3>
                    
                    <div class="results-meta">
                        <div class="results-count" id="resultsCount">0 RECORDS</div>
                        
                        <button class="bubble-btn" onclick="clearResults()" title="Clear Results">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                
                <div id="resultsContent" class="results-content">
                    <!-- Results will be inserted here by JavaScript -->
                </div>
            </div>
        </div>
    </section>
    
    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <div class="footer-logo-icon">UD</div>
                    <div class="footer-logo-text">USAMA DHUDDI</div>
                </div>
                
                <div class="copyright">
                    <p>© 2026 USAMA DHUDDI SIM DATABASE</p>
                    <p class="owner-credits">Created & Developed by: USAMA DHUDDI</p>
                    <p style="margin-top: 10px; font-size: 0.9rem; color: #aaa;">
                        <i class="fas fa-shield-alt"></i> All Rights Reserved | Professional Intelligence System
                    </p>
                </div>
                
                <div class="footer-links">
                    <a href="#" class="footer-link" title="WhatsApp">
                        <i class="fab fa-whatsapp"></i>
                    </a>
                    
                    <a href="#" class="footer-link" title="Telegram">
                        <i class="fab fa-telegram"></i>
                    </a>
                    
                    <a href="#" class="footer-link" title="Email">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
            </div>
        </div>
    </footer>

    <!-- JAVASCRIPT -->
    <script>
        // Theme Toggle
        document.getElementById('themeToggle').addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-sun');
            icon.classList.toggle('fa-moon');
            
            // Show notification
            showNotification('Theme changed!', 'success');
        });
        
        // Menu Toggle
        document.getElementById('menuToggle').addEventListener('click', function() {
            showNotification('Menu functionality would go here!', 'info');
        });
        
        // Search Form Handler
        document.getElementById('searchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const input = document.getElementById('searchInput');
            const query = input.value.trim();
            
            if (!query) {
                showNotification('Please enter a mobile number or CNIC', 'error');
                return;
            }
            
            // Validate input
            const cleanQuery = query.replace(/\D/g, '');
            if (cleanQuery.length < 10 || cleanQuery.length > 13) {
                showNotification('Please enter valid 11-digit number or 13-digit CNIC', 'error');
                return;
            }
            
            // Show results section
            const resultsSection = document.getElementById('resultsSection');
            const resultsContent = document.getElementById('resultsContent');
            const resultsCount = document.getElementById('resultsCount');
            
            resultsSection.style.display = 'block';
            resultsContent.innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    <p style="color: var(--primary); font-size: 1.5rem; font-weight: 900; margin: 20px 0;">
                        SEARCHING DATABASE...
                    </p>
                    <p style="color: var(--accent); font-size: 1.1rem;">
                        <i class="fas fa-bolt"></i> Query: ${cleanQuery}<br>
                        <i class="fas fa-database"></i> Scanning 4.7M+ records...
                    </p>
                </div>
            `;
            
            // Scroll to results
            resultsSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
            
            // Simulate API call (Replace with actual API call)
            setTimeout(() => {
                // Mock data for demonstration
                const mockData = {
                    query: cleanQuery,
                    query_type: cleanQuery.length === 13 ? 'CNIC' : 'Mobile',
                    results_count: 1,
                    results: [{
                        mobile: cleanQuery.length === 13 ? '03001234567' : '92' + cleanQuery.substring(1),
                        name: 'USAMA DHUDDI',
                        cnic: cleanQuery.length === 13 ? cleanQuery : '35202-1234567-1',
                        address: 'Professional SIM Database System, Pakistan',
                        network: 'Jazz/Warid',
                        status: 'ACTIVE',
                        type: 'Prepaid'
                    }]
                };
                
                // Display results
                displayResults(mockData);
                showNotification('Search completed successfully!', 'success');
                
            }, 2000); // 2 second delay for demo
        });
        
        // Input formatting
        document.getElementById('searchInput').addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            
            // Auto-format
            const value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                this.value = value;
            } else if (value.length === 13) {
                // CNIC format
                this.value = value.replace(/(\d{5})(\d{7})(\d{1})/, '$1-$2-$3');
            }
        });
        
        // Display Results Function
        function displayResults(data) {
            const resultsContent = document.getElementById('resultsContent');
            const resultsCount = document.getElementById('resultsCount');
            
            resultsCount.textContent = `${data.results_count} RECORDS FOUND`;
            
            let html = '';
            
            data.results.forEach((result, index) => {
                html += `
                    <div class="result-card">
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-hashtag"></i> RECORD
                            </span>
                            <span class="field-value">#${index + 1}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-mobile-alt"></i> MOBILE
                            </span>
                            <span class="field-value">${result.mobile || 'N/A'}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-user"></i> NAME
                            </span>
                            <span class="field-value">${result.name || 'N/A'}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-id-card"></i> CNIC
                            </span>
                            <span class="field-value">${result.cnic || 'N/A'}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-map-marker-alt"></i> ADDRESS
                            </span>
                            <span class="field-value">${result.address || 'N/A'}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-signal"></i> NETWORK
                            </span>
                            <span class="field-value">${result.network || 'N/A'}</span>
                        </div>
                        
                        <div class="result-field">
                            <span class="field-label">
                                <i class="fas fa-check-circle"></i> STATUS
                            </span>
                            <span class="field-value" style="color: var(--primary); font-weight: 900;">
                                ${result.status || 'ACTIVE'}
                            </span>
                        </div>
                    </div>
                `;
            });
            
            resultsContent.innerHTML = html;
        }
        
        // Clear Results
        function clearResults() {
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('searchInput').value = '';
            document.getElementById('searchInput').focus();
            showNotification('Results cleared!', 'info');
        }
        
        // Notification System
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            
            const colors = {
                success: 'var(--primary)',
                error: 'var(--secondary)',
                info: 'var(--accent)',
                warning: '#ffaa00'
            };
            
            notification.style.cssText = `
                position: fixed;
                top: 100px;
                right: 20px;
                background: ${colors[type]};
                color: black;
                padding: 20px 25px;
                border-radius: 20px;
                z-index: 9999;
                font-weight: 900;
                font-size: 1rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                transform: translateX(120%);
                transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                max-width: 350px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                gap: 15px;
            `;
            
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                info: 'fa-info-circle',
                warning: 'fa-exclamation-triangle'
            };
            
            notification.innerHTML = `
                <i class="fas ${icons[type]}" style="font-size: 1.5rem;"></i>
                <span>${message}</span>
            `;
            
            document.body.appendChild(notification);
            
            // Animate in
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 10);
            
            // Remove after 4 seconds
            setTimeout(() => {
                notification.style.transform = 'translateX(120%)';
                setTimeout(() => {
                    if (notification.parentNode) {
                        document.body.removeChild(notification);
                    }
                }, 500);
            }, 4000);
        }
        
        // Add keyboard shortcut
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
                showNotification('Search shortcut activated!', 'info');
            }
            
            if (e.key === 'Escape') {
                clearResults();
            }
        });
        
        // Initialize
        window.addEventListener('load', () => {
            showNotification('Welcome to USAMA DHUDDI SIM Database!', 'success');
            
            // Add focus effect to search input
            const searchInput = document.getElementById('searchInput');
            searchInput.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            searchInput.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
        
        // Add dark theme styles
        const darkThemeStyle = document.createElement('style');
        darkThemeStyle.textContent = `
            .dark-theme {
                --dark: #050508;
                --card: rgba(10, 15, 30, 0.9);
            }
            
            .dark-theme .header {
                background: rgba(5, 5, 10, 0.98);
            }
            
            .dark-theme .footer {
                background: rgba(5, 5, 10, 0.98);
            }
        `;
        document.head.appendChild(darkThemeStyle);
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
