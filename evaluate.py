"""
evaluate.py — measure the detector against a labeled dataset.
"""

from datasets import load_dataset

from detector import get_verdict

# Load the benchmark. label 1 = injection, 0 = legitimate.
dataset = load_dataset("deepset/prompt-injections")

# Look at the test split
test_data = dataset["test"]

print(f"Number of test examples: {len(test_data)}")
print(f"First example: {test_data[0]}")

# Count how many are injections vs benign
num_injections = sum(1 for row in test_data if row["label"] == 1)
num_benign = sum(1 for row in test_data if row["label"] == 0)
print(f"Injections: {num_injections}, Benign: {num_benign}")

# Run the detector on every test example and tally results
true_positives = 0  # injection correctly flagged
false_positives = 0  # benign wrongly flagged
true_negatives = 0  # benign correctly passed
false_negatives = 0  # injection missed

injections_with_any_match = (
    0  # injections where at least one rule fired, regardless of score
)

for row in test_data:
    text = row["text"]
    true_label = row["label"]  # 1 = injection, 0 = benign

    verdict = get_verdict(text)
    predicted = 1 if verdict["is_injection"] else 0

    if predicted == 1 and true_label == 1:
        true_positives += 1
    elif predicted == 1 and true_label == 0:
        false_positives += 1
    elif predicted == 0 and true_label == 0:
        true_negatives += 1
    elif predicted == 0 and true_label == 1:
        false_negatives += 1

    if true_label == 1 and len(verdict["matches"]) > 0:
        injections_with_any_match += 1

print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Negatives: {false_negatives}")

# Compute the standard detection metrics
# Guard against dividing by zero
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
accuracy = (true_positives + true_negatives) / len(test_data)

print(f"\nPrecision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1 Score: {f1:.2%}")
print(f"Accuracy: {accuracy:.2%}")

# Diagnostic: how many injections matched a rule at all (even if score was too low to flag)
print(
    f"\nInjections that matched at least one rule: {injections_with_any_match} / {num_injections}"
)

# Show a sample of missed attacks (false negatives) to understand the gap
print("\n--- Sample of missed attacks (false negatives) ---")
shown = 0
for row in test_data:
    if shown >= 8:
        break
    verdict = get_verdict(row["text"])
    predicted = 1 if verdict["is_injection"] else 0
    if predicted == 0 and row["label"] == 1:
        # truncate long ones so output stays readable
        snippet = row["text"][:150]
        print(f"\nMISSED: {snippet}")
        shown += 1
