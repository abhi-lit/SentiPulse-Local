"""
Automated AI Business Advisor & Service Improvement Recommendation Engine.
Analyzes sentiment metrics, aspect ratings, and pain points to synthesize:
- Executive Summary & Customer Satisfaction Grade
- Prioritized Action Plan (Urgent, Moderate, Growth)
- Departmental Operational Advice
- Pre-composed Professional Review Response Templates for Business Owners
"""

def generate_business_recommendations(analysis_result, business_info=None):
    """
    Generates actionable business feedback based on sentiment analysis results.
    """
    total = analysis_result.get("total_reviews", 0)
    if total == 0:
        return {
            "grade": "N/A",
            "summary": "No reviews available to generate recommendations.",
            "action_items": [],
            "strengths": [],
            "weaknesses": [],
            "response_templates": []
        }

    sentiment_pcts = analysis_result.get("sentiment_percentages", {})
    pos_pct = sentiment_pcts.get("Positive", 0)
    neg_pct = sentiment_pcts.get("Negative", 0)
    overall_score = analysis_result.get("overall_sentiment_score", 50)
    aspects = analysis_result.get("aspect_breakdown", {})
    pain_points = [p["word"] for p in analysis_result.get("pain_points", [])]
    key_drivers = [d["word"] for d in analysis_result.get("key_drivers", [])]

    # Calculate Letter Grade
    if overall_score >= 88:
        grade = "A+"
        grade_desc = "Outstanding Customer Experience"
        grade_color = "emerald"
    elif overall_score >= 75:
        grade = "A"
        grade_desc = "Strong Customer Satisfaction"
        grade_color = "green"
    elif overall_score >= 60:
        grade = "B"
        grade_desc = "Good, with clear areas for optimization"
        grade_color = "blue"
    elif overall_score >= 45:
        grade = "C"
        grade_desc = "Average - Significant service friction detected"
        grade_color = "amber"
    else:
        grade = "D"
        grade_desc = "Critical - High customer churn risk"
        grade_color = "red"

    # Identify Strengths and Areas of Concern
    strengths = []
    weaknesses = []
    action_items = []

    # Check each aspect
    for asp_name, asp_data in aspects.items():
        if asp_data["total_mentions"] > 0:
            pos_ratio = asp_data["pos_ratio"]
            if pos_ratio >= 65:
                strengths.append({
                    "aspect": asp_name,
                    "satisfaction": f"{pos_ratio}%",
                    "note": f"Customers consistently commend your {asp_name.lower()}."
                })
            elif pos_ratio < 45:
                weaknesses.append({
                    "aspect": asp_name,
                    "satisfaction": f"{pos_ratio}%",
                    "negative_count": asp_data["negative"],
                    "note": f"{asp_data['negative']} negative reviews flagged regarding {asp_name.lower()}."
                })

    # Generate Targeted Action Items
    if any("rude" in p or "staff" in p or "service" in p for p in pain_points) or aspects.get("Customer Service", {}).get("pos_ratio", 100) < 55:
        action_items.append({
            "priority": "High",
            "category": "Frontline Staff Training",
            "title": "Hospitality & De-escalation Refresher",
            "impact": "Crucial",
            "details": "Customer feedback indicates friction with frontline attitudes or perceived indifference. Conduct a customer service workshop focusing on greeting etiquette, active listening, and reservation handling."
        })

    if any("wait" in p or "delayed" in p or "slow" in p or "time" in p for p in pain_points) or aspects.get("Wait Time & Speed", {}).get("pos_ratio", 100) < 55:
        action_items.append({
            "priority": "High",
            "category": "Operational Efficiency",
            "title": "Peak-Hour Queue & Turnaround Management",
            "impact": "High",
            "details": "Long wait times are a recurring grievance. Audit peak-hour workflow (5 PM - 8 PM), consider SMS notifications for waitlists, and streamline preparation to reduce turnaround bottlenecks."
        })

    if any("expensive" in p or "steep" in p or "price" in p or "fee" in p for p in pain_points) or aspects.get("Pricing & Value", {}).get("pos_ratio", 100) < 50:
        action_items.append({
            "priority": "Medium",
            "category": "Value Perception",
            "title": "Transparent Pricing & Value-Add Combos",
            "impact": "Medium",
            "details": "Perceived price-to-value gap detected. Review pricing transparency, eliminate surprise fees, or introduce bundled specials and loyalty perks to boost perceived value."
        })

    if any("delivery" in p or "cold" in p or "takeout" in p for p in pain_points) or aspects.get("Delivery & Logistics", {}).get("pos_ratio", 100) < 55:
        action_items.append({
            "priority": "Medium",
            "category": "Logistics & Delivery",
            "title": "Insulated Packaging & Order Quality Checklist",
            "impact": "Medium",
            "details": "Takeout orders are arriving lukewarm or missing items. Implement a pre-handover checklist and upgrade to high-grade insulated thermal bags for courier handoffs."
        })

    if any("clean" in p or "dirty" in p or "hygiene" in p for p in pain_points) or aspects.get("Cleanliness & Ambience", {}).get("pos_ratio", 100) < 60:
        action_items.append({
            "priority": "High",
            "category": "Facility Management",
            "title": "Hourly Cleanliness Inspection Protocol",
            "impact": "High",
            "details": "Cleanliness and atmosphere complaints can immediately kill customer trust. Institute a signed hourly sanitation checklist for restrooms, tables, and workout stations."
        })

    # Always ensure at least 2 positive / growth action items
    action_items.append({
        "priority": "Growth",
        "category": "Marketing & Social Proof",
        "title": "Amplify Organic Praise on Social Media",
        "impact": "Revenue Driver",
        "details": f"Leverage your top positive keywords ({', '.join(key_drivers[:3]) if key_drivers else 'quality service'}) in marketing ads and spotlight happy customer quotes on your Instagram/Twitter."
    })

    # Executive Summary Paragraph
    b_name = business_info.get("name", "Your business") if business_info else "Your business"
    summary = (
        f"{b_name} maintains an overall sentiment rating of {overall_score}/100 based on {total} analyzed reviews across Google and Twitter. "
        f"{pos_pct}% of customers express positive sentiment, while {neg_pct}% experienced friction. "
        f"Key customer loyalty drivers include: {', '.join(key_drivers[:4]) if key_drivers else 'overall experience'}. "
        f"Immediate operational attention should focus on: {', '.join(pain_points[:3]) if pain_points else 'ongoing consistency'}."
    )

    # Pre-drafted Professional Response Templates
    response_templates = [
        {
            "scenario": "Responding to a Critical 1-Star Review (Service Recovery)",
            "subject": "De-escalating negative experience",
            "template": (
                f"Hello [Customer Name],\n\n"
                f"Thank you for taking the time to share your feedback. At {b_name}, we hold our hospitality and service to high standards, "
                f"and we are genuinely sorry that your recent visit fell short of what you deserved. We take your comments regarding [Specific issue, e.g., wait time / food temperature] seriously.\n\n"
                f"We would love the chance to make this right. Please email our management directly at management@business.com or call us so we can personally assist you.\n\n"
                f"Warm regards,\nThe Management Team"
            )
        },
        {
            "scenario": "Responding to a Glowing 5-Star Review (Building Brand Loyalty)",
            "subject": "Appreciation & Social Engagement",
            "template": (
                f"Hi [Customer Name],\n\n"
                f"Wow, thank you so much for the wonderful review! Our entire team at {b_name} was thrilled to hear how much you enjoyed our [mention favorite item/service]! 🌟\n\n"
                f"Your support means the world to our local team. We cannot wait to welcome you back again soon!\n\n"
                f"Cheers,\nThe {b_name} Team"
            )
        },
        {
            "scenario": "Responding to Constructive 3-Star Feedback (Value & Speed)",
            "subject": "Acknowledging feedback with operational commitment",
            "template": (
                f"Dear [Customer Name],\n\n"
                f"Thank you for visiting {b_name} and giving us your honest review. We are glad you enjoyed [positive aspect], but we hear you loud and clear regarding [pain point].\n\n"
                f"We are actively tweaking our operations to ensure smoother, faster service. Next time you drop by, let our supervisor know—we want to ensure your next experience is a solid 5 stars!\n\n"
                f"Best,\nThe {b_name} Team"
            )
        }
    ]

    return {
        "grade": grade,
        "grade_desc": grade_desc,
        "grade_color": grade_color,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "action_items": action_items,
        "response_templates": response_templates
    }
