"""
ml_classifier.py — a machine learning classifier for prompt injection.
Compares against the rule-based detector on the same benchmark.
"""

from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load the same benchmark we used for the rules
dataset = load_dataset("deepset/prompt-injections")
train_data = dataset["train"]
test_data = dataset["test"]

# Pull out the text and labels into plain lists
train_texts = [row["text"] for row in train_data]
train_labels = [row["label"] for row in train_data]
test_texts = [row["text"] for row in test_data]
test_labels = [row["label"] for row in test_data]

print(f"Training examples: {len(train_texts)}")
print(f"Test examples: {len(test_texts)}")

# Turn text into numbers the model can learn from (TF-IDF)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

# Train the classifier on the training data
model = LogisticRegression(max_iter=1000)
model.fit(X_train, train_labels)

print("Model trained.")

# Run the trained model on the test set
predictions = model.predict(X_test)

# Tally the same four buckets as the rule-based evaluation
true_positives = 0
false_positives = 0
true_negatives = 0
false_negatives = 0

for predicted, actual in zip(predictions, test_labels):
    if predicted == 1 and actual == 1:
        true_positives += 1
    elif predicted == 1 and actual == 0:
        false_positives += 1
    elif predicted == 0 and actual == 0:
        true_negatives += 1
    elif predicted == 0 and actual == 1:
        false_negatives += 1

# Same metrics as Phase 2, computed the same way
precision = (
    true_positives / (true_positives + false_positives)
    if (true_positives + false_positives) > 0
    else 0
)
recall = (
    true_positives / (true_positives + false_negatives)
    if (true_positives + false_negatives) > 0
    else 0
)
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
accuracy = (true_positives + true_negatives) / len(test_labels)

print(f"\n--- ML Classifier Results ---")
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Negatives: {false_negatives}")
print(f"\nPrecision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1 Score: {f1:.2%}")
print(f"Accuracy: {accuracy:.2%}")
