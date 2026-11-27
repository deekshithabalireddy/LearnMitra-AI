# LearnMitra AI – Learning Analytics Dashboard

## 📌 Project Overview

LearnMitra AI is an AI-supported learning platform designed to make learning easier, smarter, and more interactive.

The platform provides AI-powered learning assistance, multilingual translation, quizzes, chat support, learning history, and learning analytics to help users understand and track their learning activities.

## ✨ Features

- **AI Learning Assistant:** Provides AI-powered explanations and learning support.
- **Multilingual Translator:** Supports translation between different languages.
- **Interactive Quizzes:** Helps users test their knowledge.
- **Chat Support:** Enables interactive conversations.
- **Learning History:** Maintains learning activity history.
- **Learning Analytics Dashboard:** Visualizes learning activities and usage statistics.
- **Language-wise Analytics:** Displays language usage patterns.
- **Activity Tracking:** Tracks explanations, quizzes, translations, and chat sessions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| HTML | Frontend structure |
| CSS | Styling and responsive design |
| JavaScript | Frontend functionality |
| Python | Backend and analytics |
| FastAPI | Backend API |
| Streamlit | Analytics dashboard |
| MongoDB Atlas | Database |
| Google Gemini AI | AI-powered assistance |
| Pandas | Data processing |
| Plotly | Data visualization |

## 📁 Project Structure

```text
LearnMitra-AI/
│
├── analytics/
├── backend/
│   ├── app.py
│   ├── database.py
│   └── requirements.txt
│
├── data/
│   └── learnmitra_activity.csv
│
├── frontend/
│   ├── index.html
│   ├── assistant.html
│   ├── chat.html
│   ├── history.html
│   ├── quiz.html
│   ├── translator.html
│   ├── style.css
│   └── JavaScript files
│
├── streamlit_app/
│   └── dashboard.py
│
├── requirements.txt
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/deekshithabalireddy/LearnMitra-AI.git
```

### 2. Navigate to the Project Folder

```bash
cd LearnMitra-AI
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Streamlit Dashboard

```bash
streamlit run streamlit_app/dashboard.py
```

The dashboard will open at:

`http://localhost:8501`

## 🔐 Environment Variables

Configure the required API keys and database connection details using environment variables.

Do not upload `.env` files, API keys, or database credentials to GitHub.

For cloud deployment, configure secrets through the hosting platform.

## 📊 Dashboard Analytics

The LearnMitra AI dashboard provides:

- Total Learning Activities
- Total Explanations
- Total Quizzes
- Total Translations
- Total Chat Sessions
- Daily Learning Activity Trend
- Language-wise Usage
- Activity-wise Usage

## 🌐 Deployment

- **Source Code:** GitHub
- **Analytics Dashboard:** Streamlit Community Cloud
- **Database:** MongoDB Atlas

## 🎯 Project Objective

The main objective of LearnMitra AI is to create an interactive and intelligent learning environment by combining AI-powered learning assistance with data-driven learning analytics.

## 👩‍💻 Developer

**Deekshitha Balireddy**

B.Tech – School of Computing and Data Science

Sai University
