# Skin-Solutions: AI-Powered Dermatology Analysis System 🏥

This repository contains the code for **Skin-Solutions**, an end-to-end web application developed as part of a Technical Challenge. The system leverages Artificial Intelligence to assist in the detection and classification of various skin lesions from dermatoscopic images.

## ✨ Project Overview

Skin-Solutions aims to provide a professional and intuitive tool for preliminary dermatological image analysis. It showcases a complete machine learning pipeline integrated into a user-friendly web interface.

## 🚀 Key Features

*   **Intuitive Web Interface:** Built with Streamlit, offering a responsive and clean user experience for image upload and result visualization.
*   **Machine Learning Core:** Utilizes a fine-tuned MobileNetV2 model, employing transfer learning for robust skin lesion classification. The model is trained on a balanced subset of the HAM10000 dermatoscopic image dataset.
*   **Comprehensive Analysis Reports:** Generates detailed HTML reports including patient information, AI-derived diagnosis, confidence scores, risk assessments, and clinical recommendations. These can be easily saved and converted to PDF.
*   **Modular Architecture:** Demonstrates best practices in structuring a full-stack machine learning application.
*   **Interactive Analytics:** Provides a 'Reports' section with mock data to visualize system performance and diagnostic distribution.
*   **Clinical Usage Guidelines:** A dedicated 'Instructions' tab offers detailed protocols for image acquisition, analysis, interpretation, and clinical integration.

## 🛠️ Technologies Used

*   **Frontend/Backend Framework:** Streamlit
*   **Machine Learning:** TensorFlow 2.x, Keras, scikit-learn
*   **Data Handling:** Pandas, NumPy, PIL (Pillow)
*   **Plotting:** Plotly Express
*   **Version Control:** Git, GitHub

## 📂 Repository Structure

The project is structured with modular Python files for clear organization and maintainability.

- `Skin-Solutions/`
  - `app.py`                  # Main Streamlit web application
  - `model.py`                # Machine learning model definition and prediction logic
  - `data_loader.py`          # Script for loading and preprocessing the HAM10000 dataset
  - `.gitignore`              # Specifies files/folders to be ignored by Git (e.g., 'data/', model weights)
  - `requirements.txt`        # List of Python dependencies
  - `README.md`               # Project overview and setup instructions
  - `data/`                   # (Local folder for HAM10000 dataset - ignored by Git)
    - `HAM10000_metadata.csv`
    - `HAM10000_images_part_1/`
    - `HAM10000_images_part_2/`
  - `ham10000_trained_model.h5` # (Local file for trained model weights - ignored by Git)
  - `class_names.pkl`         # (Local file for saved class names - ignored by Git)

## 📊 Dataset Information

This project utilizes the **HAM10000 (Human Against Machine with 10000 training images)** dataset, a large collection of multi-source dermatoscopic images of pigmented lesions.

**Note on Dataset Size:** The full HAM10000 dataset is approximately 6GB and is **not included in this repository** due to GitHub's file size limitations.

*   **Download Link:** [Skin Cancer MNIST: HAM10000 on Kaggle](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)
*   **Setup:** After downloading, please extract the `HAM10000_metadata.csv`, `HAM10000_images_part_1/`, and `HAM10000_images_part_2/` into a folder named `data/` in the root of this project.

## ⚙️ Local Setup and Run

To set up and run this project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SUBASHREE-KARUR-SIVAKUMAR/Skin-Solutions.git
    cd Skin-Solutions
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, manually install: `pip install streamlit tensorflow opencv-python scikit-learn pandas numpy matplotlib pillow plotly`)*
4.  **Download the HAM10000 dataset** from the [Kaggle link](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) and place the extracted `HAM10000_metadata.csv`, `HAM10000_images_part_1/`, and `HAM10000_images_part_2/` files/folders into a new directory named `data/` in the project root.
5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser. The first time you run it, the ML model will train on a subset of the downloaded data (this might take 5-15 minutes depending on your system).

## 📄 Documentation

This project serves as a demonstration of end-to-end thinking, problem-solving, and continuous learning. The accompanying comprehensive documentation (as required by the challenge) details:

*   The development journey, including dataset exploration, preprocessing, model selection, and integration.
*   Challenges encountered and their solutions.
*   Rationale behind architectural and technical decisions.
*   Transparent use of AI tools and resources.

## 🌐 Live Demo
https://skin-solutions.streamlit.app
---

**© 2025 ACM-W Technical Challenge | Developed by Subashree**

*Disclaimer: This system is intended for educational and research purposes only and does not constitute medical advice. Always consult qualified healthcare professionals for medical diagnosis and treatment.*
