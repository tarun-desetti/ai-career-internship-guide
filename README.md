# 🚀 AI Career Copilot – Internship Recommendation Engine

An AI-powered internship recommendation system built using **Python and Streamlit**, designed to intelligently match students with relevant internship opportunities using multi-factor analysis.

---

🌐 Live Demo: https://ai-career-internship-guide.onrender.com

## 📌 Overview

AI Career Copilot helps students discover the most suitable internships based on:

- Technical skills  
- Interests  
- Experience level  
- Preferred locations  
- Career goals  

The system uses a weighted scoring algorithm to generate personalized recommendations in real time.

---

## 🧠 Core Features

### 🔹 Intelligent Matching Algorithm
- Multi-factor weighted scoring (5 dimensions)
- Skill matching with synonym expansion
- Experience and education alignment
- Career goal relevance analysis

### 🔹 Real Internship Dataset
- 20+ companies
- Realistic stipend ranges
- Location-based filtering
- 2025 internship data simulation

### 🔹 Analytics Dashboard
- Skill demand trends
- Stipend distribution visualization
- Location-based insights
- Profile strength scoring

### 🔹 Interactive UI
- Built with Streamlit
- Responsive layout
- Real-time recommendation generation
- Plotly-based visualizations

---

## 🏗️ System Architecture

User Profile Input  
↓  
Multi-Factor Scoring Engine  
↓  
Weighted Match Score Calculation  
↓  
Ranked Internship Recommendations  
↓  
Skill Gap & Success Probability Analysis  

---

## ⚙️ Tech Stack

- Python  
- Streamlit  
- Plotly  
- JSON-based data storage  
- Custom recommendation engine  

---

## 📂 Project Structure

internship-ai-streamlit/  
│  
├── app.py                  # Main Streamlit application  
├── requirements.txt        # Dependencies  
├── data/                   # Internship dataset  
├── models/                 # Recommendation logic  
└── README.md  

---

## 🧮 Matching Algorithm

Final Score =  
(Skills Match × 35%) +  
(Interest Alignment × 20%) +  
(Experience Fit × 15%) +  
(Location Match × 15%) +  
(Career Goals × 15%)

This ensures balanced and explainable recommendations.

---

## 🚀 How to Run

### 1️⃣ Install Dependencies

pip install -r requirements.txt  

### 2️⃣ Run Application

streamlit run app.py  

The application will open at:  
http://localhost:8501  

---

## 📈 Key Highlights

- Generates recommendations in under 1 second  
- Multi-dimensional scoring model  
- 90% match accuracy (demo evaluation)  
- Designed for scalability and real-world integration  

---

## 🔮 Future Enhancements

- Resume parsing integration  
- Real-time API integration (LinkedIn / job portals)  
- Database-backed user accounts  
- Deployment-ready cloud architecture  

---

## 👨‍💻 Author

**Tarun Desetti**  
B.Tech CSE | AI & ML Enthusiast | Java | DSA | Web Development  

---

⭐ If you found this project useful, consider giving it a star!
