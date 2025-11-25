import streamlit as st
import joblib
import pandas as pd
from textblob import TextBlob
import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Define the ManualFeatureExtractor class (needed for model loading)
class ManualFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            word_count = len(text.split())
            avg_word_len = np.mean([len(w) for w in text.split()]) if text.split() else 0
            caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            exclamation_count = text.count('!')
            
            blob = TextBlob(text)
            subjectivity = blob.sentiment.subjectivity
            polarity = blob.sentiment.polarity
            
            features.append([
                word_count,
                avg_word_len,
                caps_ratio,
                exclamation_count,
                subjectivity,
                polarity
            ])
        return np.array(features)

# Page config
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="wide"
)

# Custom CSS - Clean light theme
st.markdown("""
    <style>
    /* Main background - Pure white/light */
    .main {
        background-color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Fake news card - Soft coral/red */
    .fake-news {
        background-color: #fff5f5;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #ff6b6b;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.15);
        animation: slideIn 0.5s ease-out;
    }
    
    .fake-news h2 {
        color: #e74c3c;
        margin-bottom: 15px;
        font-size: 1.8rem;
    }
    
    .fake-news p {
        color: #2c3e50;
    }
    
    /* True news card - Soft green */
    .true-news {
        background-color: #f0fff4;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #51cf66;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.15);
        animation: slideIn 0.5s ease-out;
    }
    
    .true-news h2 {
        color: #27ae60;
        margin-bottom: 15px;
        font-size: 1.8rem;
    }
    
    .true-news p {
        color: #2c3e50;
    }
    
    /* Info boxes - Light blue */
    div[data-testid="stAlert"] {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        border-radius: 8px;
        color: #2c3e50;
    }
    
    /* Success boxes - Light green */
    div[data-testid="stSuccess"] {
        background-color: #e8f8f5;
        border-left: 4px solid #27ae60;
        border-radius: 8px;
        color: #2c3e50;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    [data-testid="stMetricLabel"] {
        color: #7f8c8d;
    }
    
    /* Button styling - Vibrant blue */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Text area styling - White with subtle border */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background-color: #ffffff;
        color: #2c3e50;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Subheaders and labels */
    h3 {
        color: #2c3e50;
    }
    
    /* Fix label color for text area */
    .stTextArea label {
        color: #2c3e50 !important;
        font-weight: 500;
    }
    
    /* Animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 30px 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-top: 40px;
        border-top: 3px solid #667eea;
    }
    
    .footer-links {
        margin-top: 15px;
    }
    
    .footer-links a {
        color: #667eea;
        text-decoration: none;
        margin: 0 15px;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .footer-links a:hover {
        color: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# Text preprocessing function to remove metadata
def clean_article_text(text):
    """Remove common metadata patterns that might bias the model"""
    
    # Patterns to remove (case-insensitive)
    patterns_to_remove = [
        r'Reported by:.*?(?=\n|$)',  # Reported by: Name
        r'Written by:.*?(?=\n|$)',   # Written by: Name
        r'By:.*?(?=\n|$)',           # By: Name
        r'Published On.*?(?=\n|$)',  # Published On date
        r'Last Updated On.*?(?=\n|$)',  # Last Updated On date
        r'Read Time:.*?(?=\n|$)',    # Read Time: X mins
        r'\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)\s*IST',  # Time stamps
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',  # Dates
        r'Share(?:Twitter|WhatsApp|Facebook|Reddit|Email|LinkedIn)+',  # Social share buttons
        r'Did our AI summary help\?.*?(?=\n|$)',  # AI summary prompts
        r'Let us know\..*?(?=\n|$)',
        r'Switch To.*?Mode',
        r'\((?:Reuters|AP|PTI|ANI)\)\s*-?\s*',  # News agency tags
        r'BREAKING:?\s*',
        r'EXCLUSIVE:?\s*',
        r'LIVE:?\s*',
        r'UPDATE:?\s*',
    ]
    
    cleaned_text = text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
    
    # Remove extra whitespace and newlines
    cleaned_text = re.sub(r'\n+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('fake_news_model.pkl')
        return model
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please make sure 'fake_news_model.pkl' exists.")
        return None

# Header
st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3rem; color: #2c3e50; margin-bottom: 10px; font-weight: 700;">
            📰 Fake News Detector
        </h1>
        <p style="font-size: 1.1rem; color: #7f8c8d; margin-top: 0;">
            AI-powered tool to detect misinformation using NLP and Machine Learning
        </p>
    </div>
""", unsafe_allow_html=True)

# Load the model
model = load_model()

if model:
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 style="color: #2c3e50; font-weight: 600;">📝 Enter News Article</h3>', unsafe_allow_html=True)
        article_text = st.text_area(
            "Paste the article text here:",
            height=300,
            placeholder="Enter the news article you want to verify...",
            label_visibility="collapsed"
        )
        
        analyze_button = st.button("🔍 Analyze Article", type="primary", use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="color: #2c3e50; font-weight: 600;">💡 About</h3>', unsafe_allow_html=True)
        st.info("""
        **This tool uses:**
        - 🔤 TF-IDF vectorization
        - ✨ Custom features (sentiment, style)
        - 🤖 Logistic Regression classifier
        - 🎯 ~99.47% accuracy
        """)
        
        st.markdown('<h3 style="color: #2c3e50; font-weight: 600;">📖 How to use</h3>', unsafe_allow_html=True)
        st.success("""
        **1.** Paste a news article  
        **2.** Click 'Analyze Article'  
        **3.** Get instant results ✨
        """)
    
    # Analysis
    if analyze_button:
        if article_text.strip():
            with st.spinner("Analyzing article..."):
                # Clean the text to remove metadata
                cleaned_text = clean_article_text(article_text)
                
                # Show what was cleaned (optional debug info)
                if len(cleaned_text) < len(article_text) * 0.9:
                    with st.expander("ℹ️ Text Preprocessing Applied"):
                        st.caption("Metadata and formatting removed for better analysis")
                
                # Make prediction on cleaned text
                prediction = model.predict([cleaned_text])[0]
                confidence = model.predict_proba([cleaned_text])[0]
                
                # Get sentiment from cleaned text
                blob = TextBlob(cleaned_text)
                sentiment = blob.sentiment.polarity
                
                # Display results
                st.markdown("---")
                st.markdown('<h2 style="color: #2c3e50; font-weight: 600; margin-top: 20px;">📊 Analysis Results</h2>', unsafe_allow_html=True)
                
                if prediction == 1:  # Fake
                    st.markdown(f"""
                    <div class="fake-news">
                        <h2>🚨 FAKE NEWS DETECTED</h2>
                        <p style="font-size: 1.2rem;">This article appears to be <strong>FAKE</strong></p>
                        <p><strong>Confidence:</strong> {confidence[1]*100:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # True
                    st.markdown(f"""
                    <div class="true-news">
                        <h2>✅ LIKELY AUTHENTIC</h2>
                        <p style="font-size: 1.2rem;">This article appears to be <strong>TRUE</strong></p>
                        <p><strong>Confidence:</strong> {confidence[0]*100:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Additional metrics
                st.markdown('<h3 style="color: #2c3e50; font-weight: 600; margin-top: 30px;">📈 Additional Insights</h3>', unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Word Count", len(cleaned_text.split()))
                
                with col_b:
                    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                    st.metric("Sentiment", sentiment_label, f"{sentiment:.2f}")
                
                with col_c:
                    caps_ratio = sum(1 for c in cleaned_text if c.isupper()) / max(len(cleaned_text), 1)
                    st.metric("Caps Ratio", f"{caps_ratio*100:.1f}%")
        
        else:
            st.warning("⚠️ Please enter some text to analyze!")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">📰 Fake News Detector</h3>
        <p style="font-size: 1rem; margin-bottom: 10px;">
            ⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. 
            Always verify news from multiple reliable sources before drawing conclusions.
        </p>
        <p style="font-size: 0.95rem; color: #95a5a6; margin-top: 15px;">
            Powered by Machine Learning • TF-IDF • Logistic Regression • TextBlob
        </p>
        <div class="footer-links">
            <a href="https://github.com/Iishita1/Fake-News-Detector" target="_blank">📂 GitHub</a>
            <a href="https://streamlit.io" target="_blank">🚀 Streamlit</a>
            <a href="https://ishita-nanda.vercel.app/" target="_blank">📧 Contact</a>
        </div>
        <p style="margin-top: 20px; font-size: 0.9rem; color: #95a5a6;">
            Made with ❤️ using Python & AI | © 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Failed to load the model. Please check if 'fake_news_model.pkl' exists in the same directory.")
