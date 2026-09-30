"""
NLP & Sentiment Analysis Engine for Local Business Reviews
Features:
- VADER Sentiment Intensity Analysis (Compound, Pos, Neu, Neg)
- Aspect-Based Sentiment Analysis (Customer Service, Quality, Pricing, Ambience, Speed, Delivery)
- Emotion / Tone Detection (Satisfaction, Frustration, Disappointment, Appreciation)
- Key Drivers & Pain Points Extraction
"""

import re
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Domain aspects dictionary with trigger keywords
ASPECT_KEYWORDS = {
    "Customer Service": [
        "service", "staff", "waiter", "waitress", "server", "hostess", "receptionist",
        "manager", "employee", "team", "trainer", "doctor", "hygienist", "helpful",
        "rude", "friendly", "polite", "courteous", "attitude", "attentive", "patient"
    ],
    "Product / Food Quality": [
        "quality", "food", "taste", "delicious", "flavor", "pizza", "pasta", "crust",
        "equipment", "machine", "racks", "barbell", "treatment", "pain", "fresh",
        "soggy", "burnt", "cold", "menu", "dish", "teeth", "workout", "results"
    ],
    "Pricing & Value": [
        "price", "pricing", "cost", "expensive", "steep", "overpriced", "cheap",
        "affordable", "value", "worth", "money", "bill", "fee", "charged", "membership",
        "robbery", "refund", "dollar", "$"
    ],
    "Cleanliness & Ambience": [
        "clean", "cleanliness", "dirty", "hygiene", "ambience", "atmosphere", "vibe",
        "lighting", "music", "noisy", "loud", "cramped", "spacious", "decor",
        "restroom", "shower", "locker", "table", "cozy", "studio"
    ],
    "Wait Time & Speed": [
        "wait", "waited", "waiting", "time", "delay", "delayed", "slow", "fast", "quick",
        "prompt", "rush", "hour", "minutes", "speed", "sluggish", "schedule", "appointment"
    ],
    "Delivery & Logistics": [
        "delivery", "takeout", "pickup", "order", "parking", "arrive", "arrived",
        "packaging", "eta", "driver", "transport"
    ]
}

EMOTION_KEYWORDS = {
    "Delight / Joy": ["love", "loved", "obsessed", "best", "incredible", "divine", "dream", "amazing", "top-notch", "fantastic", "perfection"],
    "Frustration / Anger": ["awful", "rude", "robbery", "nightmare", "predatory", "worst", "unacceptable", "furious", "angry", "terrible"],
    "Disappointment": ["disappointing", "disappointed", "lukewarm", "slipped", "soggy", "burnt", "expected better", "mediocre"],
    "Appreciation / Trust": ["thank", "thanks", "gentle", "lifesavers", "transparent", "attentive", "recommend", "patient"]
}

STOPWORDS = {
    "the", "and", "a", "to", "was", "for", "with", "in", "of", "on", "is", "it",
    "i", "we", "my", "our", "at", "this", "that", "had", "have", "were", "but",
    "as", "be", "so", "very", "all", "they", "you", "from", "by", "an", "not",
    "just", "too", "when", "her", "his", "out", "up", "or", "if", "there", "their",
    "been", "about", "would", "got", "can", "into", "even", "came", "get", "did"
}

def analyze_single_review(review_text, rating=None):
    """
    Analyzes an individual review text and returns scores, aspect tags, and emotions.
    """
    scores = analyzer.polarity_scores(review_text)
    compound = scores['compound']
    
    # Classify sentiment label
    if compound >= 0.05:
        sentiment = "Positive"
        color = "green"
    elif compound <= -0.05:
        sentiment = "Negative"
        color = "red"
    else:
        sentiment = "Neutral"
        color = "gray"
        
    # Also reconcile with star rating if provided (e.g. 1 star with sarcastic words)
    if rating is not None:
        if rating <= 2 and compound > 0.2:
            # Low star rating overrides borderline positive text (sarcasm or polite complaint)
            sentiment = "Negative"
            color = "red"
        elif rating >= 4 and compound < -0.2:
            sentiment = "Positive"
            color = "green"

    # Aspect extraction
    detected_aspects = {}
    lower_text = review_text.lower()
    sentences = re.split(r'[.!?]+', review_text)

    for aspect, keywords in ASPECT_KEYWORDS.items():
        matched_words = [kw for kw in keywords if kw in lower_text]
        if matched_words:
            # Calculate aspect specific sentiment by scanning sentences containing keyword
            aspect_sentences = [
                s for s in sentences if any(kw in s.lower() for kw in matched_words)
            ]
            if aspect_sentences:
                sub_score = analyzer.polarity_scores(" ".join(aspect_sentences))['compound']
            else:
                sub_score = compound

            if sub_score >= 0.05:
                asp_sentiment = "Positive"
            elif sub_score <= -0.05:
                asp_sentiment = "Negative"
            else:
                asp_sentiment = "Neutral"

            detected_aspects[aspect] = {
                "sentiment": asp_sentiment,
                "score": round(sub_score, 2),
                "matched_keywords": matched_words[:3]
            }

    # Emotion detection
    detected_emotions = []
    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(kw in lower_text for kw in keywords):
            detected_emotions.append(emotion)
    if not detected_emotions:
        detected_emotions.append("Neutral / Objective" if sentiment == "Neutral" else ("Content" if sentiment == "Positive" else "Dissatisfied"))

    return {
        "text": review_text,
        "sentiment": sentiment,
        "sentiment_color": color,
        "compound_score": round(compound, 3),
        "scores": {
            "pos": round(scores['pos'], 3),
            "neu": round(scores['neu'], 3),
            "neg": round(scores['neg'], 3)
        },
        "aspects": detected_aspects,
        "emotions": detected_emotions
    }


def analyze_dataset(reviews_list):
    """
    Analyzes an aggregate list of reviews and returns complete statistics,
    breakdowns by source, aspect scores, word clouds, and key takeaways.
    """
    total = len(reviews_list)
    if total == 0:
        return {
            "total_reviews": 0,
            "overall_sentiment_score": 0,
            "sentiment_counts": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "sentiment_percentages": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "source_breakdown": {},
            "aspect_breakdown": {},
            "key_drivers": [],
            "pain_points": [],
            "reviews": []
        }

    enriched_reviews = []
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    source_counts = {
        "google": {"Positive": 0, "Neutral": 0, "Negative": 0, "total": 0, "ratings_sum": 0},
        "twitter": {"Positive": 0, "Neutral": 0, "Negative": 0, "total": 0, "ratings_sum": 0}
    }
    
    aspect_stats = {
        asp: {"positive": 0, "negative": 0, "neutral": 0, "total_mentions": 0, "score_sum": 0.0}
        for asp in ASPECT_KEYWORDS.keys()
    }

    positive_words_list = []
    negative_words_list = []

    for item in reviews_list:
        text = item.get("text", "")
        rating = item.get("rating")
        source = item.get("source", "google").lower()
        if source not in source_counts:
            source_counts[source] = {"Positive": 0, "Neutral": 0, "Negative": 0, "total": 0, "ratings_sum": 0}

        analysis = analyze_single_review(text, rating)
        
        # Merge with existing item metadata
        enriched_item = {**item, **analysis}
        enriched_reviews.append(enriched_item)

        s_label = analysis["sentiment"]
        sentiment_counts[s_label] += 1
        source_counts[source][s_label] += 1
        source_counts[source]["total"] += 1
        if rating:
            source_counts[source]["ratings_sum"] += rating

        # Aspect aggregation
        for asp_name, asp_data in analysis["aspects"].items():
            aspect_stats[asp_name]["total_mentions"] += 1
            aspect_stats[asp_name]["score_sum"] += asp_data["score"]
            if asp_data["sentiment"] == "Positive":
                aspect_stats[asp_name]["positive"] += 1
            elif asp_data["sentiment"] == "Negative":
                aspect_stats[asp_name]["negative"] += 1
            else:
                aspect_stats[asp_name]["neutral"] += 1

        # Token extraction for word insights
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        meaningful_words = [w for w in words if w not in STOPWORDS]
        if s_label == "Positive":
            positive_words_list.extend(meaningful_words)
        elif s_label == "Negative":
            negative_words_list.extend(meaningful_words)

    # Compute percentages
    sentiment_pcts = {
        k: round((v / total) * 100, 1) for k, v in sentiment_counts.items()
    }

    # Net sentiment index: (Positive % - Negative %) scaled to 0-100 index
    # -100 to +100 -> mapped to 0 to 100
    raw_net = sentiment_pcts["Positive"] - sentiment_pcts["Negative"]
    overall_sentiment_score = round(max(0, min(100, (raw_net + 100) / 2)), 1)

    # Clean aspect breakdown
    aspect_breakdown = {}
    for asp, data in aspect_stats.items():
        if data["total_mentions"] > 0:
            avg_score = round(data["score_sum"] / data["total_mentions"], 2)
            pos_ratio = round((data["positive"] / data["total_mentions"]) * 100, 1)
            aspect_breakdown[asp] = {
                "total_mentions": data["total_mentions"],
                "positive": data["positive"],
                "negative": data["negative"],
                "neutral": data["neutral"],
                "pos_ratio": pos_ratio,
                "avg_score": avg_score,
                "status": "Healthy" if pos_ratio >= 65 else ("Attention Needed" if pos_ratio >= 40 else "Critical Issue")
            }
        else:
            aspect_breakdown[asp] = {
                "total_mentions": 0,
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "pos_ratio": 0.0,
                "avg_score": 0.0,
                "status": "No Mentions"
            }

    # Extract Top Drivers and Pain Points (frequency pairs or high-impact words)
    top_positives = [
        {"word": w, "count": count}
        for w, count in Counter(positive_words_list).most_common(8)
    ]
    top_negatives = [
        {"word": w, "count": count}
        for w, count in Counter(negative_words_list).most_common(8)
    ]

    return {
        "total_reviews": total,
        "overall_sentiment_score": overall_sentiment_score,
        "sentiment_counts": sentiment_counts,
        "sentiment_percentages": sentiment_pcts,
        "source_breakdown": source_counts,
        "aspect_breakdown": aspect_breakdown,
        "key_drivers": top_positives,
        "pain_points": top_negatives,
        "reviews": enriched_reviews
    }
