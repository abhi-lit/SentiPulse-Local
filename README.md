# SentiPulse-Local: Sentiment Analysis of Local Business Reviews

## Project Title
**Sentiment Analysis of Local Business Reviews**

## Project Description
> **Scrape and analyze online reviews (Twitter, Google); provide feedback to businesses to improve services.**

**SentiPulse Local** is an end-to-end web platform and NLP intelligence dashboard tailored for local business owners (restaurants, fitness clubs, dental clinics, retail, etc.). It automates scraping and aggregating reviews from **Google Reviews** and **Twitter / X**, conducts sentiment analysis and Aspect-Based Sentiment Analysis (ABSA), and synthesizes actionable operational recommendations to help businesses elevate service standards, resolve friction, and reduce customer churn.

---

## 🌟 Key Features & Capabilities

### 1. Multi-Source Scraping & Aggregation Engine
- **Google Reviews Scraper**: Gathers reviewer names, star ratings, dates, and full review text.
- **Twitter / X Scraper**: Scrapes mentions (`@handle`), hashtags (`#business`), customer tweets, and social sentiment.
- **Live Business Discovery**: Dynamically scrapes or generates realistic real-world review distributions for any local business name and category entered by the user.
- **Direct URL & CSV Batch Import**: Support for crawling specific review URLs or uploading CSV files directly.

### 2. Advanced NLP & Aspect-Based Sentiment Analysis (ABSA)
- **VADER Sentiment Engine**: Specifically designed for informal social media text, handling emojis, intensifiers, punctuation, and negations to calculate compound scores (-1.0 to +1.0) and classifications (Positive, Neutral, Negative).
- **Aspect-Based Sentiment Analysis (ABSA)**: Classifies sentiment across 6 business dimensions:
  - *Customer Service & Frontline Staff*
  - *Product / Food Quality*
  - *Pricing & Value for Money*
  - *Cleanliness & Ambience*
  - *Wait Time & Operational Speed*
  - *Delivery & Logistics*
- **Emotion & Tone Detection**: Automatically tags reviews with emotions such as *Delight / Joy*, *Frustration / Anger*, *Disappointment*, or *Appreciation / Trust*.
- **Key Customer Drivers & Friction Pain Points**: Real-time extraction of top recurring praises and complaints.

### 3. Automated AI Business Advisory & Service Improvement Center
- **Executive Satisfaction Grade**: Letter grading (A+, A, B, C, D) and Health Index (0–100%).
- **Prioritized Action Plan**: Ranked operational directives (High Priority / Red, Medium Operational / Amber, Growth / Green).
- **Automated Review Response Generator**: Pre-composed, empathetic, and professional review response templates for 1-star, 3-star, and 5-star customer feedback.
- **1-Click Review Reply Generator**: Drafts instant custom replies for any individual review card in the feed.
- **Single Review Playground**: Interactive sandbox to test any customer statement or tweet in real time.
- **Audit Export**: Printable format & 1-click JSON export for business owners and management presentations.

### 4. 🌌 Luxury Dark Theme & Interactive Mouse Hover Animations
- **Obsidian / Midnight Aesthetic (`#090d16`)**: Translucent glassmorphic cards (`rgba(17, 24, 39, 0.75)`) with subtle glowing borders.
- **Interactive Mouse Spotlight Follower**: A smooth, glowing ambient radial aura that follows the mouse cursor across the screen in real time.
- **3D Card Hover Tilt**: Moving the mouse over KPI cards, action plan cards, or survey cards dynamically tilts them in 3D perspective based on cursor coordinates.
- **Shimmer Light Sweep**: Hovering over cards triggers a subtle diagonal light sweep across the surface.
- **Button & Chip Hover Glow**: Buttons and tag chips lift, scale, and cast luminous glowing drop shadows.

### 5. 📈 Field Consumer Survey Analytics (50 Respondents)
- **Verified Empirical Dataset**: Analysis of 50 local consumer survey responses across 11 question categories.
- **Key Empirical Findings**:
  - **86%** check online reviews prior to visiting a local business.
  - **65.3%** rate Google reviews as important or very important.
  - **64%** cite long waiting times (34%) and high prices (30%) as their primary frustration.
  - **26%** abandon a business permanently after a bad experience, while **60%** can be retained through swift service recovery.
- **11 Interactive Donut Charts**: Rendered with Chart.js with matching color palettes and project relevance notes.
- **Interactive Category Filtering**: Filter survey questions by Demographics, Review Habits, Review Factors, Pain Points, and Service Recovery.
- **Dedicated REST API**: `GET /api/survey-data` returns the complete survey JSON dataset.

---

## 🏗️ Architecture & File Structure

```
d:\field project\
├── app.py                 # Main Flask web application & REST API routes
├── scraper.py             # Google Reviews & Twitter/X scrapers and discovery engine
├── analyzer.py            # VADER & Aspect-Based Sentiment NLP engine
├── advisor.py             # AI Business feedback & recommendation generator
├── sample_data.py         # Showcase datasets (Restaurant, Gym, Dental Clinic)
├── survey_data.py         # 50-respondent empirical survey dataset (11 questions)
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file (cache, temp files)
├── templates/
│   └── index.html         # Responsive tabbed dashboard (Dark luxury theme)
└── static/
    ├── css/
    │   └── style.css      # Dark theme styling, ambient glow, 3D tilt, print CSS
    └── js/
        └── main.js        # Chart.js visualization, filters, modals, mouse spotlight & tilt
```

---

## 🚀 Getting Started

### 1. Requirements
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```

### 4. Open in Browser
Open your browser and navigate to:
```
http://localhost:5000
```
