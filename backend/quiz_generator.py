# backend/quiz_generator.py

import re
from typing import List, Dict

from summarizer import get_keywords, split_into_sentences

# Very small stopword set to avoid useless keywords like "what" or "this"
STOPWORDS = {
    "what",
    "that",
    "this",
    "with",
    "have",
    "from",
    "about",
    "would",
    "could",
    "should",
    "there",
    "their",
    "where",
    "these",
    "those",
    "which",
    "maybe",
    "want",
    "will",
    "your",
    "you're",
    "youre",
}


def clean_sentence(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def build_cloze_question(sentence: str, keyword: str, qid: int) -> Dict:
    """
    Create a fill-in-the-blank style question by masking a keyword.
    """
    masked = re.sub(re.escape(keyword), "____", sentence, flags=re.IGNORECASE)
    return {
        "id": qid,
        "type": "fill_blank",
        "question": f"Fill in the blank: {masked}",
        "answer": keyword,
    }


def build_explain_question(keyword: str, context: str, qid: int) -> Dict:
    """
    Ask for an explanation of a key concept with a short context hint.
    """
    hint = context
    if len(hint) > 140:
        hint = hint[:137].rstrip() + "..."
    return {
        "id": qid,
        "type": "short_answer",
        "question": f"Why/How is '{keyword}' important here? (Hint: {hint})",
        "answer": context,
    }


def generate_quiz(text: str, summary_bullets: List[str], num_questions: int = 5) -> List[Dict]:
    """
    Generate quizzes that reflect understanding of the content:
    - Uses keywords from the full text to focus on important concepts.
    - Builds fill-in-the-blank and explain-style questions from real sentences.
    """
    bullets = [clean_sentence(b) for b in summary_bullets if b.strip()]
    sentences = [clean_sentence(s) for s in split_into_sentences(text)]

    keywords = [
        kw
        for kw in get_keywords(text, top_k=40)
        if kw not in STOPWORDS and kw.isalpha()
    ]

    questions: List[Dict] = []
    qid = 1

    # Build cloze questions by masking top keywords in their source sentences
    for kw in keywords:
        if qid > num_questions:
            break
        match = next((s for s in sentences if re.search(rf"\\b{kw}\\b", s, re.IGNORECASE)), None)
        if not match:
            continue
        questions.append(build_cloze_question(match, kw, qid))
        qid += 1

    # If still short on questions, fall back to explain-style from summary bullets
    for bullet in bullets:
        if qid > num_questions:
            break
        key = next((kw for kw in keywords if kw in bullet.lower()), None)
        fallback_kw = key or "this topic"
        questions.append(build_explain_question(fallback_kw, bullet, qid))
        qid += 1

    # Absolute fallback if nothing generated
    if not questions and bullets:
        for bullet in bullets[:num_questions]:
            questions.append(
                {
                    "id": qid,
                    "type": "short_answer",
                    "question": f"What is the main takeaway from: \"{bullet}\"?",
                    "answer": bullet,
                }
            )
            qid += 1

    return questions
