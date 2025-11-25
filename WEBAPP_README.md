# 🚀 Fake News Detector Web App

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fake-news-detection-for-all.streamlit.app/)

A beautiful, interactive web application to detect fake news using AI and Machine Learning.

## 🌐 Live Demo

**Try it now:** [https://fake-news-detection-for-all.streamlit.app/](https://fake-news-detection-for-all.streamlit.app/)

## 🎯 Features

- ✅ **Clean, modern UI** with light theme
- ✅ **Real-time fake news detection** powered by ML
- ✅ **Confidence scores** for predictions
- ✅ **Sentiment analysis** of articles
- ✅ **Article statistics** (word count, caps ratio)
- ✅ **Smart preprocessing** removes metadata/timestamps
- ✅ **Color-coded results** (red for fake, green for true)
- ✅ **Responsive design** works on all devices

## 📱 How to Use

1. Visit [the live app](https://fake-news-detection-for-all.streamlit.app/)
2. Paste any news article into the text area
3. Click "🔍 Analyze Article"
4. Get instant results with:
   - Fake/True prediction
   - Confidence percentage
   - Sentiment analysis
   - Article insights

## 🛠️ Running Locally

### Prerequisites
- Python 3.11+
- The trained model file: `fake_news_model.pkl`

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Fake-News-Detector

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🏗️ Technical Stack

- **Frontend:** Streamlit
- **ML Model:** Logistic Regression (~99.47% accuracy)
- **NLP:** TF-IDF vectorization, TextBlob sentiment analysis
- **Features:** Custom feature extraction (word count, caps ratio, sentiment)
- **Deployment:** Streamlit Cloud

## 🌐 Deployment

This app is deployed on **Streamlit Cloud** for free!

### Deploy Your Own Version

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Click "Deploy"!

### Alternative Deployment Options

**Heroku:**
```bash
heroku create your-app-name
git push heroku main
```

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**AWS/GCP/Azure:**
Use their respective app services or container platforms.

## 🔧 Configuration

The app uses `.streamlit/config.toml` for theming:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#2c3e50"
```

## 📊 Model Details

- **Algorithm:** Logistic Regression
- **Features:** TF-IDF (8000 features, 1-3 grams) + Manual features
- **Accuracy:** ~99.47% on test set
- **Preprocessing:** Removes metadata, timestamps, and source tags

## ⚠️ Important Notes

- The model file `fake_news_model.pkl` must be in the same directory as `app.py`
- For best results, paste the main article content (not just headlines)
- The tool is for educational purposes - always verify from multiple sources

## 🐛 Troubleshooting

**Model not loading?**
- Ensure `fake_news_model.pkl` exists in the project root
- Check that all dependencies are installed

**App not starting?**
- Verify Python version (3.11+)
- Run `pip install -r requirements.txt` again

**Predictions seem off?**
- The model works best with full article text
- Avoid pasting only headlines or metadata

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check the main [README.md](README.md) for more details

---

**Made with ❤️ using Streamlit & Machine Learning**
