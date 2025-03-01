from classifier import classify_repository_ai, classify_description_ai
from classifier import CLASSIFIER_NAMES

results = classify_description_ai(
    "WordPress.org Plugin Mirror", CLASSIFIER_NAMES.PHP, 
    "https://api.deepseek.com/v1/chat/completions", 
    "deepseek-chat", "sk-a946edaed1fb47f99a1cc8e584a836cf"
)

print(results)
