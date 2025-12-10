# backend/summarizer.py

import re
from collections import Counter
from typing import List

SENTENCE_SPLIT_REGEX = r"(?<=[.!?])\s+"


def normalize_text(text: str) -> str:
    """Collapse whitespace and strip stray symbols for cleaner processing."""
    return re.sub(r"\s+", " ", text).strip()


def split_into_sentences(text: str) -> List[str]:
    text = normalize_text(text.replace("\n", " "))
    sentences = re.split(SENTENCE_SPLIT_REGEX, text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def chunk_by_words(text: str, max_words: int = 40) -> List[str]:
    """
    If the transcript lacks punctuation, create pseudo-sentences every N words
    so summarization still has multiple units to choose from.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def get_keywords(text: str, top_k: int = 20) -> List[str]:
    """Return top keywords by frequency (length > 3 chars, alnum only)."""
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = [w for w in text.split() if len(w) > 3]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(top_k)]


def score_sentence(sentence: str, keywords: List[str], position_weight: float = 0.15) -> float:
    """
    Score a sentence by keyword coverage and slight positional bias
    (earlier sentences get a tiny bump to keep context).
    """
    s = sentence.lower()
    keyword_score = sum(1 for k in keywords if k in s)
    return keyword_score + position_weight


def too_similar(a: str, b: str, threshold: float = 0.6) -> bool:
    """
    Rough deduplication using Jaccard overlap of word sets.
    Prevents repeating the same idea across bullets.
    """
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a or not set_b:
        return False
    overlap = len(set_a & set_b) / len(set_a | set_b)
    return overlap >= threshold


def format_bullet(sentence: str, max_len: int = 200) -> str:
    """Trim long sentences and remove trailing punctuation for cleaner bullets."""
    sentence = normalize_text(sentence)
    if len(sentence) > max_len:
        sentence = sentence[: max_len - 3].rstrip() + "..."
    return sentence.rstrip(".;:")


def summarize_text(text: str, max_sentences: int = 7) -> List[str]:
    """
    Extractive summarization aimed at producing concise lecture notes/keypoints.
    - Scores sentences by keyword coverage.
    - Deduplicates overlapping sentences.
    - Returns trimmed, note-friendly bullets.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    # If punctuation is sparse and we got too few sentences, fall back to word chunks
    if len(sentences) < 3:
        sentences = chunk_by_words(text, max_words=40)
        if not sentences:
            return []

    keywords = get_keywords(text)
    if not keywords:
        return [format_bullet(s) for s in sentences[:max_sentences]]

    scored = [(score_sentence(s, keywords), idx, s) for idx, s in enumerate(sentences)]
    scored.sort(key=lambda x: (-x[0], x[1]))

    selected: List[str] = []
    seen_bullets = set()
    for _, _, sentence in scored:
        if len(selected) >= max_sentences:
            break
        if any(too_similar(sentence, keep) for keep in selected):
            continue
        bullet = format_bullet(sentence)
        norm = bullet.lower()
        if norm in seen_bullets:
            continue
        seen_bullets.add(norm)
        selected.append(bullet)

    # If we didn't reach max bullets (e.g., heavy deduplication), top up in order.
    if len(selected) < max_sentences:
        for _, _, sentence in sorted(scored, key=lambda x: x[1]):
            if len(selected) >= max_sentences:
                break
            if any(too_similar(sentence, keep) for keep in selected):
                continue
            bullet = format_bullet(sentence)
            norm = bullet.lower()
            if norm in seen_bullets:
                continue
            seen_bullets.add(norm)
            selected.append(bullet)

    return selected
