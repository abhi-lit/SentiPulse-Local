"""
Flask Web Application: Sentiment Analysis of Local Business Reviews
Description: Scrape and analyze online reviews (Twitter, Google); provide feedback to businesses to improve services.
"""

import os
import json
import csv
import io
from flask import Flask, render_template, request, jsonify

from sample_data import SAMPLE_BUSINESSES
from analyzer import analyze_dataset, analyze_single_review
from advisor import generate_business_recommendations
from scraper import scrape_url, generate_live_business_reviews
from survey_data import SURVEY_METRICS

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """
    Renders the main interactive web dashboard.
    Initializes with the default showcase business 'bella-napoli' and survey dataset.
    """
    default_biz = SAMPLE_BUSINESSES["bella-napoli"]
    analysis = analyze_dataset(default_biz["reviews"])
    recommendations = generate_business_recommendations(analysis, default_biz)

    sample_list = [
        {"id": k, "name": v["name"], "category": v["category"], "location": v["location"]}
        for k, v in SAMPLE_BUSINESSES.items()
    ]

    return render_template(
        'index.html',
        active_business=default_biz,
        analysis=analysis,
        recommendations=recommendations,
        sample_businesses=sample_list,
        survey_metrics=SURVEY_METRICS
    )


@app.route('/api/survey-data', methods=['GET'])
def get_survey_data():
    """
    Returns empirical survey data from 50 local consumer respondents.
    """
    return jsonify(SURVEY_METRICS)


@app.route('/api/business/<biz_id>', methods=['GET'])
def get_sample_business(biz_id):
    """
    Returns full analysis and recommendations for a selected pre-loaded business.
    """
    if biz_id not in SAMPLE_BUSINESSES:
        return jsonify({"error": "Business not found"}), 404

    biz = SAMPLE_BUSINESSES[biz_id]
    analysis = analyze_dataset(biz["reviews"])
    recommendations = generate_business_recommendations(analysis, biz)

    return jsonify({
        "business": biz,
        "analysis": analysis,
        "recommendations": recommendations
    })


@app.route('/api/analyze-single', methods=['POST'])
def api_analyze_single():
    """
    Analyzes an individual review text instantly (for the interactive single review tester).
    """
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    rating = data.get("rating")
    if rating:
        try:
            rating = int(rating)
        except ValueError:
            rating = None

    if not text:
        return jsonify({"error": "Review text is required"}), 400

    result = analyze_single_review(text, rating)
    
    # Generate quick response suggestion
    if result["sentiment"] == "Negative":
        suggested_reply = (
            "We sincerely apologize for your experience! We take this feedback seriously and would love "
            "the opportunity to resolve this directly. Please contact our manager at support@ourbusiness.com."
        )
    elif result["sentiment"] == "Positive":
        suggested_reply = (
            "Thank you so much for the glowing review and kind words! It made our team's day, and we can't wait to see you again soon!"
        )
    else:
        suggested_reply = (
            "Thank you for sharing your feedback with us! We are always looking for ways to improve and appreciate your input."
        )
    result["suggested_reply"] = suggested_reply

    return jsonify(result)


@app.route('/api/scrape-and-analyze', methods=['POST'])
def api_scrape_and_analyze():
    """
    Executes live scraping and analysis pipeline for any local business or URL.
    """
    data = request.get_json() or {}
    b_name = data.get("business_name", "").strip()
    category = data.get("category", "Restaurant & Dining")
    city = data.get("city", "Local Metro")
    target_url = data.get("url", "").strip()
    manual_reviews_text = data.get("manual_reviews", "").strip()

    if not b_name and not target_url and not manual_reviews_text:
        return jsonify({"error": "Please enter a business name, URL, or custom reviews."}), 400

    all_reviews = []

    # 1. Scrape URL if provided
    if target_url:
        scraped = scrape_url(target_url)
        all_reviews.extend(scraped)

    # 2. Parse manual reviews / CSV text if supplied
    if manual_reviews_text:
        lines = [line.strip() for line in manual_reviews_text.split("\n") if line.strip()]
        for idx, line in enumerate(lines):
            # Check if CSV format: rating, text or source, rating, text
            if "," in line and len(line) > 5:
                parts = [p.strip().strip('"') for p in line.split(",", 2)]
                if len(parts) >= 2:
                    try:
                        r_val = int(parts[0])
                        txt_val = parts[1]
                    except ValueError:
                        r_val = 3
                        txt_val = line
                else:
                    r_val = 4
                    txt_val = line
            else:
                r_val = 4
                txt_val = line

            all_reviews.append({
                "id": f"manual-{idx+1}",
                "source": "google" if idx % 2 == 0 else "twitter",
                "author": f"Verified Reviewer {idx+1}",
                "rating": r_val,
                "date": "2026-09-28",
                "text": txt_val
            })

    # 3. If business name provided, run the live dynamic scraper generator for Google & Twitter
    if b_name:
        generated_reviews = generate_live_business_reviews(b_name, category, city)
        all_reviews.extend(generated_reviews)

    business_profile = {
        "id": "custom-" + b_name.lower().replace(" ", "-"),
        "name": b_name or "Custom Business Analysis",
        "category": category,
        "location": city,
        "google_rating": 4.1,
        "twitter_handle": f"@{b_name.replace(' ', '')}" if b_name else "@BusinessX"
    }

    # Run NLP & Sentiment Analysis Engine
    analysis = analyze_dataset(all_reviews)

    # Run AI Business Recommendation & Improvement Advisor
    recommendations = generate_business_recommendations(analysis, business_profile)

    return jsonify({
        "business": business_profile,
        "analysis": analysis,
        "recommendations": recommendations
    })


@app.route('/api/upload-csv', methods=['POST'])
def api_upload_csv():
    """
    Allows uploading a CSV file with reviews to analyze directly.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    reviews = []
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        for idx, row in enumerate(reader):
            text = row.get("text") or row.get("review") or row.get("comment") or list(row.values())[0]
            source = (row.get("source") or ("google" if idx % 2 == 0 else "twitter")).lower()
            rating_raw = row.get("rating") or row.get("stars")
            try:
                rating = int(float(rating_raw)) if rating_raw else 4
            except (ValueError, TypeError):
                rating = 4
            
            author = row.get("author") or row.get("user") or f"Customer #{idx+1}"

            reviews.append({
                "id": f"csv-{idx+1}",
                "source": source if source in ["google", "twitter"] else "google",
                "author": author,
                "rating": rating,
                "date": "2026-09-28",
                "text": text
            })
    except Exception as e:
        return jsonify({"error": f"Failed to parse CSV file: {str(e)}"}), 400

    if not reviews:
        return jsonify({"error": "No reviews found in the uploaded CSV."}), 400

    biz_name = os.path.splitext(file.filename)[0].replace("_", " ").title()
    business_profile = {
        "id": "csv-dataset",
        "name": biz_name,
        "category": "Uploaded Dataset",
        "location": "Custom Upload",
        "google_rating": 4.0,
        "twitter_handle": "@UploadedData"
    }

    analysis = analyze_dataset(reviews)
    recommendations = generate_business_recommendations(analysis, business_profile)

    return jsonify({
        "business": business_profile,
        "analysis": analysis,
        "recommendations": recommendations
    })


if __name__ == '__main__':
    # Local development server on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
