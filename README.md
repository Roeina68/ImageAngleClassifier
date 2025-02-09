# Drone Image Angle Classifier

## 📌 Project Overview
This project aims to classify drone images into three categories based on their angle: **Horizontal (0-30°), Diagonal (30-60°), and Vertical (60-90°)**. Using a deep learning model, we process drone images and predict their primary viewpoint.

## 📂 Project Structure
```
📦 drone_angle_classifier
├── data/                  # Raw and processed datasets
├── notebooks/             # Jupyter notebooks for experiments
├── src/                   # Python scripts for data preprocessing, training, and evaluation
├── models/                # Trained models and checkpoints
├── deployment/            # Scripts for model deployment (API/UI)
├── tests/                 # Unit tests for validation
├── reports/               # Documentation and performance analysis
├── .gitignore             # Files and directories ignored by Git
├── README.md              # Project documentation
```

## 🚀 Features
- **Labeled Drone Dataset:** Preprocessed drone images with angle labels.
- **Deep Learning Model:** CNN-based classifier trained to categorize angles.
- **On-the-Fly Preprocessing:** Real-time image augmentation and normalization.
- **Performance Metrics:** Evaluation using accuracy, F1-score, and confusion matrix.
- **Deployment Ready:** Model can be served via an API for inference.

## 🔧 Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drone-angle-classifier.git
   cd drone-angle-classifier
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run a sample notebook:
   ```bash
   jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
   ```

## 🛠️ Usage
- Train the model:
  ```bash
  python src/train.py
  ```
- Evaluate the model:
  ```bash
  python src/evaluate.py
  ```
- Run inference on new images:
  ```bash
  python src/predict.py --image_path sample.jpg
  ```

## 📈 Results & Performance
Check the `reports/` directory for evaluation metrics and model performance analysis.

## 📜 License
This project is licensed under the MIT License.
