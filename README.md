# 🌱 GreenKart AI: Sustainability & Eco-Score Predictor

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-15B550?style=for-the-badge&logo=xgboost&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

> **"Bridging the gap between Supply Chain Data and Environmental Action using Machine Learning & GenAI."**

### 🚀 [**View Live Demo**](https://eco-score-predictor.onrender.com)

---

## 📖 Overview
**GreenKart AI** is an intelligent auditing tool designed to quantify the environmental impact of consumer products. It moves beyond simple analytics by combining **Predictive AI** (to calculate risk) with **Generative AI** (to offer solutions).

In a corporate context, this mimics an **ESG Compliance System**, helping supply chain managers not just *measure* their carbon footprint, but actively *reduce* it through AI-driven consulting.

---

## 📸 Interface
| **Input Parameters** | **AI-Generated Consultant Report** |
|:---:|:---:|
| <img src="assets\Screenshot (3536).png" width="400"> | <img src="assets\Screenshot (3537).png" width="400"> | 

---

## 🏗️ System Architecture
The application follows a **Hybrid AI Architecture**, integrating a regression model for scoring and an LLM for reasoning.

```mermaid
graph LR
    A[User Input] -->|Materials, Distance, Weight| B(Data Preprocessing);
    B -->|Encoded Features| C{XGBoost Engine};
    C -->|Predicts| D[Eco Score 0-100];
    D --> E[Gemini AI Agent];
    A --> E;
    E -->|Generates Strategy| F[Actionable Recommendations];
    D --> G[Streamlit Dashboard];
    F --> G;
