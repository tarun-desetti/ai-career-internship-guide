"""
AI-Powered Internship Recommendation Engine
Built with Streamlit for PM Internship Scheme
"""

import streamlit as st
import sys
sys.path.append('.')

from data.real_internships import get_all_internships, get_statistics
from models.recommender import InternshipRecommender, calculate_profile_strength
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def generate_roadmap(skill_gaps):
    roadmap = {}
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    
    for i, skill in enumerate(skill_gaps[:4]):
        roadmap[weeks[i]] = f"Learn {skill} fundamentals and build 1 small project"
    
    return roadmap

# Page configuration
st.set_page_config(
    page_title="AI Internship Recommender",
    page_icon="💃🏻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

/* ===== HEADERS ===== */
.main-header {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.sub-header {
    font-size: 1.15rem;
    text-align: center;
    color: #94a3b8;
    margin-bottom: 2rem;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e5e7eb;
}

/* ===== CARDS ===== */
.stat-card {
    background: linear-gradient(135deg, #1e293b, #020617);
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(56,189,248,0.15);
    border: 1px solid rgba(56,189,248,0.2);
}

.stat-card h2 {
    font-size: 2.3rem;
    color: #38bdf8;
}

/* ===== MATCH CARD ===== */
.match-card {
    background: rgba(2,6,23,0.8);
    border-radius: 18px;
    padding: 1.8rem;
    border-left: 4px solid #818cf8;
    box-shadow: 0 0 40px rgba(129,140,248,0.15);
}

/* ===== SCORE ===== */
.match-score {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== BADGES ===== */
.success-badge {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: #022c22;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
    margin-top: 0.5rem;
}

/* ===== SKILLS ===== */
.skill-tag {
    display: inline-block;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    margin: 0.25rem;
    font-size: 0.8rem;
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.3);
}

.skill-gap {
    background: rgba(251,191,36,0.15);
    color: #facc15;
    border: 1px solid rgba(251,191,36,0.3);
}

/* ===== BUTTONS ===== */
button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 14px;
    font-weight: 700;
    border: none;
    box-shadow: 0 0 30px rgba(99,102,241,0.4);
}

button[kind="secondary"] {
    background: transparent;
    border: 1px solid #334155;
    color: #e5e7eb;
    border-radius: 14px;
}

/* ===== METRICS ===== */
[data-testid="stMetricValue"] {
    color: #38bdf8;
    font-weight: 700;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background: #020617;
    border-radius: 14px;
    border: 1px solid #1e293b;
}
/* Emoji visibility boost */
span, p, h1, h2, h3, h4 {
    filter: brightness(1.2);
}
/* Sidebar radio button visibility */
section[data-testid="stSidebar"] label {
    color: #e5e7eb !important;
    opacity: 1 !important;
}            
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'student_profile' not in st.session_state:
    st.session_state.student_profile = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

# Initialize components
@st.cache_resource
def load_recommender():
    return InternshipRecommender()

@st.cache_data
def load_internships():
    return get_all_internships()

@st.cache_data
def load_stats():
    return get_statistics()

recommender = load_recommender()
all_internships = load_internships()
stats = load_stats()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
    "assets/heroo.jpg",
    width=120
)
        st.markdown(
    """
    <style>
    img {
        border-radius: 50%;
        border: 2px solid #38bdf8;
        box-shadow: 0 0 25px rgba(56,189,248,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.title("Navigation")
    
    page = st.radio(
        "Choose Page",
        ["🏠 Home", "👤 Create Profile", "🎯 Recommendations", "📊 Analytics", "💼 Browse Internships"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    **AI Internship Recommender**
    
    Intelligent matching using:
    - Multi-factor analysis
    - Skill gap identification
    - Success probability
    - Personalized learning paths
    """)
    
    st.markdown("---")
    st.markdown("### Stats")
    st.metric("Total Internships", stats['total_internships'])
    st.metric("Companies", stats['total_companies'])
    st.metric("Avg Stipend", f"₹{stats['avg_stipend']:,.0f}")
# HOME PAGE
if "🏠 Home" in page:
    
    # ===== HERO HEADER =====
    col_icon, col_title = st.columns([1, 14])

    with col_icon:
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                font-size: 2.5rem;
            ">
                
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_title:
        st.markdown(
            "<div class='main-header'>AI Career Copilot – Your Personalized Internship Navigator </div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='sub-header'>Built by Team of Love • Powered by Advanced ML • PM Internship Scheme</div>",
        unsafe_allow_html=True
    )    
    # Hero stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{stats['total_internships']}</h2>
            <p>Live Internships</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{stats['total_companies']}</h2>
            <p>Top Companies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>90%</h2>
            <p>Match Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>85%</h2>
            <p>Time Saved</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features
    st.subheader("🚀 Why Choose Our AI Engine?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 🎯 Smart Matching")
        st.write("Multi-factor algorithm analyzes skills, interests, and career goals")
    
    with col2:
        st.markdown("#### ⚡ Lightning Fast")
        st.write("Get personalized recommendations in under 1 second")
    
    with col3:
        st.markdown("#### 📊 Skill Gap Analysis")
        st.write("Know exactly what to learn for your dream internship")
    
    with col4:
        st.markdown("#### 🤖 Explainable AI")
        st.write("Understand why each internship was recommended")
    
    # Call to action
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Get Started - Create Your Profile", type="primary", use_container_width=True):
            page = "👤 Create Profile"
            st.rerun()
    
    # Top Skills in Demand
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔥 Top Skills in Demand")
    
    # Create bar chart
    top_skills = stats['top_skills'][:10]
    skill_counts = list(range(len(top_skills), 0, -1))  # Descending counts
    
    fig = px.bar(
        x=skill_counts,
        y=top_skills,
        orientation='h',
        labels={'x': 'Demand', 'y': 'Skill'},
        color=skill_counts,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Featured Companies
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💼 Featured Companies Hiring")
    
    companies = stats['companies'][:12]
    cols = st.columns(4)
    for idx, company in enumerate(companies):
        with cols[idx % 4]:
            st.info(f"**{company}**")

# CREATE PROFILE PAGE
elif "👤 Create Profile" in page:
    st.markdown('<div class="main-header">Create Your Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Tell us about yourself to get personalized recommendations</div>', unsafe_allow_html=True)
    
    with st.form("student_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Rahul Sharma")
            email = st.text_input("Email *", placeholder="rahul@university.edu")
            education = st.text_input("Education *", placeholder="B.Tech in Computer Science")
            gpa = st.number_input("GPA (out of 10) *", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        
        with col2:
            experience_months = st.number_input("Experience (months) *", min_value=0, max_value=120, value=0, step=1)
            preferred_locations = st.multiselect(
                "Preferred Locations *",
                options=stats['locations'],
                default=["Bangalore, Karnataka"]
            )
        
        # Skills
        st.markdown("### Skills")
        st.info("💡 Tip: Select skills you're confident in. Quality over quantity!")
        
        # Popular skills organized by category
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Programming**")
            prog_skills = st.multiselect(
                "Select Programming Skills",
                ["Python", "Java", "JavaScript", "C++", "Go", "Rust", "SQL"],
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Frameworks & Tools**")
            framework_skills = st.multiselect(
                "Select Frameworks",
                ["React", "Angular", "Node.js", "Django", "Flask", "Spring Boot", "Docker", "Kubernetes"],
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**Data & ML**")
            data_skills = st.multiselect(
                "Select Data/ML Skills",
                ["Machine Learning", "Deep Learning", "Data Analysis", "Statistics", "TensorFlow", "PyTorch", "Pandas", "NumPy"],
                label_visibility="collapsed"
            )
        
        # Additional skills
        other_skills = st.text_input(
            "Other Skills (comma-separated)",
            placeholder="Git, Agile, UI/UX, etc."
        )
        
        # Combine all skills
        all_skills = prog_skills + framework_skills + data_skills
        if other_skills:
            all_skills.extend([s.strip() for s in other_skills.split(',')])
        
        # Interests
        st.markdown("### Interests")
        interests = st.multiselect(
            "What areas interest you? *",
            ["Artificial Intelligence", "Web Development", "Mobile Apps", "Data Science",
             "Cloud Computing", "Cybersecurity", "Blockchain", "IoT", "AR/VR",
             "Product Management", "UI/UX Design", "DevOps", "Game Development"]
        )
        
        # Career goals
        st.markdown("### Career Goals")
        career_goals = st.text_area(
            "What are your career aspirations? *",
            placeholder="I want to become a Machine Learning Engineer at a top tech company, working on cutting-edge AI solutions...",
            height=100
        )
        import PyPDF2

        st.markdown("### 📄 Upload Resume (Optional)")
        uploaded_resume = st.file_uploader("Upload PDF Resume", type=["pdf"])

        resume_text = ""

        if uploaded_resume:
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            st.success("Resume uploaded successfully!")
        # Submit
        submit = st.form_submit_button("🎯 Get My Recommendations", type="primary", use_container_width=True)
        
        if submit:
            if not all([name, email, education, all_skills, interests, career_goals]):
                st.error("⚠️ Please fill in all required fields marked with *")
            else:
                # Create profile
                profile = {
                    'name': name,
                    'email': email,
                    'education': education,
                    'gpa': gpa,
                    'experience_months': experience_months,
                    'preferred_locations': preferred_locations,
                    'skills': all_skills,
                    'interests': interests,
                    'career_goals': career_goals,
                    'created_at': datetime.now().isoformat()
                }
                
                st.session_state.student_profile = profile
                # ===== RESUME ANALYSIS =====
                if uploaded_resume:
                    resume_lower = resume_text.lower()

                    matched_skills = [skill for skill in all_skills if skill.lower() in resume_lower]
                    missing_skills = [skill for skill in all_skills if skill.lower() not in resume_lower]

                    resume_score = int((len(matched_skills) / max(len(all_skills),1)) * 100)

                    st.markdown("### 📄 Resume Analysis")
                    st.metric("Resume Match Score", f"{resume_score}%")

                    if missing_skills:
                        st.warning(f"Consider adding these skills in your resume: {', '.join(missing_skills[:5])}")
                # Calculate profile strength
                strength = calculate_profile_strength(profile)
                
                # Generate recommendations
                with st.spinner("🤖 AI is analyzing your profile and matching internships..."):
                    recommendations = recommender.recommend(profile, all_internships, top_k=10)
                    st.session_state.recommendations = recommendations
                
                st.success(f"✅ Profile created successfully! Found {len(recommendations)} matching internships.")
                st.balloons()
                
                # Show profile strength
                st.markdown("### 📊 Profile Strength")
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    st.progress(strength['percentage'] / 100)
                with col2:
                    st.metric("Score", f"{strength['score']}/{strength['max_score']}")
                with col3:
                    st.metric("Rating", strength['rating'])
                
                if strength['feedback']:
                    with st.expander("💡 Tips to Improve Your Profile"):
                        for tip in strength['feedback']:
                            st.write(f"• {tip}")
                
                st.info("👉 Go to **Recommendations** page to see your matches!")

# RECOMMENDATIONS PAGE
elif "🎯 Recommendations" in page:
    st.markdown('<div class="main-header">Your Personalized Recommendations</div>', unsafe_allow_html=True)
    
    if st.session_state.recommendations is None:
        st.warning("⚠️ No recommendations yet. Please create your profile first!")
        if st.button("Create Profile Now"):
            st.switch_page("pages/01_Create_Profile.py")
    else:
        recommendations = st.session_state.recommendations
        profile = st.session_state.student_profile
        
        st.markdown(f'<div class="sub-header">Hi {profile["name"]}! We found {len(recommendations)} perfect matches for you</div>', unsafe_allow_html=True)
        
        # Filters
        with st.expander("🔍 Filter Recommendations"):
            col1, col2, col3 = st.columns(3)
            with col1:
                min_score = st.slider("Minimum Match Score (%)", 0, 100, 50)
            with col2:
                locations = st.multiselect("Locations", list(set(r['location'] for r in recommendations)))
            with col3:
                min_stipend = st.number_input("Min Stipend (₹)", min_value=0, value=0, step=5000)
        
        # Apply filters
        filtered_recs = [
            r for r in recommendations
            if r['match_percentage'] >= min_score
            and (not locations or r['location'] in locations)
            and r['stipend'] >= min_stipend
        ]
        
        st.info(f"Showing {len(filtered_recs)} internships")
        
        # Display recommendations
        for idx, rec in enumerate(filtered_recs, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {idx}. {rec['company']}")
                    st.markdown(f"**{rec['title']}**")
                    st.markdown(f"📍 {rec['location']} • 💰 ₹{rec['stipend']:,}/month • ⏱️ {rec['duration_months']} months")
                
                with col2:
                    st.markdown(f'<div class="match-score">{rec["match_percentage"]}%</div>', unsafe_allow_html=True)
                    st.markdown("<small>Match Score</small>", unsafe_allow_html=True)
                    st.markdown(f'<div class="success-badge">{int(rec["success_probability"]*100)}% Success Rate</div>', unsafe_allow_html=True)
                
                # Match reasons
                st.markdown("#### ✨ Why This Matches")
                for reason in rec['match_reasons']:
                    st.markdown(f"- {reason}")
                
                # Skill gaps
                if rec['skill_gaps']:
                    st.markdown("#### 📚 Skills to Learn")
                    gaps_html = " ".join([f'<span class="skill-tag skill-gap">{gap}</span>' for gap in rec['skill_gaps']])
                    st.markdown(gaps_html, unsafe_allow_html=True)
                if rec['skill_gaps']:
                    st.markdown("### 🛣 Personalized 4-Week Roadmap")
                    roadmap = generate_roadmap(rec['skill_gaps'])
    
                    for week, task in roadmap.items():
                        st.write(f"**{week}:** {task}")
                # Details expander
                with st.expander("📋 Full Job Description"):
                    st.markdown(f"**Description:** {rec['description']}")
                    st.markdown(f"**Department:** {rec['department']}")
                    st.markdown(f"**Required Skills:** {', '.join(rec['required_skills'])}")
                    if rec.get('preferred_skills'):
                        st.markdown(f"**Preferred Skills:** {', '.join(rec['preferred_skills'])}")
                    st.markdown(f"**Experience Required:** {rec['experience_required']} months")
                    st.markdown(f"**Posted:** {rec.get('posted_date', 'Recent')}")
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"🚀 Apply Now", key=f"apply_{idx}", type="primary")
                with col2:
                    st.button(f"💾 Save for Later", key=f"save_{idx}")
                with col3:
                    st.button(f"📤 Share", key=f"share_{idx}")
                
                st.markdown("---")

# ANALYTICS PAGE  
elif "📊 Analytics" in page:
    st.markdown('<div class="main-header">Platform Analytics</div>', unsafe_allow_html=True)
    
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Internships", stats['total_internships'])
    col2.metric("Companies Hiring", stats['total_companies'])
    col3.metric("Locations", stats['total_locations'])
    col4.metric("Avg Stipend", f"₹{stats['avg_stipend']:,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Skills demand
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Most In-Demand Skills")
        top_skills = stats['top_skills'][:15]
        skill_counts = list(range(len(top_skills), 0, -1))
        
        fig = px.bar(
            y=top_skills,
            x=skill_counts,
            orientation='h',
            labels={'x': 'Demand Level', 'y': 'Skill'},
            color=skill_counts,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Stipend Distribution")
        stipends = [i['stipend'] for i in all_internships]
        
        fig = px.histogram(
            stipends,
            nbins=15,
            labels={'value': 'Stipend (₹)', 'count': 'Number of Internships'},
            color_discrete_sequence=['#6366f1']
        )
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Location distribution
    st.subheader("📍 Internships by Location")
    location_counts = {}
    for internship in all_internships:
        loc = internship['location'].split(',')[0]  # Get city
        location_counts[loc] = location_counts.get(loc, 0) + 1
    
    fig = px.pie(
        values=list(location_counts.values()),
        names=list(location_counts.keys()),
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)

# BROWSE INTERNSHIPS PAGE
elif "💼 Browse Internships" in page:
    st.markdown('<div class="main-header">Browse All Internships</div>', unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by company, title, or skills...")
    with col2:
        location_filter = st.multiselect("Location", stats['locations'])
    with col3:
        min_stipend_filter = st.number_input("Min Stipend", min_value=0, value=0, step=5000)
    
    # Filter internships
    filtered = all_internships
    
    if search:
        search_lower = search.lower()
        filtered = [
            i for i in filtered
            if search_lower in i['company'].lower()
            or search_lower in i['title'].lower()
            or any(search_lower in skill.lower() for skill in i['required_skills'])
        ]
    
    if location_filter:
        filtered = [i for i in filtered if i['location'] in location_filter]
    
    if min_stipend_filter > 0:
        filtered = [i for i in filtered if i['stipend'] >= min_stipend_filter]
    
    st.info(f"Showing {len(filtered)} of {len(all_internships)} internships")
    
    # Display as table
    df = pd.DataFrame(filtered)
    df = df[['company', 'title', 'location', 'stipend', 'duration_months', 'department']]
    df = df.rename(columns={
        'company': 'Company',
        'title': 'Title',
        'location': 'Location',
        'stipend': 'Stipend (₹)',
        'duration_months': 'Duration (months)',
        'department': 'Department'
    })
    
    st.dataframe(df, use_container_width=True, height=600)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="internships.csv",
        mime="text/csv"
    )

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🎯 AI Internship Recommender**")
with col2:
    st.markdown("Built for PM Internship Scheme")
with col3:
    st.markdown("Made    with     ❤️ ")
