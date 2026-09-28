import streamlit as st
import os
import sys
import importlib.util

# --- DYNAMICALLY LOCATE AND IMPORT ANALYZER.PY ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

analyzer_found = False
for root, dirs, files in os.walk(ROOT_DIR):
    if "analyzer.py" in files:
        if root not in sys.path:
            sys.path.insert(0, root)
        
        file_path = os.path.join(root, "analyzer.py")
        spec = importlib.util.spec_from_file_location("analyzer_module", file_path)
        analyzer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analyzer_module)
        analyze_niche = analyzer_module.analyze_niche
        analyzer_found = True
        break

if not analyzer_found:
    st.error("Critical Error: `analyzer.py` could not be located in the repository.")

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VERA — YouTube Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. YOUTUBE BRAND RED & DARK PALETTE STYLING ---
st.markdown("""
    <style>
    /* Force Streamlit Header & Toolbar Background */
    header[data-testid="stHeader"], 
    div[data-testid="stToolbar"],
    .stAppHeader {
        background-color: #0F0F0F !important;
        color: #FFFFFF !important;
    }

    /* Full-Width Canvas Layout with Balanced Side Margins */
    .stMainBlockContainer {
        padding-top: 3.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 100% !important;
    }

    /* Main Background & Base Text */
    .stApp {
        background-color: #0F0F0F;
        color: #F1F1F1;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Feature Cards Styling */
    .feature-card {
        background-color: #161616;
        border: 1px solid #262626;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease;
    }
    .feature-card:hover {
        border-color: #383838;
    }
    .feature-card h3 {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
    }
    .feature-card p {
        color: #AAAAAA;
        font-size: 0.9rem;
        line-height: 1.45;
        margin: 0;
    }

    /* Primary Action Buttons (YouTube Red) */
    .stButton>button {
        background-color: #FF0000;
        color: #FFFFFF;
        border-radius: 20px;
        border: none;
        padding: 0.65rem 1.6rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: background-color 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #CC0000;
        border: none;
        color: #FFFFFF;
    }

    /* Form Buttons */
    div[data-testid="stForm"] .stButton>button {
        border-radius: 20px;
    }

    /* Input Fields */
    .stTextInput input {
        background-color: #121212;
        color: #FFFFFF;
        border: 1px solid #282828;
        border-radius: 8px;
        font-size: 0.95rem;
        padding: 0.6rem 0.8rem;
    }
    .stTextInput input:focus {
        border-color: #FF0000;
        box-shadow: none;
    }

    /* Metrics Override */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.7rem !important;
        font-weight: 700;
    }

    /* Footer Badges */
    .badge-container {
        display: flex;
        gap: 12px;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #222222;
    }
    .badge {
        background-color: #141414;
        border: 1px solid #282828;
        color: #888888;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR WORKSPACE TRANSITION ---
if "workspace_active" not in st.session_state:
    st.session_state["workspace_active"] = False

# --- 4. BRAND HEADER ---
st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
        <svg width="34" height="24" viewBox="0 0 68 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M66.52 7.74C65.74 4.82 63.43 2.52 60.5 1.74C55.23 0.33 34 0.33 34 0.33C34 0.33 12.77 0.33 7.5 1.74C4.57 2.52 2.26 4.82 1.48 7.74C0.08 13.01 0 24 0 24C0 24 0.08 34.99 1.48 40.26C2.26 43.18 4.57 45.48 7.5 46.26C12.77 47.67 34 47.67 34 47.67C34 47.67 55.23 47.67 60.5 46.26C63.43 45.48 65.74 43.18 66.52 40.26C67.92 34.99 68 24 68 24C68 24 67.92 13.01 66.52 7.74Z" fill="#FF0000"/>
            <path d="M27 34L45 24L27 14V34Z" fill="white"/>
        </svg>
        <span style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;">VERA</span>
        <span style="color: #383838; font-size: 1.2rem; font-weight: 300;">|</span>
        <span style="color: #AAAAAA; font-size: 0.92rem; font-weight: 400; letter-spacing: 0.2px;">Video Evidence & Resonance Analytics</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid #222222; margin: 12px 0 24px 0;'>", unsafe_allow_html=True)

# --- 5. DASHBOARD WORKSPACE ---

if not st.session_state["workspace_active"]:
    st.markdown("<h2 style='font-size: 1.8rem; font-weight: 700; margin-bottom: 6px;'>Welcome to VERA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #AAAAAA; font-size: 1rem; margin-bottom: 2rem;'>An evidence-based intelligence agent designed to replace channel guesswork with observable public market data.</p>", unsafe_allow_html=True)
    
    # 3-Column Visual Card Layout filling side margins
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>📊 Market Sampling</h3>
                <p>Extracts public search metrics to establish real performance view baselines across competitive domains.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>🔍 Title Correlations</h3>
                <p>Pinpoints high-performing hooks and weak title patterns using structured quartile performance splits.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3>🚀 Testable Concepts</h3>
                <p>Formulates targeted video launch ideas backed directly by market sample gap analysis and trends.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    btn_col, info_col = st.columns([1, 3])
    with btn_col:
        if st.button("Launch Research Workspace →"):
            st.session_state["workspace_active"] = True
            st.rerun()

else:
    with st.form("search_form"):
        user_input = st.text_input(
            "Enter target channel topic or niche idea:",
            placeholder="e.g., Handmade Silver Jewellery, Python Web Development, Mechanical Keyboard Restoration",
            help="Provide a specific domain or topic for market evaluation."
        )
        
        c1, c2 = st.columns([1, 4])
        with c1:
            submitted = st.form_submit_button("Analyze Market")
        with c2:
            if st.form_submit_button("← Back to Welcome"):
                st.session_state["workspace_active"] = False
                st.rerun()

    if submitted:
        if not user_input.strip():
            st.warning("Please enter a valid topic or channel concept to proceed.")
        else:
            with st.spinner("Fetching public market metrics & evaluating strategy..."):
                try:
                    # Inject Streamlit secrets into system environment for backend services
                    if "YOUTUBE_API_KEY" in st.secrets:
                        os.environ["YOUTUBE_API_KEY"] = st.secrets["YOUTUBE_API_KEY"]
                    if "GROQ_API_KEY" in st.secrets:
                        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

                    # Execute processing function directly
                    data = analyze_niche(user_input)
                    
                    if isinstance(data, dict):
                        if data.get("status") == "NEEDS_NICHE":
                            st.info("💡 Input is broad. Select a refined domain to execute precise analysis:")
                            for niche in data.get("suggested_niches", []):
                                st.markdown(f"- **{niche}**")
                        
                        elif data.get("status") == "SUCCESS":
                            st.markdown("### 📈 Performance Baseline")
                            m1, m2 = st.columns(2)
                            m1.metric("Sample Size", f"{data.get('analyzed_sample_size', 0)} Videos")
                            m2.metric("Median Views Benchmark", f"{data.get('median_views_in_sample', 0):,} views")
                            
                            st.markdown("<hr style='border: none; border-top: 1px solid #222222; margin: 20px 0;'>", unsafe_allow_html=True)
                            
                            st.markdown("### 🧠 Observed Title Patterns")
                            p_left, p_right = st.columns(2)
                            
                            with p_left:
                                st.markdown("🟢 **Stronger Performing Patterns**")
                                for pattern in data.get("strong_patterns", []):
                                    st.markdown(f"• {pattern}")
                                    
                            with p_right:
                                st.markdown("🔴 **Weaker Performing Patterns**")
                                for pattern in data.get("weaker_patterns", []):
                                    st.markdown(f"• {pattern}")
                                    
                            st.markdown("<hr style='border: none; border-top: 1px solid #222222; margin: 20px 0;'>", unsafe_allow_html=True)
                            
                            st.markdown("### 🚀 Testable Launch Ideas")
                            ideas = data.get("launch_ideas", [])
                            for idx, idea in enumerate(ideas, 1):
                                with st.expander(f"Concept {idx}: {idea.get('title_framework')}"):
                                    st.write(f"**Format:** {idea.get('format')}")
                                    st.write(f"**Target Subtopic:** {idea.get('target_subtopic')}")
                                    st.write(f"**Data Observation:** {idea.get('rationale_from_data')}")
                    else:
                        st.error("Received unexpected response structure from analysis engine.")

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

# --- 6. FOOTER DISCLAIMER BADGES ---
st.markdown("""
    <div class="badge-container">
        <span class="badge">🌐 Public Metadata Sourced</span>
        <span class="badge">🔒 Zero Private Analytics Access</span>
        <span class="badge">📊 Sample Correlation Model</span>
    </div>
""", unsafe_allow_html=True)
