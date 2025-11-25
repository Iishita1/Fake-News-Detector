# 📰 Fake News Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fake-news-detection-for-all.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust NLP + ML pipeline to classify news articles as Fake or True using a hybrid approach:
- TF-IDF features (uni/bi/tri-grams)
- Handcrafted features (lexical, stylistic, sentiment via TextBlob)
- Logistic Regression classifier
- **Live Web App** for instant predictions

> Built to help analyze and mitigate misinformation by combining semantic and stylistic cues.

## 🌐 Try It Live!

**[Launch Web App →](https://fake-news-detection-for-all.streamlit.app/)**

Simply paste any news article and get instant AI-powered analysis!

---

## 📂 Project Structure

```text
Fake-News-Detector/
├─ app.py                      # Streamlit web application
├─ fake_news_model.pkl         # Trained ML model
├─ requirements.txt            # Python dependencies
├─ Datasets/
│  ├─ Fake.csv                # Fake news dataset
│  └─ True.csv                # True news dataset
├─ FakeNewsPredictor.ipynb    # Model training notebook
├─ .streamlit/
│  └─ config.toml             # Streamlit configuration
├─ README.md
└─ WEBAPP_README.md           # Web app documentation
```

**Key Files:**
* **`app.py`**: Interactive Streamlit web application (deployed live!)
* **`fake_news_model.pkl`**: Trained model with ~99.47% accuracy
* **`FakeNewsPredictor.ipynb`**: End-to-end workflow (EDA → training → evaluation)
* **`Datasets/`**: Core labeled datasets for training
  
---

## 🚀 Features

- Hybrid feature engineering:
  - TF-IDF with n-grams up to 3
  - Manual features: word count, avg word length, caps ratio, exclamations, subjectivity, polarity
- Careful text cleaning to avoid source leakage (e.g., removing patterns like “(Reuters) - ...”)
- Train/test split with reproducibility
- Confusion matrix and detailed classification report
- Interactive predictor with confidence bands and contextual reasoning

---

## 🧠 Model & Approach

- Vectorization: `TfidfVectorizer(max_features=8000, ngram_range=(1,3), stop_words='english', sublinear_tf=True)`
- Manual features: via a custom `ManualFeatureExtractor`
- Feature union: `FeatureUnion([tfidf, manual])`
- Scaling: `StandardScaler(with_mean=False)` to support sparse matrices
- Classifier: `LogisticRegression(C=1.0, max_iter=1000, solver='liblinear')`

---

## 📊 Results

- Test Accuracy: ~99.47%
- Evaluation: Accuracy, Precision/Recall/F1 (per class), Confusion Matrix
- Insight: Hybrid features capture both semantic content and stylistic/sentiment signal that helps distinguish fake from true articles.

Note: Reported metrics are based on the given dataset and current preprocessing choices.

---

## 🛠️ Setup

### 1) Create environment
```bash
# Option A: venv (Windows PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# Option B: conda
conda create -n news-detector python=3.10 -y
conda activate news-detector
```
### 2) Install dependencies
```bash
pip install -U pip
pip install pandas numpy requests beautifulsoup4 matplotlib seaborn scikit-learn nltk textblob
```
### 3) NLTK & TextBlob data (first run may auto-download)
The notebook already attempts:

```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
```

## ▶️ Usage

### Option A: Use the Web App (Recommended)

**[Visit the Live App →](https://fake-news-detection-for-all.streamlit.app/)**

1. Paste any news article into the text box
2. Click "Analyze Article"
3. Get instant results with confidence scores and insights

### Option B: Run Locally

```bash
# Clone the repository
git clone <your-repo-url>
cd Fake-News-Detector

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Option C: Train Your Own Model

1. Open **`FakeNewsPredictor.ipynb`** in Jupyter or VS Code
2. Run cells top-to-bottom to:
   - Load and explore datasets
   - Train the model
   - Evaluate performance
   - Export the trained model

---

## 📁 Data

**Provided:**

* `Datasets/Fake.csv`
* `Datasets/True.csv`

**Columns used:**

* **`text`** (main body), **`title`** (fallback), and **`label`** (0 = True, 1 = Fake; assigned in notebook)

**Preprocessing:**

* Fill missing `text`/`title` with empty strings
* Shuffle data for unbiased splits
* Boilerplate/source removal to reduce leakage

**Note:** If using alternative datasets, ensure a similar schema with a **`text`** field.

---

## 📈 EDA Highlights

* **Class distribution visualization** (True vs Fake classes)
* **Article length** (word count) histograms by class
* Observations on **stylistic patterns** (e.g., capitalization, punctuation), **sentiment tendencies**

---

## 🚀 Deployment

This project is deployed on **Streamlit Cloud** and accessible worldwide:

**Live App:** [https://fake-news-detection-for-all.streamlit.app/](https://fake-news-detection-for-all.streamlit.app/)

### Deploy Your Own

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

## 🧩 Future Enhancements

* **Advanced Models:** Experiment with BERT, RoBERTa, or ensemble methods
* **Multilingual Support:** Extend to detect fake news in multiple languages
* **Real-time Scraping:** Integrate with news APIs for live article analysis
* **Explainability:** Add LIME/SHAP for model interpretability
* **Mobile App:** Create React Native or Flutter version
* **Browser Extension:** Chrome/Firefox extension for on-the-fly fact-checking

---

## ⚠️ Notes & Limitations

* High accuracy can reflect dataset characteristics and **potential residual biases**.
* Real-world performance depends on **domain shift**, writing styles, and **adversarial content**.
* Use as a **decision aid**, not a sole arbiter of truth.

---

## 📦 Requirements

* **Python** 3.9–3.11
* **Packages:**
    * `pandas`, `numpy`, `requests`, `beautifulsoup4`
    * `matplotlib`, `seaborn`
    * `scikit-learn`
    * `nltk`, `textblob`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙌 Acknowledgments

* Dataset sources derived from public fake/true news corpora
* Built with [Streamlit](https://streamlit.io/), [scikit-learn](https://scikit-learn.org/), and [TextBlob](https://textblob.readthedocs.io/)
* Deployed on [Streamlit Cloud](https://streamlit.io/cloud)

## 📧 Contact

Have questions or feedback? Feel free to reach out or open an issue!

---

**⭐ If you find this project useful, please consider giving it a star!**

