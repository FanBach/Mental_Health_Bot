#!/usr/bin/env python3
"""
Demo data generator for Mental Health Companion Bot
This script populates the application with sample data for testing
"""

import json
import datetime
import random
from textblob import TextBlob

def generate_journal_entries():
    """Generate sample journal entries for the past 14 days"""
    journal_entries = {}
    
    journal_templates = [
        "Today was {feeling}. I {activity} and it made me feel {impact}. {reflection}",
        "I woke up feeling {feeling} today. {activity}, which was {impact}. {reflection}",
        "Had a {feeling} day. Spent time {activity}. It was {impact}. {reflection}",
        "{reflection} Today I {activity}, which made the day feel {feeling}. It was {impact}.",
        "{activity} today, which was {impact}. Overall, feeling {feeling}. {reflection}"
    ]
    
    feelings = ["good", "okay", "great", "challenging", "productive", "relaxed", "tired", "energetic", "mixed"]
    activities = [
        "went for a walk", "read a book", "talked with friends", 
        "worked on a project", "tried meditation", "cooked a new recipe",
        "watched a movie", "exercised", "cleaned my space", "practiced a hobby"
    ]
    impacts = [
        "really enjoyable", "helpful", "just what I needed",
        "somewhat challenging", "a good distraction", "calming",
        "interesting", "refreshing", "satisfying", "time well spent"
    ]
    reflections = [
        "I should do this more often.", 
        "I'm grateful for the little things.", 
        "Tomorrow I want to focus more on self-care.",
        "I'm learning to appreciate the present moment.",
        "I need to remember to take breaks.",
        "Noticing my feelings helps me understand myself better.",
        "I'm proud of how I handled today's challenges.",
        "Taking time for myself is important.",
        "Small steps lead to progress.",
        "I'm working on being kinder to myself."
    ]
    
    # Generate entries for the past 14 days
    for i in range(14, 0, -1):
        date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        
        template = random.choice(journal_templates)
        entry = template.format(
            feeling=random.choice(feelings),
            activity=random.choice(activities),
            impact=random.choice(impacts),
            reflection=random.choice(reflections)
        )
        
        journal_entries[date] = entry
    
    return journal_entries

def generate_mood_entries():
    """Generate sample mood entries for the past 14 days"""
    mood_entries = {}
    
    moods = ["Very Bad", "Bad", "Neutral", "Good", "Excellent"]
    mood_weights = [0.1, 0.2, 0.4, 0.2, 0.1]  # For realistic distribution
    
    notes_templates = [
        "Feeling {mood_desc} today. {detail}",
        "{detail} Overall mood: {mood_desc}.",
        "{mood_desc} day. {detail}",
        "{detail}",
        "Today's mood is {mood_desc}. {detail}"
    ]
    
    mood_details = {
        "Very Bad": [
            "Struggling with anxiety today.",
            "Had trouble sleeping last night, feeling off.",
            "Stressed about upcoming deadlines.",
            "Not feeling motivated at all."
        ],
        "Bad": [
            "A bit down today but managing.",
            "Work was challenging today.",
            "Feeling somewhat low energy.",
            "Minor headache affecting my mood."
        ],
        "Neutral": [
            "Average day, nothing special.",
            "Just taking things one step at a time.",
            "Neither good nor bad today.",
            "Steady day, maintaining balance."
        ],
        "Good": [
            "Had a nice chat with a friend.",
            "Completed some tasks I've been putting off.",
            "Weather was nice which boosted my mood.",
            "Made progress on a personal project."
        ],
        "Excellent": [
            "Everything went smoothly today!",
            "Feeling very energetic and positive.",
            "Had a breakthrough on something I've been working on.",
            "Great day with lots of accomplishments."
        ]
    }
    
    # Generate entries with some randomness in time
    for i in range(14, 0, -1):
        # Base date
        base_date = datetime.datetime.now() - datetime.timedelta(days=i)
        
        # Add 1-3 entries per day with random times
        entries_count = random.randint(1, 3)
        for _ in range(entries_count):
            # Random hour
            hour = random.randint(8, 21)
            minute = random.randint(0, 59)
            entry_date = base_date.replace(hour=hour, minute=minute)
            date_key = entry_date.strftime("%Y-%m-%d %H:%M")
            
            # Select mood with weighted probability
            mood = random.choices(moods, weights=mood_weights)[0]
            
            # Create notes
            template = random.choice(notes_templates)
            detail = random.choice(mood_details[mood])
            notes = template.format(mood_desc=mood.lower(), detail=detail)
            
            # Calculate sentiment score
            analysis = TextBlob(notes)
            sentiment_score = analysis.sentiment.polarity
            
            mood_entries[date_key] = {
                "mood": mood,
                "notes": notes,
                "sentiment_score": sentiment_score
            }
    
    return mood_entries

def save_demo_data():
    """Save the generated demo data to JSON files"""
    # Generate data
    journal_entries = generate_journal_entries()
    mood_entries = generate_mood_entries()
    
    # Save journal entries
    with open("journal_entries.json", "w") as f:
        json.dump(journal_entries, f, indent=2)
    
    # Save mood entries
    with open("mood_entries.json", "w") as f:
        json.dump(mood_entries, f, indent=2)
    
    print("Demo data generated successfully!")
    print(f"Created {len(journal_entries)} journal entries")
    print(f"Created {len(mood_entries)} mood entries")
    print("\nYou can now run the application with: streamlit run app.py")

if __name__ == "__main__":
    print("Generating demo data for Mental Health Companion Bot...")
    save_demo_data()