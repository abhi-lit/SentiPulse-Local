"""
Field Research & Survey Data: Sentiment Analysis of Local Business Reviews
Dataset compiled from 50 local consumer survey responses.
Contains 11 survey questions covering demographics, review-checking habits,
pain points, feedback focus, customer churn, and service improvement needs.
"""

SURVEY_METRICS = {
    "total_respondents": 50,
    "survey_title": "Local Business Reviews & Consumer Experience Field Study",
    "key_takeaways": [
        {
            "stat": "86%",
            "label": "Check Reviews Prior to Visiting",
            "desc": "Consumers consistently rely on online feedback (Google & Twitter) before choosing a local business."
        },
        {
            "stat": "65.3%",
            "label": "Rate Google Reviews as Crucial",
            "desc": "40.8% find them Important and 24.5% Very Important in their purchasing decision."
        },
        {
            "stat": "64%",
            "label": "Cite Delays & High Prices as #1 Frustration",
            "desc": "Long waiting times (34%) and high prices (30%) constitute the vast majority of local business grievances."
        },
        {
            "stat": "26%",
            "label": "Permanent Churn Risk on Bad Service",
            "desc": "Over a quarter of customers abandon businesses after bad experiences, while 60% can be retained with proper service recovery."
        }
    ],
    "questions": [
        {
            "id": "q1_occupation",
            "category": "demographics",
            "title": "What is your occupation?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Student", "percentage": 50.0, "color": "#f59e0b"},
                {"label": "Business / Self-employed", "percentage": 32.0, "color": "#3b82f6"},
                {"label": "Working Professional", "percentage": 14.0, "color": "#ef4444"},
                {"label": "Other", "percentage": 4.0, "color": "#10b981"}
            ],
            "insight": "Half the respondents are students, followed by 32% self-employed/business owners who are highly active online."
        },
        {
            "id": "q2_age_group",
            "category": "demographics",
            "title": "What is your age group?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "18 to 25", "percentage": 78.0, "color": "#3b82f6"},
                {"label": "26 to 40", "percentage": 16.0, "color": "#ef4444"},
                {"label": "41 to 60", "percentage": 4.0, "color": "#f59e0b"},
                {"label": "Above 60", "percentage": 2.0, "color": "#10b981"}
            ],
            "insight": "78% belong to the 18–25 age bracket, representing digitally native consumers who consult social media and Google first."
        },
        {
            "id": "q3_check_frequency",
            "category": "habits",
            "title": "How often do you check online reviews before visiting a business?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Sometimes", "percentage": 38.0, "color": "#f59e0b"},
                {"label": "Always", "percentage": 28.0, "color": "#3b82f6"},
                {"label": "Often", "percentage": 20.0, "color": "#ef4444"},
                {"label": "Never", "percentage": 12.0, "color": "#a855f7"},
                {"label": "Rarely", "percentage": 2.0, "color": "#10b981"}
            ],
            "insight": "86% check online reviews (Always 28%, Often 20%, Sometimes 38%), validating the critical need for sentiment monitoring."
        },
        {
            "id": "q4_google_importance",
            "category": "habits",
            "title": "How important are Google reviews when choosing a business?",
            "responses_count": 49,
            "chart_type": "doughnut",
            "data": [
                {"label": "Important", "percentage": 40.8, "color": "#ef4444"},
                {"label": "Neutral", "percentage": 30.6, "color": "#f59e0b"},
                {"label": "Very Important", "percentage": 24.5, "color": "#3b82f6"},
                {"label": "Less Important", "percentage": 2.0, "color": "#10b981"},
                {"label": "Not Important", "percentage": 2.1, "color": "#a855f7"}
            ],
            "insight": "65.3% consider Google reviews important or very important when deciding which local establishment to visit."
        },
        {
            "id": "q5_important_factor",
            "category": "factors",
            "title": "What is the most important factor when reviewing a local business?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Product Quality", "percentage": 32.0, "color": "#10b981"},
                {"label": "Staff Behavior", "percentage": 32.0, "color": "#ef4444"},
                {"label": "Service Quality", "percentage": 24.0, "color": "#3b82f6"},
                {"label": "Pricing Concerns", "percentage": 6.0, "color": "#f59e0b"},
                {"label": "Cleanliness", "percentage": 6.0, "color": "#a855f7"}
            ],
            "insight": "Product Quality (32%) and Staff Behavior (32%) dominate customer review criteria, followed by Service Quality (24%)."
        },
        {
            "id": "q6_recent_experience",
            "category": "experience",
            "title": "How would you describe your recent experience with the business?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Neutral", "percentage": 44.0, "color": "#f59e0b"},
                {"label": "Positive", "percentage": 36.0, "color": "#ef4444"},
                {"label": "Very Positive", "percentage": 16.0, "color": "#3b82f6"},
                {"label": "Very Negative", "percentage": 4.0, "color": "#a855f7"}
            ],
            "insight": "52% experienced positive visits, but a large 44% reported neutral experiences—prime targets for service optimization."
        },
        {
            "id": "q7_common_problem",
            "category": "pain_points",
            "title": "What is the most common problem you face with local businesses?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Long Waiting Time", "percentage": 34.0, "color": "#f59e0b"},
                {"label": "High Prices", "percentage": 30.0, "color": "#ef4444"},
                {"label": "Poor Service", "percentage": 16.0, "color": "#3b82f6"},
                {"label": "Product Quality", "percentage": 12.0, "color": "#a855f7"},
                {"label": "Staff Behavior", "percentage": 8.0, "color": "#10b981"}
            ],
            "insight": "Waiting time (34%) and pricing (30%) constitute 64% of grievances, directly guiding our AI operational recommendations."
        },
        {
            "id": "q8_business_response",
            "category": "service_recovery",
            "title": "Do you think businesses respond properly to customer reviews?",
            "responses_count": 49,
            "chart_type": "doughnut",
            "data": [
                {"label": "Sometimes", "percentage": 36.7, "color": "#f59e0b"},
                {"label": "Always", "percentage": 30.6, "color": "#3b82f6"},
                {"label": "Often", "percentage": 18.4, "color": "#ef4444"},
                {"label": "Rarely", "percentage": 8.2, "color": "#10b981"},
                {"label": "Never", "percentage": 6.1, "color": "#a855f7"}
            ],
            "insight": "Over 51% feel businesses respond inconsistently (Sometimes 36.7%, Rarely 8.2%, Never 6.1%), showing the need for automated reply drafts."
        },
        {
            "id": "q9_feedback_focus",
            "category": "service_recovery",
            "title": "What type of feedback should businesses focus on most?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Product Quality", "percentage": 32.0, "color": "#f59e0b"},
                {"label": "Customer Complaints", "percentage": 28.0, "color": "#3b82f6"},
                {"label": "Service Quality", "percentage": 28.0, "color": "#ef4444"},
                {"label": "Staff Behavior", "percentage": 6.0, "color": "#10b981"},
                {"label": "Pricing", "percentage": 6.0, "color": "#a855f7"}
            ],
            "insight": "Customers urge businesses to prioritize resolving complaints (28%) and boosting product & service quality (60%)."
        },
        {
            "id": "q10_negative_retention",
            "category": "service_recovery",
            "title": "Would you continue using a business after a negative experience?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Probably Yes", "percentage": 34.0, "color": "#ef4444"},
                {"label": "Not Sure", "percentage": 26.0, "color": "#f59e0b"},
                {"label": "Probably No", "percentage": 18.0, "color": "#10b981"},
                {"label": "Definitely Yes", "percentage": 14.0, "color": "#3b82f6"},
                {"label": "Definitely No", "percentage": 8.0, "color": "#a855f7"}
            ],
            "insight": "26% will abandon the business (Probably/Definitely No). 60% (Probably Yes + Not Sure) can be retained if businesses reach out promptly."
        },
        {
            "id": "q11_improvement_areas",
            "category": "pain_points",
            "title": "What would improve your overall experience with a local business?",
            "responses_count": 50,
            "chart_type": "doughnut",
            "data": [
                {"label": "Better Service", "percentage": 38.0, "color": "#3b82f6"},
                {"label": "Better Customer Support", "percentage": 24.0, "color": "#ef4444"},
                {"label": "Lower Prices", "percentage": 24.0, "color": "#f59e0b"},
                {"label": "Better Product Quality", "percentage": 8.0, "color": "#a855f7"},
                {"label": "Faster Service", "percentage": 6.0, "color": "#10b981"}
            ],
            "insight": "Better service (38%) and customer support (24%) are the top demands, accounting for 62% of consumer improvement desires."
        }
    ]
}
