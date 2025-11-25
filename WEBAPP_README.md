# 🚀 Fake News Detector Web App

A beautiful, interactive web application to detect fake news using AI and Machine Learning.

## 📋 Prerequisites

Make sure you have:
- Python 3.11+
- The trained model file: `fake_news_model.pkl`

## 🛠️ Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ Running the App

Simply run:
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎯 Features

- ✅ Clean, modern UI
- ✅ Real-time fake news detection
- ✅ Confidence scores
- ✅ Sentiment analysis
- ✅ Article statistics
- ✅ Color-coded results

## 📱 How to Use

1. Paste a news article into the text area
2. Click "Analyze Article"
3. Get instant results with confidence scores

## 🌐 Deployment Options

### Deploy to Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Deploy to Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/GCP/Azure
Use Docker or serverless functions for cloud deployment.

## ⚠️ Note

Make sure `fake_news_model.pkl` is in the same directory as `app.py`!
