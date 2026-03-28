# JEE-TOPIC-CLASSIFIER-WITH-AIML
A Python-based desktop application designed for JEE Main aspirants to generate structured 75-question mock exam blueprints. 
# JEE Assistant Pro - Mock Paper Architect

## 📌 Project Overview
**JEE Assistant Pro** is a professional-grade Python desktop application designed to assist JEE Main aspirants. The tool generates structured 75-question mock exam blueprints (25 Physics, 25 Chemistry, and 25 Mathematics) based on the official syllabus.

To simulate real-world exam variability, the application implements a **skewed difficulty algorithm**. Instead of a fixed distribution, each generated paper features a unique, randomized weight for Easy, Medium, and Hard questions. Additionally, the app provides a **Strategy Hub** with personalized preparation tips tailored to the complexity of the generated paper.

## 🚀 Features
- **Automated Blueprint Generation:** Instant 75-question paper structure.
- **Dynamic Difficulty Scaling:** Randomized complexity ratios (Easy/Medium/Hard) for every session.
- **Personalized Strategy Hub:** Unlocks 6 targeted preparation tips after generation.
- **Subject-Coded UI:** Visual subject markers (Violet for Physics, Emerald for Chemistry, Blue for Maths).
- **CSV Export:** Save your mock blueprints locally for offline tracking.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** Tkinter (Standard Library)
- **Data Analysis:** Pandas

---

## 📥 Setup & Installation

Follow these steps to set up the environment and install dependencies.

###  Prerequisites
Ensure you have **Python 3.8 or higher** installed on your system.
## Concepts used in the Project
This document outlines the core Artificial Intelligence and Machine Learning principles implemented within the project. While the application is optimized for local performance, it utilizes several foundational AI paradigms to achieve its functionality.
# 1. Rule-Based Expert Systems (Symbolic AI)
The core of the Topic Classifier is built upon the "Rule-Based" or "Knowledge-Based" AI paradigm.
~ Concept: Unlike "Black Box" models, symbolic AI uses a predefined set of rules (keywords mapped to subjects) to reach a conclusion.
~ Implementation: The project utilizes a Knowledge Base (the topics_map) and an Inference Engine (the classification logic) to map unstructured text input to a specific category in the JEE syllabus.
~ Significance: This ensures 100% explainability, which is critical in educational tools where the user must understand why a question was categorized a certain way.
# 2. Stochastic Modeling & Probability Distributions
The Mock Paper Generator utilizes stochastic (randomized) processes to simulate real-world variability.
~ Concept: Instead of using a fixed/deterministic output, the system uses Weighted Random Sampling.
~ Implementation: The application generates a unique Probability Distribution for every session:
          - P(Easy) = w1
          - P(Medium) = w2
          - P(Hard) = w3
~ Significance: This simulates the "Entropy" or unpredictability of an actual competitive exam, ensuring that no two mock papers are identical, thereby providing better training data for the student.
# 3. Heuristic Search & Recommendation Logic
~ The Strategy Hub acts as a primitive "Recommender System" using heuristic evaluation.
~ Concept: Heuristics are "mental shortcuts" or rules of thumb used by AI to make quick decisions without exhaustive computation.
~ Implementation: The system performs a Complexity Analysis on the generated dataset. If the frequency of "Hard" labels exceeds a specific heuristic threshold (e.g., N > 28), the AI triggers a specific "Complexity Alert" and adjusts the recommendation pool.
~ Significance: This mimics a human mentor's ability to look at a paper and immediately identify if it is "tough" or "balanced."
# 4. Data Representation & Feature Mapping
~ Concept: In Machine Learning, raw data must be structured into features that a machine can process.
~ Implementation: The project structures the vast JEE syllabus into a Mapped Data Structure (Dictionaries/DataFrames). By organizing data into Subject -> Topic ->  ~ Complexity, the system treats these as categorical features for both the generator and the reporter.
~ Significance: This structured representation is the prerequisite for any future upgrade to supervised learning models (like Random Forests or Neural Networks).

