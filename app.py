import streamlit as st
import pandas as pd
import requests
import time

# ==========================================
# 🔧 LINKS
# ==========================================
PIPEDREAM_URL = "https://eo4fe1dgen61r4b.m.pipedream.net"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3So6w_6JMrrzTWzgVw5-hF7fQpNVgwosQ1_lMN6g9L_jEn5cjGyyHkz0CjBK8aH9Y3fnSVr18s3xp/pub?output=csv"
# ==========================================

st.set_page_config(page_title="Insights Agent", layout="wide")

# Custom CSS for Dark Mode
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .card {
        background-color: #1E2330;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4F8BF9;
        margin-bottom: 15px;
    }
    h3 { color: #FFFFFF; margin: 0 0 10px 0; }
    p { color: #CCCCCC; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
spacer_left, col_middle, spacer_right = st.columns([1, 6, 1])
with col_middle:
    # Title
    st.markdown("<h1 style='text-align: center;'>Insights Agent 🧠</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AI-Powered Content Strategy Generator</p>", unsafe_allow_html=True)


# --- INPUT SECTION ---
st.write("")
st.divider()

c_in1, c_in2, c_in3 = st.columns([1, 2, 1])
with c_in2:
    keyword = st.text_input("Enter Niche / Keyword", placeholder="e.g. picky eater, child nutrition")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
    with col_btn2:
        run_btn = st.button("🚀 Analyze Strategy", type="primary", use_container_width=True)

# --- LOGIC SECTION ---
if run_btn and keyword:
    
    # 1. TRIGGER PIPEDREAM
    with st.status("Initializing Agent Workflow...", expanded=True) as status:
        st.write(f"📡 Sending '{keyword}' to Pipedream...")
        
        try:
            requests.post(PIPEDREAM_URL, json={"keyword": keyword})
            st.write("✅ Workflow Triggered!")
        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.stop()
            
        # 2. REALISTIC WAIT LOOP (60 Seconds)
        progress_bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.6) # 60 seconds total
            progress_bar.progress(i + 1)
            
            if i == 10: st.write("🕷️ Apify Scraper: Searching Instagram Reels...")
            elif i == 40: st.write("👀 Extracting viral hooks and captions...")
            elif i == 70: st.write("🧠 Groq AI: Analyzing psychological patterns...")
            elif i == 90: st.write("📝 Finalizing strategy & saving to database...")
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # 3. DISPLAY RESULTS
    st.subheader(f"Strategy Results for: {keyword}")
    
    try:
        # FORCE FRESH DATA
        st.cache_data.clear()
        unique_url = f"{SHEET_URL}&v={time.time()}"
        df = pd.read_csv(unique_url)
        
        latest = df.tail(3)[::-1]
        
        for index, row in latest.iterrows():
            c1, c2, c3 = st.columns(3)
            
            # ⚠️ HERE IS THE FIX: MATCHING YOUR EXACT SHEET HEADERS
            struggle = row.get("TOP STRUGGLE", "Waiting for AI...")
            hook = row.get("SUGGESTED HOOK", "Waiting for AI...")
            insight = row.get("STRATEGIC INSIGHT", "Waiting for AI...")
            
            with c1: st.markdown(f'<div class="card"><h3>Struggle</h3><p>{struggle}</p></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="card"><h3>Hook</h3><p>{hook}</p></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="card"><h3>Insight</h3><p>{insight}</p></div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error("Waiting for data... (Check your CSV link)")