"""
AI Recommendation Engine - Optimized for Streamlit
Multi-factor intelligent matching system
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import Counter
import re

class InternshipRecommender:
    """
    Smart recommendation engine using multi-factor analysis
    """
    
    def __init__(self):
        # Configurable weights for different matching factors
        self.weights = {
            'skills_match': 0.35,
            'interest_alignment': 0.20,
            'experience_fit': 0.15,
            'location_match': 0.15,
            'career_goals': 0.15
        }
        
        # Skill similarity mappings (for better matching)
        self.skill_synonyms = {
            'ml': ['machine learning', 'deep learning', 'ai'],
            'python': ['pandas', 'numpy', 'scikit-learn'],
            'java': ['spring', 'spring boot', 'hibernate'],
            'web': ['html', 'css', 'javascript', 'react', 'angular', 'vue'],
            'mobile': ['android', 'ios', 'react native', 'flutter'],
            'data': ['sql', 'postgresql', 'mysql', 'mongodb'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
        }
        
        print("✅ Recommendation engine initialized")
    
    def recommend(
        self,
        student_profile: Dict,
        all_internships: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Generate top-k personalized recommendations
        
        Args:
            student_profile: Student's profile with skills, interests, etc.
            all_internships: List of all available internships
            top_k: Number of top recommendations to return
            
        Returns:
            List of recommended internships with scores and explanations
        """
        recommendations = []
        
        for internship in all_internships:
            # Calculate overall match score
            score, breakdown = self._calculate_match_score(student_profile, internship)
            
            if score > 0.3:  # Minimum threshold
                # Generate explanation
                reasons = self._generate_match_reasons(breakdown, student_profile, internship)
                
                # Identify skill gaps
                gaps = self._identify_skill_gaps(
                    student_profile.get('skills', []),
                    internship['required_skills']
                )
                
                # Success probability
                success_prob = self._calculate_success_probability(score, breakdown)
                
                recommendations.append({
                    **internship,
                    'match_score': round(score, 3),
                    'match_percentage': round(score * 100, 1),
                    'match_reasons': reasons,
                    'skill_gaps': gaps,
                    'success_probability': round(success_prob, 3),
                    'breakdown': breakdown
                })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_k]
    
    def _calculate_match_score(
        self,
        student: Dict,
        internship: Dict
    ) -> Tuple[float, Dict]:
        """Calculate weighted match score with breakdown"""
        
        breakdown = {}
        
        # 1. Skills matching (35%)
        skills_score = self._match_skills(
            student.get('skills', []),
            internship['required_skills'],
            internship.get('preferred_skills', [])
        )
        breakdown['skills_match'] = skills_score
        
        # 2. Interest alignment (20%)
        interest_score = self._match_interests(
            student.get('interests', []),
            internship['description'],
            internship.get('department', '')
        )
        breakdown['interest_alignment'] = interest_score
        
        # 3. Experience fit (15%)
        exp_score = self._match_experience(
            student.get('experience_months', 0),
            student.get('education', ''),
            internship.get('experience_required', 0)
        )
        breakdown['experience_fit'] = exp_score
        
        # 4. Location match (15%)
        location_score = self._match_location(
            student.get('preferred_locations', []),
            internship.get('location', '')
        )
        breakdown['location_match'] = location_score
        
        # 5. Career goals alignment (15%)
        career_score = self._match_career_goals(
            student.get('career_goals', ''),
            internship['title'],
            internship['description']
        )
        breakdown['career_goals'] = career_score
        
        # Calculate weighted sum
        total_score = sum(
            breakdown[key] * self.weights[key]
            for key in self.weights.keys()
        )
        
        return total_score, breakdown
    
    def _match_skills(
        self,
        student_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str]
    ) -> float:
        """Match student skills with job requirements"""
        
        # Normalize to lowercase
        student_set = set(s.lower().strip() for s in student_skills)
        required_set = set(s.lower().strip() for s in required_skills)
        preferred_set = set(s.lower().strip() for s in preferred_skills)
        
        # Expand skills using synonyms
        expanded_student = self._expand_skills(student_set)
        
        # Required skills match (70% weight)
        if required_set:
            required_matches = len(expanded_student & required_set)
            required_score = min(required_matches / len(required_set), 1.0)
        else:
            required_score = 1.0
        
        # Preferred skills match (30% weight)
        if preferred_set:
            preferred_matches = len(expanded_student & preferred_set)
            preferred_score = min(preferred_matches / len(preferred_set), 1.0)
        else:
            preferred_score = 1.0
        
        return 0.7 * required_score + 0.3 * preferred_score
    
    def _expand_skills(self, skills: set) -> set:
        """Expand skills using synonyms for better matching"""
        expanded = set(skills)
        
        for skill in skills:
            for category, synonyms in self.skill_synonyms.items():
                if skill in synonyms or category in skill:
                    expanded.update(synonyms)
        
        return expanded
    
    def _match_interests(
        self,
        student_interests: List[str],
        job_description: str,
        department: str
    ) -> float:
        """Match student interests with job content"""
        
        if not student_interests:
            return 0.6  # Neutral score
        
        # Combine job text
        job_text = f"{job_description} {department}".lower()
        
        # Count matches
        matches = sum(
            1 for interest in student_interests
            if interest.lower() in job_text
        )
        
        return min(matches / max(len(student_interests), 1), 1.0)
    
    def _match_experience(
        self,
        student_exp: int,
        education: str,
        required_exp: int
    ) -> float:
        """Match experience level"""
        
        # Education boost
        education_boost = 0.0
        edu_lower = education.lower()
        if 'master' in edu_lower or 'phd' in edu_lower or 'm.tech' in edu_lower:
            education_boost = 0.25
        elif 'bachelor' in edu_lower or 'b.tech' in edu_lower or 'b.e' in edu_lower:
            education_boost = 0.15
        
        # Experience matching
        if required_exp == 0:
            # Entry level - everyone qualifies
            exp_score = 1.0
        elif student_exp >= required_exp:
            # Meets or exceeds requirement
            exp_score = 1.0
        else:
            # Partial match - linear scaling
            exp_score = student_exp / max(required_exp, 1)
        
        return min(exp_score + education_boost, 1.0)
    
    def _match_location(
        self,
        preferred_locations: List[str],
        job_location: str
    ) -> float:
        """Match location preferences"""
        
        if not preferred_locations:
            return 0.7  # Neutral if no preference
        
        job_loc_lower = job_location.lower()
        
        for pref_loc in preferred_locations:
            pref_lower = pref_loc.lower()
            # Check for city name match
            if pref_lower in job_loc_lower or job_loc_lower in pref_lower:
                return 1.0
            # Check for state match
            if any(city in job_loc_lower for city in ['bangalore', 'bengaluru']) and \
               any(city in pref_lower for city in ['bangalore', 'bengaluru', 'karnataka']):
                return 1.0
        
        # Check if "Remote" or "Multiple Locations"
        if 'remote' in job_loc_lower or 'multiple' in job_loc_lower:
            return 0.9
        
        return 0.3  # Low but not zero
    
    def _match_career_goals(
        self,
        career_goals: str,
        job_title: str,
        job_description: str
    ) -> float:
        """Match career aspirations"""
        
        if not career_goals:
            return 0.5  # Neutral
        
        # Extract keywords from career goals
        goal_keywords = set(career_goals.lower().split())
        
        # Extract from job
        job_text = f"{job_title} {job_description}".lower()
        job_keywords = set(job_text.split())
        
        # Calculate overlap
        common = goal_keywords & job_keywords
        if not goal_keywords:
            return 0.5
        
        overlap_score = len(common) / len(goal_keywords)
        
        return min(overlap_score * 2, 1.0)  # Scale up a bit
    
    def _identify_skill_gaps(
        self,
        student_skills: List[str],
        required_skills: List[str]
    ) -> List[str]:
        """Identify missing skills"""
        
        student_set = set(s.lower().strip() for s in student_skills)
        required_set = set(s.lower().strip() for s in required_skills)
        
        # Expand student skills
        expanded_student = self._expand_skills(student_set)
        
        # Find gaps
        gaps = list(required_set - expanded_student)
        
        return gaps
    
    def _calculate_success_probability(self, match_score: float, breakdown: Dict) -> float:
        """Estimate application success probability"""
        
        # Base probability from match score
        base_prob = match_score * 0.75
        
        # Bonus for strong skills match
        if breakdown.get('skills_match', 0) > 0.8:
            base_prob += 0.15
        
        # Bonus for experience fit
        if breakdown.get('experience_fit', 0) > 0.8:
            base_prob += 0.10
        
        return min(base_prob, 0.95)  # Cap at 95%
    
    def _generate_match_reasons(
        self,
        breakdown: Dict,
        student: Dict,
        internship: Dict
    ) -> List[str]:
        """Generate human-readable match reasons"""
        
        reasons = []
        
        # Skills
        if breakdown.get('skills_match', 0) > 0.7:
            matched_skills = set(s.lower() for s in student.get('skills', [])) & \
                           set(s.lower() for s in internship['required_skills'])
            if matched_skills:
                skill_list = ', '.join(list(matched_skills)[:3])
                reasons.append(f"✅ Strong skill match: {skill_list}")
        
        # Experience
        if breakdown.get('experience_fit', 0) > 0.8:
            exp = student.get('experience_months', 0)
            if exp > 0:
                reasons.append(f"✅ Your {exp} months experience aligns well")
            else:
                reasons.append(f"✅ Perfect for entry-level candidates")
        
        # Location
        if breakdown.get('location_match', 0) > 0.9:
            reasons.append(f"✅ Matches your location preference")
        
        # Career goals
        if breakdown.get('career_goals', 0) > 0.6:
            reasons.append(f"✅ Aligns with your career aspirations")
        
        # Company prestige
        top_companies = ['google', 'microsoft', 'amazon', 'meta', 'apple']
        if any(company in internship['company'].lower() for company in top_companies):
            reasons.append(f"🌟 Top-tier company: {internship['company']}")
        
        # High stipend
        if internship.get('stipend', 0) >= 50000:
            reasons.append(f"💰 Competitive stipend: ₹{internship['stipend']:,}/month")
        
        return reasons[:5]  # Top 5 reasons

def calculate_profile_strength(student: Dict) -> Dict:
    """Calculate student profile strength score"""
    
    score = 0
    max_score = 100
    feedback = []
    
    # Skills (30 points)
    skills = student.get('skills', [])
    skill_points = min(len(skills) * 5, 30)
    score += skill_points
    if len(skills) < 5:
        feedback.append(f"Add more skills (currently {len(skills)})")
    
    # Experience (20 points)
    exp = student.get('experience_months', 0)
    exp_points = min(exp / 2, 20)
    score += exp_points
    if exp == 0:
        feedback.append("Consider adding internship/project experience")
    
    # Education (15 points)
    if student.get('education'):
        score += 15
    else:
        feedback.append("Add education details")
    
    # Career goals (15 points)
    goals = student.get('career_goals', '')
    if len(goals) > 50:
        score += 15
    elif len(goals) > 20:
        score += 10
        feedback.append("Expand your career goals description")
    else:
        feedback.append("Add detailed career goals")
    
    # Interests (10 points)
    interests = student.get('interests', [])
    score += min(len(interests) * 3, 10)
    if len(interests) < 3:
        feedback.append("Add more interests")
    
    # GPA (10 points)
    gpa = student.get('gpa', 0)
    if gpa >= 8.0:
        score += 10
    elif gpa >= 7.0:
        score += 7
    elif gpa > 0:
        score += 5
    
    return {
        'score': round(score, 1),
        'max_score': max_score,
        'percentage': round((score / max_score) * 100, 1),
        'feedback': feedback,
        'rating': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Average'
    }
