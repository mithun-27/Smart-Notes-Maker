# backend/quiz_generator.py

import re
from typing import List, Dict

def clean_sentence(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def generate_quiz(text: str, summary_bullets: List[str], num_questions: int = 5) -> List[Dict]:
    """
    Very simple quiz generator:
    - Takes some summary bullets
    - Turns them into 'explain this' / 'what is' questions.
    """
    questions = []

    bullets = [clean_sentence(b) for b in summary_bullets if b.strip()]
    if not bullets:
        return []

    # limit number of bullets used
    bullets = bullets[:num_questions]

    for i, bullet in enumerate(bullets, start=1):
        # Try to build a question from the first few words
        words = bullet.split()
        if len(words) > 5:
            short_context = " ".join(words[:8]) + "..."
        else:
            short_context = bullet

        q_text = f"What is the main idea of: \"{short_context}\"?"
        question_obj = {
            "id": i,
            "question": q_text,
            "type": "short_answer",
            "answer": bullet
        }
        questions.append(question_obj)

    return questions
