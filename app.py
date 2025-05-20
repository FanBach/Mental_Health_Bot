import streamlit as st
import datetime
import json
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
import speech_recognition as sr
import pyttsx3
import threading
import openai
from textblob import TextBlob

# Application setup
st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = {}
    
if 'mood_entries' not in st.session_state:
    st.session_state.mood_entries = {}

if 'breathing_count' not in st.session_state:
    st.session_state.breathing_count = 0
    
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
    
if 'weather_api_key' not in st.session_state:
    st.session_state.weather_api_key = ""
    
if 'city' not in st.session_state:
    st.session_state.city = "London"

if 'message_history' not in st.session_state:
    st.session_state.message_history = []

# Load existing data if available
def load_data():
    if os.path.exists("journal_entries.json"):
        with open("journal_entries.json", "r") as f:
            st.session_state.journal_entries = json.load(f)
    
    if os.path.exists("mood_entries.json"):
        with open("mood_entries.json", "r") as f:
            st.session_state.mood_entries = json.load(f)

# Save data to local files
def save_data():
    with open("journal_entries.json", "w") as f:
        json.dump(st.session_state.journal_entries, f)
    
    with open("mood_entries.json", "w") as f:
        json.dump(st.session_state.mood_entries, f)

# Load existing data on app startup
load_data()

# Sidebar for navigation
st.sidebar.title("Mental Health Companion")
page = st.sidebar.radio("Navigate to:", ["Dashboard", "Guided Breathing", "Daily Journal", 
                                         "Mood Tracker", "Reminders", "Weather & Mood", "Chat Support", 
                                         "Voice Assistant", "Settings"])

# Dashboard
if page == "Dashboard":
    st.title("Mental Health Companion Dashboard")
    st.write("Welcome to your personal mental health companion!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Latest Stats")
        
        # Recent journal entries
        st.write("#### Recent Journal Entries")
        if st.session_state.journal_entries:
            recent_entries = sorted(st.session_state.journal_entries.items(), key=lambda x: x[0], reverse=True)[:3]
            for date, entry in recent_entries:
                st.write(f"**{date}**: {entry[:100]}..." if len(entry) > 100 else f"**{date}**: {entry}")
        else:
            st.write("No journal entries yet.")
        
        # Recent mood entries
        st.write("#### Recent Mood Entries")
        if st.session_state.mood_entries:
            recent_moods = sorted(st.session_state.mood_entries.items(), key=lambda x: x[0], reverse=True)[:3]
            for date, mood_data in recent_moods:
                st.write(f"**{date}**: Mood - {mood_data['mood']}, Score - {mood_data['sentiment_score']:.2f}")
        else:
            st.write("No mood entries yet.")
    
    with col2:
        st.subheader("Quick Actions")
        
        # Quick breathing exercise
        if st.button("Quick Breathing Exercise (2 minutes)"):
            st.session_state.page = "Guided Breathing"
            st.experimental_rerun()
        
        # Quick mood check-in
        st.write("#### Quick Mood Check-in")
        quick_mood = st.select_slider(
            "How are you feeling right now?",
            options=["Very Bad", "Bad", "Neutral", "Good", "Excellent"]
        )
        
        if st.button("Save Quick Mood"):
            today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            sentiment_score = {"Very Bad": -1.0, "Bad": -0.5, "Neutral": 0.0, "Good": 0.5, "Excellent": 1.0}[quick_mood]
            
            st.session_state.mood_entries[today] = {
                "mood": quick_mood,
                "sentiment_score": sentiment_score
            }
            save_data()
            st.success("Mood saved successfully!")

# Guided Breathing Timer
elif page == "Guided Breathing":
    st.title("Guided Breathing Exercise")
    st.write("Take a moment to breathe and relax.")
    
    breathing_options = {
        "Box Breathing (4-4-4-4)": {
            "inhale": 4,
            "hold1": 4,
            "exhale": 4,
            "hold2": 4,
            "cycles": 4
        },
        "4-7-8 Breathing": {
            "inhale": 4,
            "hold1": 7,
            "exhale": 8,
            "hold2": 0,
            "cycles": 4
        },
        "Calm Breathing (5-2-5)": {
            "inhale": 5,
            "hold1": 2,
            "exhale": 5,
            "hold2": 0,
            "cycles": 5
        }
    }
    
    selected_breathing = st.selectbox("Select breathing technique:", list(breathing_options.keys()))
    
    # Get the parameters for the selected breathing technique
    technique = breathing_options[selected_breathing]
    
    if st.button("Start Breathing Exercise"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        visual_element = st.empty()
        
        cycle_duration = technique["inhale"] + technique["hold1"] + technique["exhale"] + technique["hold2"]
        total_duration = cycle_duration * technique["cycles"]
        
        for cycle in range(technique["cycles"]):
            # Inhale
            status_text.text("Inhale deeply...")
            for i in range(technique["inhale"]):
                circle_size = 50 + (i * 40 / technique["inhale"])
                visual_element.markdown(f"""
                <div style="display: flex; justify-content: center;">
                    <div style="
                        width: {circle_size}px;
                        height: {circle_size}px;
                        background-color: skyblue;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        color: white;
                    ">
                        {technique["inhale"] - i}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                progress = ((cycle * cycle_duration) + i) / total_duration
                progress_bar.progress(progress)
                time.sleep(1)
            
            # Hold 1
            if technique["hold1"] > 0:
                status_text.text("Hold your breath...")
                for i in range(technique["hold1"]):
                    visual_element.markdown(f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="
                            width: 90px;
                            height: 90px;
                            background-color: lightgreen;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 20px;
                            color: white;
                        ">
                            {technique["hold1"] - i}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    progress = ((cycle * cycle_duration) + technique["inhale"] + i) / total_duration
                    progress_bar.progress(progress)
                    time.sleep(1)
            
            # Exhale
            status_text.text("Exhale slowly...")
            for i in range(technique["exhale"]):
                circle_size = 90 - (i * 40 / technique["exhale"])
                visual_element.markdown(f"""
                <div style="display: flex; justify-content: center;">
                    <div style="
                        width: {circle_size}px;
                        height: {circle_size}px;
                        background-color: lavender;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        color: white;
                    ">
                        {technique["exhale"] - i}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                progress = ((cycle * cycle_duration) + technique["inhale"] + technique["hold1"] + i) / total_duration
                progress_bar.progress(progress)
                time.sleep(1)
            
            # Hold 2
            if technique["hold2"] > 0:
                status_text.text("Hold your breath...")
                for i in range(technique["hold2"]):
                    visual_element.markdown(f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="
                            width: 50px;
                            height: 50px;
                            background-color: lightpink;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 20px;
                            color: white;
                        ">
                            {technique["hold2"] - i}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    progress = ((cycle * cycle_duration) + technique["inhale"] + technique["hold1"] + technique["exhale"] + i) / total_duration
                    progress_bar.progress(progress)
                    time.sleep(1)
        
        st.session_state.breathing_count += 1
        progress_bar.progress(1.0)
        status_text.text("Breathing exercise complete!")
        st.balloons()
        
        # Show statistics
        st.success(f"You have completed {st.session_state.breathing_count} breathing exercises. Great job!")

# Daily Journal
elif page == "Daily Journal":
    st.title("Daily Journal")
    
    # Journal prompts
    journal_prompts = [
        "What made you smile today?",
        "What's something you're grateful for today?",
        "What's one challenge you faced today and how did you handle it?",
        "Describe one moment of joy you experienced today.",
        "What's something you learned today?",
        "What's one thing you're looking forward to tomorrow?",
        "How did you take care of yourself today?",
        "What's something you'd like to improve about tomorrow?",
        "Who made a positive impact on your day and why?",
        "What emotions were most present for you today?"
    ]
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Journal section
    st.subheader("Today's Journal")
    
    # Show a random prompt
    import random
    random_prompt = random.choice(journal_prompts)
    st.write(f"**Prompt:** {random_prompt}")
    
    # Journal entry
    journal_content = st.text_area("Your thoughts:", height=250, 
                                   value=st.session_state.journal_entries.get(today, ""))
    
    if st.button("Save Journal Entry"):
        st.session_state.journal_entries[today] = journal_content
        save_data()
        st.success("Journal entry saved successfully!")
    
    # Show past entries
    st.subheader("Past Journal Entries")
    if st.session_state.journal_entries:
        selected_date = st.selectbox(
            "Select a date:",
            sorted(st.session_state.journal_entries.keys(), reverse=True)
        )
        
        st.write(st.session_state.journal_entries[selected_date])
        
        if st.button("Delete this entry"):
            del st.session_state.journal_entries[selected_date]
            save_data()
            st.success("Journal entry deleted.")
            st.experimental_rerun()
    else:
        st.write("No journal entries yet.")

# Mood Tracker
elif page == "Mood Tracker":
    st.title("Mood Tracker")
    st.write("Track your mood and see patterns over time.")
    
    # Current mood input
    st.subheader("How are you feeling today?")
    
    mood_options = ["Very Bad", "Bad", "Neutral", "Good", "Excellent"]
    selected_mood = st.select_slider(
        "Select your mood:",
        options=mood_options
    )
    
    notes = st.text_area("Notes about your mood (optional):", height=100)
    
    if st.button("Save Mood"):
        # Get current date and time
        now = datetime.datetime.now()
        date_key = now.strftime("%Y-%m-%d %H:%M")
        
        # Perform sentiment analysis on notes
        if notes:
            analysis = TextBlob(notes)
            sentiment_score = analysis.sentiment.polarity
        else:
            # If no notes, use a predetermined sentiment score based on selected mood
            sentiment_map = {
                "Very Bad": -1.0,
                "Bad": -0.5,
                "Neutral": 0.0,
                "Good": 0.5,
                "Excellent": 1.0
            }
            sentiment_score = sentiment_map[selected_mood]
        
        # Save mood data
        st.session_state.mood_entries[date_key] = {
            "mood": selected_mood,
            "notes": notes,
            "sentiment_score": sentiment_score
        }
        
        save_data()
        st.success("Mood saved successfully!")
    
    # Display mood history
    st.subheader("Mood History")
    
    if st.session_state.mood_entries:
        # Convert mood entries to DataFrame for analysis
        mood_data = []
        for date_str, entry in st.session_state.mood_entries.items():
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            mood_data.append({
                "date": date,
                "mood": entry["mood"],
                "score": entry["sentiment_score"]
            })
        
        mood_df = pd.DataFrame(mood_data)
        mood_df = mood_df.sort_values("date")
        
        # Generate the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot sentiment scores
        ax.plot(mood_df["date"], mood_df["score"], marker='o', linestyle='-', color='blue')
        
        # Customize the plot
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood Score")
        ax.set_title("Mood History Over Time")
        ax.grid(True, alpha=0.3)
        
        # Improve x-axis date formatting
        plt.xticks(rotation=45)
        
        # Set y-axis limits
        ax.set_ylim(-1.1, 1.1)
        
        # Add horizontal lines for mood categories
        ax.axhline(y=0.75, color='darkgreen', alpha=0.3, linestyle='--')
        ax.axhline(y=0.25, color='green', alpha=0.3, linestyle='--')
        ax.axhline(y=0, color='gray', alpha=0.3, linestyle='--')
        ax.axhline(y=-0.25, color='orange', alpha=0.3, linestyle='--')
        ax.axhline(y=-0.75, color='red', alpha=0.3, linestyle='--')
        
        # Add text labels for mood zones
        ax.text(mood_df["date"].iloc[0], 0.9, "Excellent", color='darkgreen')
        ax.text(mood_df["date"].iloc[0], 0.5, "Good", color='green')
        ax.text(mood_df["date"].iloc[0], 0, "Neutral", color='gray')
        ax.text(mood_df["date"].iloc[0], -0.5, "Bad", color='orange')
        ax.text(mood_df["date"].iloc[0], -0.9, "Very Bad", color='red')
        
        # Display the plot
        st.pyplot(fig)
        
        # Show tabular data
        st.subheader("Mood Log")
        display_df = mood_df.sort_values("date", ascending=False)
        display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(display_df[["date", "mood", "score"]])
        
    else:
        st.write("No mood data recorded yet.")

# Reminders
elif page == "Reminders":
    st.title("Daily Reminders")
    st.write("""
    This section simulates reminder functionality. 
    In a production app, this would use scheduling libraries to send actual notifications.
    """)
    
    # Set up reminders
    st.subheader("Set Reminders")
    
    reminder_types = {
        "breathing": "Breathing Exercise",
        "journal": "Journal Entry",
        "mood": "Mood Check-in",
        "medication": "Medication",
        "water": "Drink Water",
        "walk": "Take a Walk",
        "stretch": "Stretch Break"
    }
    
    selected_reminder = st.selectbox("Reminder type:", list(reminder_types.values()))
    reminder_time = st.time_input("Set time:", datetime.time(8, 0))
    reminder_days = st.multiselect(
        "Select days:",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )
    
    reminder_note = st.text_input("Additional note (optional):")
    
    if st.button("Set Reminder"):
        st.success(f"Reminder set for {reminder_time.strftime('%H:%M')} on {', '.join(reminder_days)}!")
        
        # This would typically save to a reminder database
        # For this demo, we'll just display a confirmation
    
    # Demo of upcoming reminders
    st.subheader("Today's Reminders")
    
    # Current time for demo
    now = datetime.datetime.now()
    today_weekday = now.strftime("%A")
    
    # Demo reminders
    demo_reminders = [
        {"type": "Breathing Exercise", "time": "08:00", "done": True},
        {"type": "Mood Check-in", "time": "12:00", "done": now.hour >= 12},
        {"type": "Journal Entry", "time": "20:00", "done": now.hour >= 20},
        {"type": "Drink Water", "time": "Every 2 hours", "done": False}
    ]
    
    for reminder in demo_reminders:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{reminder['type']}**")
        with col2:
            st.write(reminder['time'])
        with col3:
            if reminder['done']:
                st.write("✅ Done")
            else:
                st.write("⏳ Upcoming")

# Weather & Mood
elif page == "Weather & Mood":
    st.title("Weather & Mood Correlation")
    
    # Weather API setup
    st.subheader("Weather Information")
    
    # API key input
    weather_api_key = st.text_input("Enter OpenWeatherMap API Key:", 
                              value=st.session_state.weather_api_key, 
                              type="password")
    
    if weather_api_key:
        st.session_state.weather_api_key = weather_api_key
    
    # City input
    city = st.text_input("Enter your city:", value=st.session_state.city)
    if city:
        st.session_state.city = city
    
    # Get weather data
    if st.button("Get Weather Data"):
        if not st.session_state.weather_api_key:
            st.error("Please enter an OpenWeatherMap API key to get weather data.")
        else:
            try:
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
                response = requests.get(weather_url)
                weather_data = response.json()
                
                if response.status_code == 200:
                    # Display current weather
                    st.subheader(f"Current Weather in {city}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Temperature:** {weather_data['main']['temp']}°C")
                        st.write(f"**Feels Like:** {weather_data['main']['feels_like']}°C")
                        st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
                        
                    with col2:
                        weather_icon = weather_data['weather'][0]['icon']
                        weather_desc = weather_data['weather'][0]['description']
                        st.write(f"**Condition:** {weather_desc.capitalize()}")
                        
                        icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
                        st.image(icon_url, width=100)
                    
                    # If we have mood data, show correlation
                    if st.session_state.mood_entries:
                        st.subheader("Weather-Mood Correlation")
                        st.write("In a production app, this would analyze your mood data against historical weather data to find patterns.")
                        
                        # Generate sample correlation data for demonstration
                        st.write("##### Example Weather Impact Analysis")
                        st.write("Based on your recorded moods and weather conditions:")
                        
                        weather_impacts = [
                            "Your mood tends to be higher on sunny days",
                            "Temperature changes of more than 10°C correlate with mood shifts",
                            "Rainy days show a slight decrease in average mood score",
                            "Higher humidity correlates with lower energy levels in your journal entries"
                        ]
                        
                        for impact in weather_impacts:
                            st.write(f"• {impact}")
                    
                else:
                    st.error(f"Error: {weather_data['message']}")
            except Exception as e:
                st.error(f"Error fetching weather data: {str(e)}")
    
    if not st.session_state.mood_entries:
        st.info("Record mood data to see weather correlations.")

# Chat Support
elif page == "Chat Support":
    st.title("Chat Support")
    st.write("Talk to our AI companion about mental health concerns.")
    
    # API key input
    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", 
                                         value=st.session_state.openai_api_key, 
                                         type="password")
    
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
    
    # Initialize OpenAI client
    if st.session_state.openai_api_key:
        openai.api_key = st.session_state.openai_api_key
    
    # Display conversation history
    st.subheader("Conversation")
    for message in st.session_state.message_history:
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        else:
            st.write(f"AI: {message['content']}")
    
    # User input
    user_input = st.text_input("Type your message:", key="chat_input")
    
    if st.button("Send") and user_input:
        # Add user message to history
        st.session_state.message_history.append({"role": "user", "content": user_input})
        
        try:
            if st.session_state.openai_api_key:
                # Create system message for mental health focus
                system_message = {
                    "role": "system", 
                    "content": "You are a supportive and compassionate mental health companion. Provide helpful guidance, support, and resources for mental wellness. Don't provide medical diagnoses or treatment advice."
                }
                
                # Prepare messages for API call
                messages = [system_message] + st.session_state.message_history
                
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                
                # Get assistant response
                assistant_response = response.choices[0].message["content"]
                
                # Add assistant response to history
                st.session_state.message_history.append({"role": "assistant", "content": assistant_response})
            else:
                # Fallback responses if no API key
                fallback_responses = [
                    "I'm here to listen. What's been on your mind lately?",
                    "It sounds like you're going through a lot. Remember to be kind to yourself.",
                    "Have you tried any breathing exercises when you feel this way?",
                    "Acknowledging your feelings is an important step. What support do you need right now?",
                    "Remember that it's okay to ask for help when you need it.",
                    "Self-care is important. What's one small thing you could do for yourself today?",
                    "I'm here to support you. Would you like to talk more about what you're experiencing?"
                ]
                
                import random
                assistant_response = random.choice(fallback_responses)
                st.session_state.message_history.append({"role": "assistant", "content": assistant_response})
                
                # Note about API key
                st.info("For personalized responses, please add your OpenAI API key in the sidebar.")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        # Rerun to update the conversation display
        st.experimental_rerun()

# Voice Assistant
elif page == "Voice Assistant":
    st.title("Voice Assistant")
    st.write("Talk to your mental health companion using voice.")
    
    # Initialize speech recognition
    recognizer = sr.Recognizer()
    
    # Voice input
    st.subheader("Voice Input")
    st.write("Click the button and speak to convert your speech to text.")
    
    if st.button("Start Listening"):
        with st.spinner("Listening..."):
            try:
                # Use microphone as source
                with sr.Microphone() as source:
                    st.write("Adjusting for ambient noise...")
                    recognizer.adjust_for_ambient_noise(source)
                    st.write("Speak now...")
                    audio = recognizer.listen(source, timeout=5)
                
                # Recognize speech
                st.write("Processing speech...")
                text = recognizer.recognize_google(audio)
                
                st.success(f"You said: {text}")
                
                # Process the speech input
                # This would typically call the chatbot function
                # For demo purposes, we'll use a simple response system
                
                responses = {
                    "hello": "Hello! How are you feeling today?",
                    "how are you": "I'm here to help you. How are you doing?",
                    "feeling sad": "I'm sorry to hear that. Remember that it's okay to feel sad sometimes. Would you like to try a breathing exercise?",
                    "feeling happy": "That's wonderful to hear! It's great that you're having a good day.",
                    "breathing": "Would you like to start a guided breathing exercise?",
                    "journal": "Would you like to write in your journal today?",
                    "mood": "Would you like to record your mood today?",
                    "help": "I'm here to help with guided breathing, journaling, mood tracking, and more. What would you like assistance with?"
                }
                
                response_text = "I'm listening. How can I help you today?"
                
                for key, response in responses.items():
                    if key in text.lower():
                        response_text = response
                        break
                
                # Use text-to-speech to respond
                st.subheader("Response")
                st.write(response_text)
                
                # This would typically use a proper TTS engine
                # For simplicity in this demo, we'll just show text
                st.info("In a production app, this would speak the response using text-to-speech.")
                
            except sr.WaitTimeoutError:
                st.error("No speech detected. Please try again.")
            except sr.RequestError:
                st.error("Could not request results. Check your internet connection.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Text-to-speech demo
    st.subheader("Text-to-Speech")
    tts_text = st.text_area("Enter text to convert to speech:", "Hello, I'm your mental health companion.")
    
    if st.button("Convert to Speech"):
        st.success("Text converted to speech!")
        st.info("In a production app, this would play the synthesized speech.")
        
        # This is where a real TTS engine would be used
        # For example, using pyttsx3 or a cloud TTS service

# Settings
elif page == "Settings":
    st.title("Settings")
    
    # API Keys
    st.subheader("API Keys")
    
    openai_api_key = st.text_input("OpenAI API Key:", 
                                  value=st.session_state.openai_api_key, 
                                  type="password")
    
    weather_api_key = st.text_input("OpenWeatherMap API Key:", 
                                   value=st.session_state.weather_api_key, 
                                   type="password")
    
    if st.button("Save API Keys"):
        st.session_state.openai_api_key = openai_api_key
        st.session_state.weather_api_key = weather_api_key
        st.success("API keys saved!")
    
    # Data Management
    st.subheader("Data Management")
    
    if st.button("Export Data"):
        # Create export data
        export_data = {
            "journal_entries": st.session_state.journal_entries,
            "mood_entries": st.session_state.mood_entries
        }
        
        # Convert to JSON string
        export_json = json.dumps(export_data)
        
        # Create download button
        st.download_button(
            label="Download JSON",
            data=export_json,
            file_name="mental_health_data.json",
            mime="application/json"
        )
    
    if st.button("Clear All Data"):
        st.warning("⚠️ This will delete all your journal entries and mood data. This action cannot be undone.")
        confirm = st.checkbox("I understand and want to clear all data")
        
        if confirm and st.button("Confirm Clear Data"):
            st.session_state.journal_entries = {}
            st.session_state.mood_entries = {}
            save_data()
            st.success("All data cleared successfully.")
            st.experimental_rerun()
    
    # Notification Settings
    st.subheader("Notification Settings")
    
    # These would be implemented with actual notification systems in a production app
    notifications_enabled = st.checkbox("Enable notifications", value=True)
    
    if notifications_enabled:
        st.write("Notification types:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Breathing reminders", value=True)
            st.checkbox("Journal reminders", value=True)
            st.checkbox("Mood check-in reminders", value=True)
        
        with col2:
            st.checkbox("Positive affirmations", value=True)
            st.checkbox("Weather updates", value=False)
            st.checkbox("Inactivity alerts", value=True)
    
    # Theme Settings
    st.subheader("Theme Settings")
    
    theme = st.radio("Select theme:", ["Light", "Dark", "System Default"])
    color_scheme = st.selectbox("Color scheme:", ["Blue", "Green", "Purple", "Warm"])
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
        
    # About
    st.subheader("About Mental Health Companion")
    st.write("""
    Mental Health Companion is a comprehensive tool designed to support your mental wellness journey.
    
    **Features:**
    - Guided breathing exercises
    - Daily journaling
    - Mood tracking with sentiment analysis
    - Weather and mood correlation
    - AI chat support
    - Voice assistant
    
    **Version:** 1.0.0
    
    This application stores all your data locally and does not send any personal information
    to external servers (except when using the API services you've configured).
    """)
    
    # Contact
    st.subheader("Help & Support")
    st.write("If you have any questions or need assistance, please contact us:")
    st.write("Email: support@mentalhealthcompanion.example.com")
    st.write("Website: [mentalhealthcompanion.example.com](https://mentalhealthcompanion.example.com)")

        