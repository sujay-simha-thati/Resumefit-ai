import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

# ==========================================
# 🌌 MODERN SAAS TECH GRADIENT LAYOUT STYLING
# ==========================================
st.set_page_config(
    page_title="ResumeFit AI | Smart Matcher", 
    page_icon="🤖", 
    layout="wide"
)



if "reset_counter" not in st.session_state:
    st.session_state["reset_counter"] = 0

if "processed_leaderboard" not in st.session_state:
    st.session_state["processed_leaderboard"] = None


# Deep space backdrop with dynamic electric radial ambient lighting elements
st.markdown("""
    <style>
    /* Nuclear sweep for empty UI frameworks and horizontal placeholder rows */
div:empty,
[data-testid="stHorizontalBlock"] > div:empty,
[data-testid="stVerticalBlock"] > div:empty,
.element-container:empty {
    display: none !important;
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin: 0px !important;
}

/* Ensure structural container grids have zero background visibility */
[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stColumn"] {
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}


    /* Nuclear background clear for all default Streamlit block structures */
[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stColumn"],
div[data-viewport="true"] > div {
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Re-apply the explicit styling background ONLY to your operational cards */
.saas-card {
    background-color: #0d1527 !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}



     /* 1. Base app styling with deep space background */
    .stApp {
        background-color: #020712 !important;
    }

    /* 2. Fix the dark/empty block glitch by making container wrappers blend in */
    [data-testid="stVerticalBlock"] > div,
    [data-testid="stHorizontalBlock"] > div,
    .element-container, 
    div[data-testid="stBlock"] {
        background-color: transparent !important;
    }

    /* 3. Style your custom dashboard cards/containers so they look premium */
    div[data-testid="stVerticalBlock"] > div:has(textarea),
    div[data-testid="stVerticalBlock"] > div:has(input) {
        background-color: #0d1527 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px;
        padding: 1.5rem;
    }
 
    .saas-brand {
        font-weight: 700;
        font-size: 1.35rem;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .saas-brand span {
        color: #06b6d4;
    }
    .saas-nav-links {
        display: flex;
        gap: 32px;
        font-size: 0.9rem;
        color: #9ca3af;
        font-weight: 500;
    }

    /* Modern SaaS Hero Typography Section */
    .hero-container {
        text-align: center;
        max-width: 850px;
        margin: 0 auto 50px auto;
    }
    .saas-badge {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.2);
        color: #22d3ee;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 6px 16px;
        border-radius: 100px;
        display: inline-block;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    .saas-hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
        letter-spacing: -1.5px;
        margin-bottom: 15px;
    }
    .saas-hero-title span {
        color: #06b6d4;
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
    }
    .saas-hero-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        line-height: 1.6;
    }
    
    /* Sleek Tech Container Grid Cards */
    .saas-card {
        background: rgba(17, 24, 39, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 30px;
        backdrop-filter: blur(24px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .saas-card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Style entry fields to match the dark glass backdrop aesthetic */
    textarea {
        background-color: rgba(3, 7, 18, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f3f4f6 !important;
        font-size: 0.95rem !important;
        padding: 15px !important;
    }
    textarea:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.15) !important;
    }

    div[data-testid="stFileUploadDropzone"] {
        background-color: rgba(3, 7, 18, 0.4) !important;
        border: 1px dashed rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* Pill Electric Blue SaaS Action Button Look */
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 0.75rem 2.5rem !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: block;
        margin: 0 auto;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 30px rgba(6, 182, 212, 0.45);
        transform: translateY(-1px);
        color: #ffffff !important;
    }

    /* Analytics Dashboard Metric Blocks */
    .saas-metric-container {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }
    .saas-metric-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        padding: 20px;
        border-radius: 14px;
        flex: 1;
        text-align: center;
    }
    .saas-metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .saas-metric-lbl {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 6px;
        font-weight: 500;
    }
    

}

    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 NLP & MATHEMATICAL DATA PIPELINE
# ==========================================
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text.strip()
    except Exception:
        return ""

def calculate_match_scores(job_desc, resume_dict):
    if not job_desc or not resume_dict:
        return []
    documents = [job_desc]
    candidate_names = list(resume_dict.keys())
    for name in candidate_names:
        documents.append(resume_dict[name])
        
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(documents)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    results = []
    for idx, name in enumerate(candidate_names):
        match_percentage = round(float(scores[idx].item()) * 100, 2)
        results.append({
            "Candidate Profile": name,
            "Match Vector Score": match_percentage
        })
    return sorted(results, key=lambda x: x["Match Vector Score"], reverse=True)

# ==========================================
# 💻 UI DASHBOARD LAYOUT
# ==========================================

# Modern SaaS Minimalist Header Navigation
st.markdown('''
<div class="saas-header-row">
    <div class="saas-brand">ResumeFit<span>.ai</span></div>
    <div class="saas-nav-links">
        <span>AI Solutions</span>
        <span>Features</span>
        <span>Use Cases</span>
        <span>Pricing</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Centralized Project Title Hero Section
st.markdown('''
<div class="hero-container">
    <div class="saas-badge">✨ Portfolio Showcase Mode</div>
    <h1 class="saas-hero-title">ResumeFit AI: Smart <span>Resume Matcher</span></h1>
    <p class="saas-hero-subtitle">An automated Natural Language Processing application designed to automatically clean, vectorize, and match candidate resumes against job descriptions using unsupervised similarity math.</p>
</div>
''', unsafe_allow_html=True)

# Workspace Columns Framework Split 
# Create your column split layout structures
# Create your column split layout structures cleanly
# ==========================================
# 🌌 WORKSPACE COLUMNS FRAMEWORK SPLIT
# ==========================================

# ==========================================
# 🌌 WORKSPACE COLUMNS FRAMEWORK SPLIT
# ==========================================



col1, col2 = st.columns(2)

with col1:
    # 🌌 LEFT TOP BOX: Target Job Description Panel
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown('<div class="saas-card-title">🌐 1. Target job description</div>', unsafe_allow_html=True)
    job_description_input = st.text_area(
        "Paste Corporate Job Description Details Here:",
        height=200,
        placeholder="Enter career criteria parameters (e.g., Python, Machine Learning platforms, NLP models...)",
        label_visibility="collapsed",
        key=f"job_desc_input_{st.session_state['reset_counter']}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 📂 LEFT BOTTOM BOX: PDF Ingestion Panel
    st.markdown('<div class="saas-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown('<div class="saas-card-title">📂 2. Candidate\'s resume pdf </div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload Unstructured Candidate PDF Resumes",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"pdf_uploader_{st.session_state['reset_counter']}"
    )
    st.markdown('</div>', unsafe_allow_html=True)
start_analysis = st.button("Get Started ✨", use_container_width=True)

# ==========================================
# 🚀 CORE DATA EXECUTION ROUTINE
# ==========================================
# Local fallbacks to make sure variables always exist
leaderboard_data_final = None
resumes_extracted_list = []

if start_analysis and job_description_input and uploaded_files:
    resume_dict = {}
    
    # 1. Extract text from uploaded PDF files
    for file in uploaded_files:
        raw_text = extract_text_from_pdf(file)
        if raw_text:
            resume_dict[file.name] = raw_text
            resumes_extracted_list.append(raw_text)
            
    # 2. Run the scoring matrix mathematical pipeline
    scored_results = calculate_match_scores(job_description_input, resume_dict)
    
    if scored_results:
        leaderboard_data_final = pd.DataFrame(scored_results)
# ==========================================
# 📊 LEADERBOARD & FEATURE ANALYSIS DISPLAY ROUTINE
# ==========================================
with col2:
    st.markdown('<div class="saas-card" style="min-height: 520px;">', unsafe_allow_html=True)
    st.markdown('<div class="saas-card-title">📊 3. Real-time Analysis & Leaderboard</div>', unsafe_allow_html=True)

    # Check if calculation results were populated successfully
    if leaderboard_data_final is not None and not leaderboard_data_final.empty:
        
        # Expanded tracking keyword array including your target tools
        COMMON_SKILLS = ["python", "machine learning", "nlp", "deep learning", "sql", "aws", "docker", 
                         "tableau", "power bi", "java", "c++", "react", "javascript", "devops", "git", 
                         "html", "pandas", "numpy"]
        
        # Clean the input parameters to handle comma-separated lists without spaces correctly
        jd_processed = job_description_input.lower().replace(",", " ")
        target_skills = [skill for skill in COMMON_SKILLS if skill in jd_processed]
        
        if not target_skills:
            target_skills = ["python", "machine learning", "nlp", "sql"]

        # Loop through rows to display cards
        for index, row in leaderboard_data_final.iterrows():
            filename = row['Candidate Profile']
            score = row['Match Vector Score']
            
            resume_text_raw = resumes_extracted_list[index].lower() if index < len(resumes_extracted_list) else ""
            matched_skills = [skill.title() for skill in target_skills if skill in resume_text_raw]
            missing_skills = [skill.title() for skill in target_skills if skill not in resume_text_raw]

            matched_skills_str = ", ".join(matched_skills) if matched_skills else "None"
            missing_skills_str = ", ".join(missing_skills) if missing_skills else "None"

            # --- 🎯 CORE ATS COMPATIBILITY ENGINE SCORE SYSTEM ---
            # Standardizing the matrix text similarity score scale out of a direct 100 benchmark
            ats_score = int(score) if score <= 100 else 100
            
            # Formulating specific ATS parsing compliance tier markers
            if ats_score >= 75:
                ats_tier = "🚀 Optimized (Highly Compatible)"
                ats_color = "#4ade80"
            elif ats_score >= 45:
                ats_tier = "⚡ Moderate (Keyword Missing)"
                ats_color = "#fbbf24"
            else:
                ats_tier = "⚠️ Critical (High Rejection Risk)"
                ats_color = "#f87171"

            # --- DYNAMIC STRUCTURAL IMPROVEMENT SUGGESTIONS ENGINE ---
            suggestions = []
            if score < 40:
                suggestions.append("⚠️ **Critical Alignment Gap:** Core background matrix lacks keyword concentrations requested by job taxonomy benchmarks.")
            
            if missing_skills:
                suggestions.append(f"💡 **Skill Optimizations Needed:** Integrate semantic mentions of missing frameworks: *{missing_skills_str}* to pass resume tracking systems.")
                
            if len(resume_text_raw.split()) < 200:
                suggestions.append("📝 **Context Density Advisory:** Resume text length is too brief. Expand quantitative role achievements to improve vector scores.")
                
            if not suggestions:
                suggestions.append("✨ **Elite Structural Matching:** Profile features a high density of relevant target metrics.")

            # --- 📝 DYNAMIC RESUME SUMMARY GENERATOR ENGINE ---
            clean_name = filename.replace(".pdf", "").replace("_", " ").split()
            clean_name = clean_name[0] if clean_name else "Candidate"
            
            if matched_skills:
                skills_pitch = f"proficient core competencies in {', '.join(matched_skills[:3])}"
            else:
                skills_pitch = "an adaptable technical framework background"

            if score > 60:
                summary_text = f"**Professional Summary:** {clean_name} is a highly aligned candidate displaying a {score:.1f}% semantic similarity matching matrix. Features strong technical acumen with {skills_pitch}. Well-positioned to deliver optimized engineering workflows matching core corporate functional targets."
            elif score > 30:
                summary_text = f"**Professional Summary:** {clean_name} is an emerging professional exhibiting a solid baseline profile alignment of {score:.1f}%. Demonstrates applied knowledge across {skills_pitch}. Primed to bridge current vector gaps quickly and add immediate value within an agile team framework."
            else:
                summary_text = f"**Professional Summary:** {clean_name} is a candidate showcasing {skills_pitch} with an initial tracking match value of {score:.1f}%. Highly motivated profile well-suited for progressive career development pipelines with targeted upskilling in {missing_skills_str if missing_skills else 'advanced frameworks'}."

            # --- PREMIUM LEADERBOARD MATCH CARD ---
            st.markdown(f"""
            <div style="background: #0d1527; border: 1px solid #1e293b; border-radius: 12px; padding: 1.25rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span style="color: #94a3b8; font-weight: 500; font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 50%;">{filename}</span>
                    <div style="display: flex; gap: 8px;">
                        <span style="background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 0.3rem 0.65rem; border-radius: 20px; font-weight: bold; font-size: 0.8rem; border: 1px solid rgba(56, 189, 248, 0.2);">
                            {score:.1f}% Sim
                        </span>
                        <span style="background: linear-gradient(135deg, #06b6d4, #0891b2); color: white; padding: 0.3rem 0.65rem; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">
                            🎯 ATS Score: {ats_score}/100
                        </span>
                    </div>
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem;">
                    Parsing Tier: <span style="color: {ats_color}; font-weight: 600;">{ats_tier}</span>
                </div>
                <hr style="border-color: #1e293b; margin: 0.5rem 0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    <div>
                        <span style="color: #4ade80; font-size: 0.8rem; font-weight: bold; display: block;">✓ Matched Matrix</span>
                        <p style="color: #e2e8f0; font-size: 0.8rem; margin: 0;">{matched_skills_str}</p>
                    </div>
                    <div>
                        <span style="color: #f87171; font-size: 0.8rem; font-weight: bold; display: block;">✗ Missing Vectors</span>
                        <p style="color: #e2e8f0; font-size: 0.8rem; margin: 0;">{missing_skills_str}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- INTERACTIVE EXPANDERS FOR ANALYTICS FEATURES ---
            with st.expander("🛠️ View Custom Profile Improvement Suggestions", expanded=False):
                for tip in suggestions:
                    st.markdown(tip)
                    
            with st.expander("📄 View AI-Generated Professional Resume Summary", expanded=False):
                st.markdown(summary_text)
                st.caption("ℹ️ *This summary is dynamically synthesized based on candidate profile similarity matrices and matched role metrics.*")
                    
            st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
            
    else:
        # Default placeholder view when resting or awaiting execution
        st.markdown("""
        <div style="text-align: center; color: #64748b; padding-top: 8rem;">
            <p style="font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">Awaiting Workspace Alignment</p>
            <p style="font-size: 0.85rem;">Fill out parameters on the left and click 'Get Started' to process profiles.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

#  -- All your main layout, inputs, matrices, and calculations go above here ---

# Add spacing above the reset action
st.write("---") 


# Reset Workspace Button with Callback
def reset_workspace_callback():
    # Clear out the raw input text states completely
    st.session_state["job_desc_input"] = ""
    st.session_state["pdf_uploader"] = None  # File uploader expects None instead of an empty list to reset

# Clear cache button code
# Clear cache button block
st.markdown('<div class="reset-container">', unsafe_allow_html=True)
if st.button("Reset Application Workspace", use_container_width=True):
    st.session_state["reset_counter"] += 1
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

