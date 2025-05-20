<<<<<<< HEAD
# Mental Health Companion Bot

A comprehensive mental wellness application built with Streamlit that includes features for breathing exercises, journaling, mood tracking, and AI-assisted support.

## Features

- **Guided Breathing Timer**: Interactive breathing exercises with visual guidance
- **Daily Journal**: Prompted journaling with local storage of entries
- **Mood Tracker**: Track your mood with sentiment analysis and visualize trends
- **Reminders**: Simulate daily wellness reminders (can be extended with scheduling libraries)
- **Weather & Mood**: Correlate your mood with weather conditions (requires OpenWeatherMap API)
- **Chat Support**: AI-powered support using OpenAI's GPT (requires OpenAI API key)
- **Voice Assistant**: Speech-to-text and text-to-speech functionality
- **Clean Modular Design**: Well-organized code structure for easy customization

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mental-health-companion.git
   cd mental-health-companion
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## API Keys Setup

For full functionality, you'll need to set up the following API keys:

### OpenAI API Key (for Chat Support)
1. Create an account at [OpenAI](https://openai.com/)
2. Generate an API key from your dashboard
3. Enter the key in the Settings page of the application

### OpenWeatherMap API Key (for Weather & Mood)
1. Create an account at [OpenWeatherMap](https://openweathermap.org/)
2. Generate an API key
3. Enter the key in the Settings page of the application

## Data Storage

All data is stored locally in JSON files:
- `journal_entries.json`: Contains all journal entries
- `mood_entries.json`: Contains mood tracking data

You can export your data from the Settings page.

## Extending the Application

### Adding New Features
The modular design makes it easy to add new features:

1. Create a new section in the page navigation
2. Implement your feature in the corresponding section
3. Update the sidebar navigation

### Implementing Real Notifications
To implement real notifications:
1. Add a scheduling library like `schedule` or `apscheduler`
2. Integrate with a notification service API
3. Set up background processes for sending notifications

## Technologies Used

- Streamlit: UI framework
- Pandas & Matplotlib: Data processing and visualization
- TextBlob: Sentiment analysis
- OpenAI API: Chatbot functionality
- SpeechRecognition & pyttsx3: Voice interaction
- Requests: API communication

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is not a substitute for professional mental health support. If you are experiencing serious mental health issues, please contact a healthcare professional.
=======
# Mental_Health_Bot
Bot
>>>>>>> 715443da6d95403040331e2d8351d3baaa0fdec5
