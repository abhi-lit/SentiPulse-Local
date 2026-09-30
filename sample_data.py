"""
Sample Review Datasets for Local Businesses across Google and Twitter (X).
Covers multiple industry verticals:
1. "Bella Napoli Pizzeria" (Restaurant / Food)
2. "Pulse Fitness Club" (Gym / Health)
3. "Sparkle Care Dental Clinic" (Healthcare)
4. "Grandview Boutique Hotel" (Hospitality)
"""

SAMPLE_BUSINESSES = {
    "bella-napoli": {
        "id": "bella-napoli",
        "name": "Bella Napoli Artisan Pizzeria",
        "category": "Restaurant & Dining",
        "location": "Downtown, Seattle, WA",
        "google_rating": 4.2,
        "twitter_handle": "@BellaNapoliPizza",
        "reviews": [
            {
                "id": "g-101",
                "source": "google",
                "author": "Sarah Jenkins",
                "rating": 5,
                "date": "2026-09-22",
                "text": "The wood-fired Margherita pizza here is hands down the best in the city! Crust was perfectly crispy with authentic San Marzano tomatoes. The servers were warm and attentive even on a busy Friday night."
            },
            {
                "id": "g-102",
                "source": "google",
                "author": "Marcus Vance",
                "rating": 2,
                "date": "2026-09-20",
                "text": "Food was okay, but we had to wait 50 minutes just for two pizzas. The waiter completely forgot our drinks order twice. Very noisy and cramped tables. Disappointing service for the price."
            },
            {
                "id": "g-103",
                "source": "google",
                "author": "Elena Rostova",
                "rating": 5,
                "date": "2026-09-18",
                "text": "Loved the truffle pasta and garlic knots! Cozy ambient lighting and friendly staff. Clean restrooms and great wine pairing recommendations from our server Marco."
            },
            {
                "id": "g-104",
                "source": "google",
                "author": "David Chen",
                "rating": 3,
                "date": "2026-09-15",
                "text": "Decent pizza, but $28 for a medium pie feels steep. Delivery was lukewarm when it arrived. The cannoli dessert was delicious though."
            },
            {
                "id": "g-105",
                "source": "google",
                "author": "Jessica Miller",
                "rating": 1,
                "date": "2026-09-12",
                "text": "Awful experience yesterday. Hostess was outright rude when we asked about our reservation status. The pizza crust was burnt to a crisp on the bottom. Will not return."
            },
            {
                "id": "g-106",
                "source": "google",
                "author": "Arun Patel",
                "rating": 5,
                "date": "2026-09-10",
                "text": "Incredible culinary experience! Fresh basil, melted buffalo mozzarella, and top-tier hospitality. The manager came over personally to check on our dietary restrictions."
            },
            {
                "id": "g-107",
                "source": "google",
                "author": "Chloe Dupont",
                "rating": 4,
                "date": "2026-09-08",
                "text": "Great pizza and salad. Can get very noisy during peak dinner rush, but service remained polite and efficient. Highly recommend the tiramisu!"
            },
            {
                "id": "t-201",
                "source": "twitter",
                "author": "@foodie_katie",
                "rating": 5,
                "date": "2026-09-27",
                "text": "Obsessed with @BellaNapoliPizza! Look at that cheese pull 🍕🔥 definitely hitting this spot every weekend! #SeattleEats #PizzaLovers"
            },
            {
                "id": "t-202",
                "source": "twitter",
                "author": "@techbro_dave",
                "rating": 2,
                "date": "2026-09-25",
                "text": "@BellaNapoliPizza Ordered takeout tonight and waited 40 mins past the pickup ETA. Food was cold and order was missing dips. Step up your takeout logistics!"
            },
            {
                "id": "t-203",
                "source": "twitter",
                "author": "@seattle_bites",
                "rating": 4,
                "date": "2026-09-21",
                "text": "Shoutout to the staff at @BellaNapoliPizza for handling our 12-person birthday party with so much patience and complimentary limoncello shots! 💛"
            },
            {
                "id": "t-204",
                "source": "twitter",
                "author": "@grumpy_commuter",
                "rating": 1,
                "date": "2026-09-19",
                "text": "@BellaNapoliPizza $34 for a pizza with delivery fee is daylight robbery. And it arrived soggy. Never again."
            },
            {
                "id": "t-205",
                "source": "twitter",
                "author": "@amber_wanders",
                "rating": 5,
                "date": "2026-09-16",
                "text": "Had dinner at @BellaNapoliPizza downtown tonight. Fantastic ambiance, courteous waiters, and divine gluten-free crust options! ✨"
            },
            {
                "id": "t-206",
                "source": "twitter",
                "author": "@hungry_sam",
                "rating": 3,
                "date": "2026-09-14",
                "text": "@BellaNapoliPizza Good taste as always, but parking nearby is an absolute nightmare and table service was super sluggish."
            }
        ]
    },
    "pulse-fitness": {
        "id": "pulse-fitness",
        "name": "Pulse Fitness & Wellness Club",
        "category": "Gym & Health Club",
        "location": "Metro District, Chicago, IL",
        "google_rating": 3.9,
        "twitter_handle": "@PulseFitnessHQ",
        "reviews": [
            {
                "id": "pf-101",
                "source": "google",
                "author": "Brian O'Connor",
                "rating": 5,
                "date": "2026-09-24",
                "text": "Top-notch gym equipment and brand new Rogue squat racks. Trainers are exceptionally knowledgeable and motivating. Love the clean locker rooms and sauna!"
            },
            {
                "id": "pf-102",
                "source": "google",
                "author": "Megan Rivera",
                "rating": 2,
                "date": "2026-09-22",
                "text": "Membership cancellation is predatory and painful. They kept charging my credit card 2 months after submitting written notice. Front desk staff gave zero help."
            },
            {
                "id": "pf-103",
                "source": "google",
                "author": "Derek Zhao",
                "rating": 3,
                "date": "2026-09-17",
                "text": "Equipments are fine, but peak hours between 5 PM and 8 PM are overcrowded. Waiting 15 minutes for a bench is frustrating. Air conditioning was also broken on the 2nd floor."
            },
            {
                "id": "pf-104",
                "source": "google",
                "author": "Samantha Lee",
                "rating": 5,
                "date": "2026-09-14",
                "text": "The Pilates and HIIT classes included with standard membership are incredible. Instructors give great personal feedback on form. Very clean showers."
            },
            {
                "id": "pf-105",
                "source": "google",
                "author": "Kevin Wright",
                "rating": 2,
                "date": "2026-09-11",
                "text": "Broken cable machines have had 'Out of order' signs for three weeks straight. What are our membership fees paying for? Locker room hygiene has slipped too."
            },
            {
                "id": "pf-201",
                "source": "twitter",
                "author": "@fit_jake",
                "rating": 5,
                "date": "2026-09-28",
                "text": "Crushed leg day at @PulseFitnessHQ! Brand new Eleiko barbell sets are a dream. Staff is always wiping down benches. Great vibe. 💪"
            },
            {
                "id": "pf-202",
                "source": "twitter",
                "author": "@chicago_dan",
                "rating": 1,
                "date": "2026-09-26",
                "text": "@PulseFitnessHQ why has the hot water in the men's showers been freezing for 4 days? Nobody at front desk seems to care. Please fix!"
            },
            {
                "id": "pf-203",
                "source": "twitter",
                "author": "@wellness_rachel",
                "rating": 4,
                "date": "2026-09-18",
                "text": "Loved the morning yoga flow with Coach Maya at @PulseFitnessHQ. Calming atmosphere and immaculate studio."
            }
        ]
    },
    "sparkle-dental": {
        "id": "sparkle-dental",
        "name": "Sparkle Care Dental Clinic",
        "category": "Healthcare & Dentistry",
        "location": "Northside Plaza, Austin, TX",
        "google_rating": 4.6,
        "twitter_handle": "@SparkleCareDent",
        "reviews": [
            {
                "id": "sd-101",
                "source": "google",
                "author": "Emily Thorne",
                "rating": 5,
                "date": "2026-09-25",
                "text": "I had severe dental anxiety, but Dr. Ramirez and the hygienists were incredibly gentle and soothing. Zero pain during my wisdom tooth extraction. Transparent pricing without surprise bills."
            },
            {
                "id": "sd-102",
                "source": "google",
                "author": "Robert Kim",
                "rating": 3,
                "date": "2026-09-19",
                "text": "Dr. Ramirez is great, but the scheduling desk is disorganized. My appointment got delayed by 45 minutes past my booked time with no apology."
            },
            {
                "id": "sd-103",
                "source": "google",
                "author": "Taylor Brooks",
                "rating": 5,
                "date": "2026-09-15",
                "text": "Cleanest clinic I have ever visited! State of the art 3D scanners and TV screens on the ceiling with Netflix to distract you during cleanings. Highly recommended."
            },
            {
                "id": "sd-201",
                "source": "twitter",
                "author": "@austin_techie",
                "rating": 5,
                "date": "2026-09-23",
                "text": "Huge thank you to @SparkleCareDent for fitting me in on emergency notice on a Saturday morning. Lifesavers! 🦷✨"
            },
            {
                "id": "sd-202",
                "source": "twitter",
                "author": "@mom_life_lisa",
                "rating": 4,
                "date": "2026-09-12",
                "text": "Brought both kids for their biannual checkup at @SparkleCareDent. Pediatric dentist was super sweet and patient. Easy digital check-in."
            }
        ]
    }
}
