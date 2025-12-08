# backend/summarizer.py

import re
from collections import Counter

SENTENCE_SPLIT_REGEX = r"(?<=[.!?])\s+"

def split_into_sentences(text: str):
    text = text.strip().replace("\n", " ")
    sentences = re.split(SENTENCE_SPLIT_REGEX, text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def get_keywords(text: str, top_k: int = 20):
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = [w for w in text.split() if len(w) > 3]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(top_k)]

def score_sentence(sentence: str, keywords):
    s = sentence.lower()
    return sum(1 for k in keywords if k in s)

def summarize_text(text: str, max_sentences: int = 7):
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    keywords = get_keywords(text)
    if not keywords:
        # fallback: just take the first few sentences
        return sentences[:max_sentences]

    scored = [(score_sentence(s, keywords), idx, s) for idx, s in enumerate(sentences)]
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[:max_sentences]
    top.sort(key=lambda x: x[1])  # keep original order

    return [s for _, _, s in top]
