# Personalized Recipe Generation with AI

# 🍽️ FlavorForge - AI-Powered Recipe Generator

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)

Generate personalized recipes with AI based on your available ingredients and dietary restrictions.

---

## ✨ Features

- 🤖 **AI-Powered Recipe Generation**  
  Uses Meta LLaMA 3.1 via OpenRouter to generate 3 unique recipes  

- 🚫 **Allergy Awareness**  
  Automatically excludes ingredients based on dietary restrictions  

- 📊 **Nutrition Estimates**  
  Get calories, protein, carbs, and fat per serving  

- 📝 **Recipe History**  
  Track all previously generated recipes  

- ❤️ **Favorites System**  
  Save and organize favorite recipes  

- 🔐 **Secure Authentication**  
  JWT-based authentication with bcrypt hashing  

---

## 🛠️ Tech Stack

| Component  | Technology |
|------------|-----------|
| Frontend   | Streamlit |
| Backend    | Flask REST API |
| Database   | MySQL |
| AI Model   | LLaMA 3.1-8B-Instruct (OpenRouter) |
| Auth       | JWT + bcrypt |

---

## 📋 Prerequisites

Make sure you have:

- Python 3.11+
- MySQL Server running
- OpenRouter API Key → https://openrouter.ai

---
### Project Structure

personalized_recipe_ai/
│
#
├── backend/
#
|
#
│
#
├── app.py
#
│
#
├── ai_engine.py
│   ├── auth.py
│   ├── db.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── Home.py
│   ├── pages/
│   │   ├── 0_Profile.py
│   │   ├── 1_Explore.py
│   │   ├── 2_Saved.py
│   │   ├── 3_Logout.py
│   │   └── 4_History.py
│   └── requirements.txt
│
├── .env
├── .gitignore
└── README.md

---
### API Endpoints

| Endpoint         | Method | Auth | Description       |
| ---------------- | ------ | ---- | ----------------- |
| /register        | POST   | ❌    | Register user     |
| /login           | POST   | ❌    | Login & get token |
| /generate        | POST   | ✅    | Generate recipes  |
| /history         | GET    | ✅    | Get history       |
| /favorite        | POST   | ✅    | Save recipe       |
| /favorites       | GET    | ✅    | Get favorites     |
| /update-allergy  | PUT    | ✅    | Update allergy    |
| /update-password | PUT    | ✅    | Change password   |

---
### Usage Example

1. Register a new account with email and password
2. Login with your credentials
3. Go to Explore page
4. Enter your available ingredients (e.g., "chicken, garlic, tomatoes, rice")
5. Click Generate Recipes
6. View 3 AI-generated recipes
	--Cooking time & difficulty
	--Ingredients with quantities
	--Step-by-step instructions
	--Nutrition information
7. You can also save your favorite recipes.

---
### License
This project is for educational purposes.

_______________________________________________________________________________________________________

### Made with ❤️ by FlavorForge Team

