# Emotion Detection Mini Project (No Libraries Used)

print("=== Emotion Detection System ===")
print("Enter a sentence and I will detect the emotion.\n")

emotion_words = {
    "happy": ["happy", "joy", "smile", "smiling", "excited", "great", "awesome", "content", "cheerful", "delighted", "pleased", "satisfied"],
    "sad": ["sad", "cry", "cried", "depressed", "unhappy", "lonely", "sorrow", "gloomy", "melancholy", "miserable", "down"],
    "angry": ["angry", "mad", "furious", "annoyed", "hate", "irritated", "outraged", "resentful", "angst", "aggravated"],
    "fear": ["fear", "scared", "afraid", "nervous", "panic", "anxious", "terrified", "uneasy", "frightened", "alarmed"],
    "love": ["love", "like", "care", "affection", "heart", "adore", "fond", "cherish", "loving", "passion"]
}

import argparse
import string
import sys


def detect_emotion(text: str):
    """Return (detected_emotion, scores, confidence, ties) for the given text."""
    # Normalize and strip punctuation for more robust matching
    text_clean = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text_clean.split()

    scores = {emotion: 0 for emotion in emotion_words}

    for word in words:
        for emotion, lex in emotion_words.items():
            if word in lex:
                scores[emotion] += 1

    total_matches = sum(scores.values())
    max_score = 0
    for score in scores.values():
        if score > max_score:
            max_score = score

    ties = [emotion for emotion, score in scores.items() if score == max_score and score > 0]

    if max_score == 0:
        detected_emotion = "neutral"
        confidence = 0.0
    elif len(ties) > 1:
        # Tie detected; report neutral to indicate ambiguity
        detected_emotion = "neutral"
        confidence = max_score / total_matches if total_matches else 0.0
    else:
        detected_emotion = ties[0]
        confidence = max_score / total_matches if total_matches else 0.0

    return detected_emotion, scores, confidence, ties


def main():
    parser = argparse.ArgumentParser(
        description='Simple rule-based emotion detection (non-ML)')
    parser.add_argument('--test', action='store_true', help='Run sample inputs non-interactively')
    parser.add_argument('--input', '-i', type=str, help='Provide a single input string to analyze (non-interactive)')
    args = parser.parse_args()

    if args.test:
        samples = [
            "I am happy",
            "I feel sad and lonely",
            "I hate this",
            "I'm scared and nervous",
            "I love you",
            "I'm excited and happy!",
            "I'm sad, depressed, and lonely...",
            "I am happy but also sad"
        ]
        for s in samples:
            detected, scores, confidence, ties = detect_emotion(s)
            tie_str = f" (ties: {', '.join(ties)})" if ties else ""
            print(f"Input: {s}\nDetected Emotion: {detected.upper()} (confidence: {confidence:.2f}){tie_str}\n")
        return

    if args.input:
        detected, scores, confidence, ties = detect_emotion(args.input)
        tie_str = f" (ties: {', '.join(ties)})" if ties else ""
        print(f"\nDetected Emotion: {detected.upper()} (confidence: {confidence:.2f}){tie_str}")
        return

    # Interactive mode
    try:
        text = input("Enter your text: ")
    except EOFError:
        print("\nNo input received. Exiting.")
        return

    detected, scores, confidence, ties = detect_emotion(text)
    tie_str = f" (ties: {', '.join(ties)})" if ties else ""
    print(f"\nDetected Emotion: {detected.upper()} (confidence: {confidence:.2f}){tie_str}")

if __name__ == "__main__":
    main()