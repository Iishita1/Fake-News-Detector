# 🚀 Deployment Guide

This guide covers deploying the Fake News Detector web app to various platforms.

## 🌐 Live App

**Current Deployment:** [https://fake-news-detection-for-all.streamlit.app/](https://fake-news-detection-for-all.streamlit.app/)

---

## Option 1: Streamlit Cloud (Recommended - FREE)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"!

3. **Done!** Your app will be live in minutes at:
   `https://your-app-name.streamlit.app/`

### Configuration
- Streamlit Cloud automatically reads `requirements.txt`
- Theme settings in `.streamlit/config.toml` are applied
- Model file (`fake_news_model.pkl`) is included in deployment

---

## Option 2: Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Files Needed

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

---

## Option 3: Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build image
docker build -t fake-news-detector .

# Run container
docker run -p 8501:8501 fake-news-detector
```

### Deploy to Docker Hub
```bash
docker tag fake-news-detector yourusername/fake-news-detector
docker push yourusername/fake-news-detector
```

---

## Option 4: AWS (EC2)

### Steps

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Open port 8501 in security group

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   git clone your-repo-url
   cd Fake-News-Detector
   pip3 install -r requirements.txt
   ```

4. **Run with nohup**
   ```bash
   nohup streamlit run app.py --server.port=8501 &
   ```

5. **Access at:** `http://your-ec2-ip:8501`

---

## Option 5: Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Deploy
```bash
# Build and deploy
gcloud run deploy fake-news-detector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 6: Azure Web Apps

### Using Azure CLI
```bash
az webapp up --name fake-news-detector \
  --resource-group myResourceGroup \
  --runtime "PYTHON:3.11"
```

---

## 🔧 Environment Variables

If you need to add secrets or API keys:

### Streamlit Cloud
- Go to app settings
- Add secrets in "Secrets" section
- Access via `st.secrets["key"]`

### Heroku
```bash
heroku config:set SECRET_KEY=your-secret
```

### Docker
```bash
docker run -e SECRET_KEY=your-secret -p 8501:8501 fake-news-detector
```

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics dashboard
- View logs in real-time
- Monitor resource usage

### Custom Monitoring
Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log predictions
logger.info(f"Prediction: {prediction}, Confidence: {confidence}")
```

---

## 🐛 Troubleshooting

### App won't start
- Check `requirements.txt` has all dependencies
- Verify Python version (3.11+)
- Ensure `fake_news_model.pkl` is included

### Model file too large
- Use Git LFS for large files
- Or host model separately (S3, Google Cloud Storage)

### Slow performance
- Upgrade to paid tier for more resources
- Optimize model loading with `@st.cache_resource`
- Consider model compression

---

## 📈 Scaling

For high traffic:
1. Use load balancer
2. Deploy multiple instances
3. Consider serverless (AWS Lambda + API Gateway)
4. Cache predictions for common articles

---

## 🔒 Security

- Never commit API keys or secrets
- Use environment variables
- Enable HTTPS (automatic on most platforms)
- Add rate limiting if needed

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid |
|----------|-----------|------|
| Streamlit Cloud | ✅ Unlimited public apps | $20/month for private |
| Heroku | ❌ (discontinued) | $7/month |
| AWS EC2 | ✅ 750 hours/month | ~$10/month |
| Google Cloud Run | ✅ 2M requests/month | Pay per use |
| Azure | ✅ Limited | ~$13/month |

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)

---

**Questions?** Open an issue on GitHub!
