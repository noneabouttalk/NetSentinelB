import streamlit as st
import subprocess
import json
import os
import requests
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NetSentinel — Network Threat Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (login + app) — LIGHT THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #f0f4f8;
    --surface:   #ffffff;
    --panel:     #f7f9fc;
    --border:    #d1dce8;
    --accent:    #0066cc;
    --accent2:   #004499;
    --danger:    #d92b4b;
    --warn:      #d97706;
    --success:   #059669;
    --text:      #1a2533;
    --muted:     #6b8099;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
    --font-body: 'IBM Plex Sans', sans-serif;
}

/* ── Global base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stHeader"]        { display: none !important; }
[data-testid="stSidebar"]       { display: none !important; }
[data-testid="collapsedControl"]{ display: none !important; }
footer                          { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ══════════════════════════════════════════
   LOGIN SCREEN — viewport-fit, no scroll
══════════════════════════════════════════ */

/* Make the Streamlit root containers fill the viewport */
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div,
[data-testid="stVerticalBlock"] {
    height: auto !important;
}

/* Full-screen login wrapper injected via markdown */
.login-root {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    z-index: 0;
    overflow: hidden;
}

/* Subtle dot-grid background */
.login-root::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.55;
}

/* Soft glow orb */
.login-root::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(70vw, 560px);
    height: min(70vw, 560px);
    background: radial-gradient(circle, rgba(0,102,204,0.07) 0%, transparent 70%);
    pointer-events: none;
    animation: pulse 7s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.7; transform: translate(-50%,-50%) scale(1); }
    50%       { opacity: 1;   transform: translate(-50%,-50%) scale(1.08); }
}

.login-card {
    position: relative;
    z-index: 10;
    width: min(420px, 92vw);
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 6px;
    padding: clamp(28px, 5vh, 48px) clamp(24px, 5vw, 44px) clamp(24px, 4vh, 40px);
    box-shadow: 0 4px 24px rgba(0,66,153,0.08), 0 20px 60px rgba(0,0,0,0.06);
    animation: cardIn 0.55s cubic-bezier(0.22,1,0.36,1) both;
}

@keyframes cardIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.login-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: clamp(20px, 3vh, 32px);
}

.login-logo-icon {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, var(--accent2), var(--accent));
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    color: #fff;
    flex-shrink: 0;
}

.login-logo-text {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 19px;
    color: var(--text);
    letter-spacing: -0.02em;
}

.login-logo-sub {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--accent);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-top: 1px;
}

.login-title {
    font-family: var(--font-head);
    font-weight: 700;
    font-size: 20px;
    color: var(--text);
    margin-bottom: 4px;
}

.login-subtitle {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-bottom: clamp(18px, 2.5vh, 28px);
}

/* Input overrides */
.stTextInput > label {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 4px !important;
}

.stTextInput > div > div > input {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    padding: 9px 13px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.1) !important;
    outline: none !important;
}

.login-error {
    background: rgba(217,43,75,0.06);
    border: 1px solid rgba(217,43,75,0.22);
    border-radius: 4px;
    padding: 9px 13px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--danger);
    margin-top: 10px;
    letter-spacing: 0.03em;
}

.login-footer {
    font-family: var(--font-mono);
    font-size: 9px;
    color: #b0bec9;
    text-align: center;
    margin-top: clamp(16px, 2vh, 28px);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    line-height: 1.7;
}

/* ══════════════════════════════════════════
   MAIN APP — LIGHT THEME
══════════════════════════════════════════ */

/* Top bar */
.topbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 56px;
    background: rgba(255,255,255,0.94);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    z-index: 1000;
    animation: barIn 0.4s ease both;
    box-shadow: 0 1px 8px rgba(0,66,153,0.06);
}

@keyframes barIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.topbar-icon {
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, var(--accent2), var(--accent));
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #fff;
}

.topbar-name {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 16px;
    color: var(--text);
    letter-spacing: -0.01em;
}

.topbar-version {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--accent);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 2px 7px;
    border: 1px solid rgba(0,102,204,0.22);
    border-radius: 2px;
    background: rgba(0,102,204,0.05);
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.topbar-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--success);
    letter-spacing: 0.1em;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: var(--success);
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

.topbar-btn {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    padding: 5px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.topbar-btn:hover {
    color: var(--accent) !important;
    border-color: var(--accent) !important;
    background: rgba(0,102,204,0.05) !important;
}

.topbar-user {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.08em;
}

/* Page body offset */
.main-body {
    padding-top: 80px;
    padding-left: 32px;
    padding-right: 32px;
    padding-bottom: 40px;
    max-width: 1440px;
    margin: 0 auto;
}

/* Hero header */
.page-header {
    margin-bottom: 36px;
    animation: fadeUp 0.5s ease 0.15s both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.page-title {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 30px;
    color: var(--text);
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.page-title span {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.page-desc {
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--muted);
    margin-top: 8px;
    font-weight: 300;
    max-width: 560px;
    line-height: 1.6;
}

/* Upload zone */
.upload-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 10px;
}

/* Section panels */
.panel-header-light {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 16px 24px;
}

.panel-num {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--accent);
    letter-spacing: 0.2em;
    background: rgba(0,102,204,0.07);
    border: 1px solid rgba(0,102,204,0.18);
    border-radius: 2px;
    padding: 2px 7px;
}

.panel-title {
    font-family: var(--font-head);
    font-weight: 700;
    font-size: 14px;
    color: var(--text);
    letter-spacing: -0.01em;
}

/* Stats chips */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 11px;
    padding: 5px 11px;
    border-radius: 2px;
    margin-right: 8px;
    margin-bottom: 8px;
    letter-spacing: 0.04em;
}

.chip-warn {
    background: rgba(217,119,6,0.08);
    border: 1px solid rgba(217,119,6,0.22);
    color: var(--warn);
}

.chip-info {
    background: rgba(0,102,204,0.07);
    border: 1px solid rgba(0,102,204,0.2);
    color: var(--accent);
}

.chip-ok {
    background: rgba(5,150,105,0.07);
    border: 1px solid rgba(5,150,105,0.2);
    color: var(--success);
}

/* Divider */
.divider {
    height: 1px;
    background: var(--border);
    margin: 28px 0;
}

/* Report output */
.report-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 24px;
    font-family: var(--font-body);
    font-size: 13px;
    line-height: 1.8;
    color: var(--text);
}

/* Streamlit file uploader */
.stFileUploader > label {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

.stFileUploader section {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 3px !important;
}

.stFileUploader section:hover {
    border-color: var(--accent) !important;
}

.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    overflow: hidden !important;
}

.stDataFrame table {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
}

/* Streamlit button */
div[data-testid="stButton"] > button {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, var(--accent2), var(--accent)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 10px 28px !important;
    transition: opacity 0.2s, transform 0.2s !important;
    width: 100% !important;
}

div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Alert / info boxes */
.stAlert {
    border-radius: 3px !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
}

/* Columns gap */
[data-testid="stHorizontalBlock"] {
    gap: 24px !important;
}

/* Heading tags */
h1, h2, h3, h4 {
    font-family: var(--font-head) !important;
    color: var(--text) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

LLAMA_SERVER_URL = "http://host.docker.internal:8080/v1/chat/completions"

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ─────────────────────────────────────────────
#  CREDENTIALS  (change as needed)
# ─────────────────────────────────────────────
VALID_USERS = {
    "admin":   "admin",
}

# ════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ════════════════════════════════════════════════════════
if not st.session_state.authenticated:

    # Full-screen decorative layer (position:fixed, behind the form)
    st.markdown('<div class="login-root"></div>', unsafe_allow_html=True)

    # Center columns — the card itself is rendered via Streamlit widgets
    # so inputs remain interactive (pure HTML forms don't work in Streamlit)
    col_l, col_c, col_r = st.columns([1, 1.05, 1])
    with col_c:
        # Card wrapper
        st.markdown("""
        <div class="login-card" style="margin-top:calc(50vh - 260px);">
            <div class="login-logo">
                <div class="login-logo-icon">&#9671;</div>
                <div>
                    <div class="login-logo-text">NetSentinel</div>
                    <div class="login-logo-sub">Network Threat Intelligence</div>
                </div>
            </div>
            <div class="login-title">Secure Access</div>
            <div class="login-subtitle">Enter your credentials to access the SOC dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="analyst@org.com", key="login_user")
        password = st.text_input("Password", type="password", placeholder="••••••••••••", key="login_pass")

        if st.button("Authenticate"):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.login_error = False
                st.rerun()
            else:
                st.session_state.login_error = True

        if st.session_state.login_error:
            st.markdown(
                '<div class="login-error">&#9432; &nbsp; Authentication failed. Verify your credentials.</div>',
                unsafe_allow_html=True
            )

        st.markdown("""
        <div class="login-footer">
            Restricted System — Authorized Personnel Only<br>
            All activity is logged and monitored
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ════════════════════════════════════════════════════════
#  TOP BAR
# ════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-icon">&#9671;</div>
        <span class="topbar-name">NetSentinel</span>
        <span class="topbar-version">v2.4.1</span>
    </div>
    <div class="topbar-right">
        <div class="topbar-status">
            <div class="status-dot"></div>
            Engine Online
        </div>
        <a class="topbar-btn" href="https://localhost:443" target="_blank">
            &#8599; &nbsp; Threat Console
        </a>
        <span class="topbar-user">&#9632; &nbsp;{st.session_state.username.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════
st.markdown('<div class="main-body">', unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-title">Network <span>Threat Analysis</span></div>
    <div class="page-desc">
        Upload a packet capture file to run automated deep inspection via Suricata IDS
        and generate an AI-powered executive threat report.
    </div>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown('<div class="upload-label">&#9632; &nbsp; Packet Capture Input</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your capture file here — supported formats: .pcapng, .pcap",
    type=["pcapng", "pcap"],
    max_upload_size=500,
    label_visibility="collapsed"
)

if uploaded_file is not None:

    timestamp_id = str(int(time.time()))
    pcap_path    = os.path.join("/tmp", f"{timestamp_id}_{uploaded_file.name}")
    output_dir   = os.path.join("/tmp", f"suricata_out_{timestamp_id}")
    os.makedirs(output_dir, exist_ok=True)

    with open(pcap_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Column 1: Suricata ──────────────────────────────
    with col1:
        st.markdown("""
        <div class="panel-header-light">
            <span class="panel-num">01</span>
            <span class="panel-title">IDS Inspection — Suricata</span>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Running deep packet inspection..."):
            subprocess.run(
                ["suricata", "-r", pcap_path, "-l", output_dir, "-k", "none"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

        eve_path   = os.path.join(output_dir, "eve.json")
        alertas_raw = []

        if os.path.exists(eve_path):
            with open(eve_path, "r") as f:
                for linea in f:
                    try:
                        log = json.loads(linea)
                        if log.get("event_type") == "alert":
                            alert = log.get("alert", {})
                            sev   = alert.get("severity")
                            cat   = alert.get("category", "")
                            ruido = [
                                "Generic Protocol Command Decode",
                                "Potentially Bad Traffic",
                                "TCPv4 invalid checksum"
                            ]
                            if sev in [1, 2] and cat not in ruido:
                                alertas_raw.append({
                                    "fecha":          log.get("timestamp")[:19],
                                    "ip_origen":      log.get("src_ip"),
                                    "puerto_destino": log.get("dest_port"),
                                    "ip_destino"    : log.get("dest_ip"),
                                    "severidad":      sev,
                                    "categoria":      cat,
                                    "firma_amenaza":  alert.get("signature")
                                })
                    except Exception:
                        continue

        if alertas_raw:
            vistas            = set()
            alertas_filtradas = []
            for a in alertas_raw:
                if a["firma_amenaza"] not in vistas:
                    alertas_filtradas.append(a)
                    vistas.add(a["firma_amenaza"])

            st.markdown(f"""
            <div style="margin:16px 0 12px;">
                <span class="chip chip-warn">&#9650; {len(alertas_raw)} suspicious events</span>
                <span class="chip chip-info">&#9670; {len(alertas_filtradas)} unique signatures</span>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(alertas_filtradas, use_container_width=True, hide_index=True)
        else:
            alertas_filtradas = []
            st.markdown("""
            <div style="margin:16px 0 12px;">
                <span class="chip chip-ok">&#10003; No critical threats detected</span>
            </div>
            """, unsafe_allow_html=True)
            st.success("Suricata completed inspection. No high-severity alerts under active filter criteria.")

    # ── Column 2: AI Report ─────────────────────────────
    with col2:
        st.markdown("""
        <div class="panel-header-light">
            <span class="panel-num">02</span>
            <span class="panel-title">AI Executive Threat Report</span>
        </div>
        """, unsafe_allow_html=True)

        if alertas_filtradas:
            with st.spinner("Generating intelligence report..."):
                datos_para_ia = alertas_filtradas[:20]
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Eres un Ingeniero experto en SOC. Analiza los JSON de Suricata y redacta "
                                "un informe técnico preciso y profesional en ESPAÑOL. "
                                "Usa temperatura 0.1 para máxima precisión."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Analiza estas alertas filtradas y genera el reporte ejecutivo:\n"
                                f"{json.dumps(datos_para_ia, indent=2)}"
                            )
                        }
                    ],
                    "temperature": 0.1,
                    "stream": False
                }

                try:
                    res_ia = requests.post(LLAMA_SERVER_URL, json=payload, timeout=1200)
                    if res_ia.status_code == 200:
                        reporte = res_ia.json()["choices"][0]["message"]["content"]
                        st.markdown(
                            f'<div class="report-box">{reporte}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.error(f"AI engine returned status {res_ia.status_code}. Check llama.cpp server.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.markdown("""
            <div class="report-box" style="color:var(--muted);font-family:'IBM Plex Mono',monospace;
                 font-size:11px;letter-spacing:0.05em;text-align:center;padding:48px 24px;">
                No anomalies detected — AI analysis not required.
            </div>
            """, unsafe_allow_html=True)

    # Cleanup
    try:
        if os.path.exists(pcap_path):
            os.remove(pcap_path)
    except Exception:
        pass

else:
    # Empty state illustration
    st.markdown("""
    <div style="text-align:center;padding:80px 0 60px;animation:fadeUp 0.5s ease 0.3s both;">
        <div style="font-size:48px;margin-bottom:20px;opacity:0.12;">&#9671;</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);
             letter-spacing:0.1em;text-transform:uppercase;">
            Awaiting packet capture input
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-body