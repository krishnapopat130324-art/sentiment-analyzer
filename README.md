# 🎯 Sentiment Analyzer Pro

> **An AI-powered sentiment analysis platform that transforms customer feedback into actionable insights using Natural Language Processing (NLP).**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-success)

---

# 📖 Table of Contents

* Features
* Use Cases
* Installation
* Usage
* Tech Stack
* Project Structure
* Configuration
* Testing
* Deployment
* Support

---

# ✨ Features

## 🚀 Core Features

* ⚡ Real-time sentiment analysis
* 😊 Positive, Negative, and Neutral classification
* 📊 Interactive statistics dashboard
* 🎨 Modern glassmorphism user interface
* 💾 Export results to CSV
* 📱 Fully responsive design

## 🧠 Advanced Features

* AI-powered sentiment detection using NLP
* Statistical sentiment insights
* Intelligent recommendation system
* Keyword extraction
* Individual review analysis
* Instant processing and feedback

---

# 🎯 Use Cases

## 🏢 For Businesses

* Customer feedback analysis
* Product review monitoring
* Brand reputation tracking
* Customer satisfaction measurement

## 👤 For Individuals

* Product review summarization
* Purchase decision support
* Opinion analysis

## 👨‍💻 For Developers

* NLP experimentation
* API integration
* Learning sentiment analysis concepts

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/krishnapopat130324-art/sentiment-analyzer.git
cd sentiment-analyzer
```

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run the Application

```bash
python app.py
```

Open your browser:

```text
http://localhost:5000
```

---

# 📸 Application Workflow

1. Enter customer reviews.
2. Click **Analyze Sentiment**.
3. Receive:

   * Sentiment classification
   * Confidence levels
   * Statistical insights
   * Overall recommendation

---

# 💻 Tech Stack

## Backend

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Programming Language |
| Flask      | Backend Framework    |
| TextBlob   | NLP Processing       |

## Frontend

| Technology | Purpose       |
| ---------- | ------------- |
| HTML5      | Structure     |
| CSS3       | Styling       |
| JavaScript | Interactivity |

## Development Tools

* Git
* GitHub
* VS Code

---

# 📁 Project Structure

```text
sentiment-analyzer/
│
├── app.py                 # ✅ Main application (contains all HTML/CSS)
├── requirements.txt       # ✅ Dependencies
├── README.md              # ✅ Documentation
├── .gitignore             # ✅ Git ignore rules
├── run.bat                # ✅ Windows launcher (optional)
│
├── .venv/                 # ✅ Virtual environment (auto-created)
│
└── data/                  # ✅ Optional sample data
    └── sample_reviews.csv
```

---

# 🔧 Configuration

Example environment variables:

```env
HOST=0.0.0.0
PORT=5000
DEBUG=True

THRESHOLD_POSITIVE=0.1
THRESHOLD_NEGATIVE=-0.1
```

---

# 🧪 Sample Test Cases

## 😊 Positive Reviews

* Amazing product!
* Highly recommended.
* Best purchase ever.
* Excellent experience overall.

## 😠 Negative Reviews

* Terrible quality.
* Waste of money.
* Very disappointing.
* Would not recommend.

## 😐 Neutral Reviews

* Average product.
* Nothing special.
* Acceptable performance.
* Works as expected.

---

# 🚢 Deployment

## Render

```bash
pip install -r requirements.txt
python app.py
```

## PythonAnywhere

* Upload project files
* Install dependencies
* Configure Flask application
* Deploy

## Hugging Face Spaces

Supports Docker deployment for free hosting.

---

# 📊 Example Output

| Review                       | Sentiment   |
| ---------------------------- | ----------- |
| Amazing product!             | 😊 Positive |
| Poor quality and overpriced. | 😠 Negative |
| Average experience overall.  | 😐 Neutral  |

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

# 👨‍💻 Author

**Krishna Popat**

---

## Made with ❤️ using Flask, Python, and NLP
