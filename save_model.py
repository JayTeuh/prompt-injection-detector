"""
save_model.py — train and save the model to disk so the app loads instantly.
Run this once locally. The saved files get committed to the repo.
"""

import joblib

from ml_classifier import model, vectorizer

joblib.dump(vectorizer, "vectorizer.joblib")
joblib.dump(model, "model.joblib")

print("Saved vectorizer.joblib and model.joblib")
