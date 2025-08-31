\
"""
Summarization utilities with two modes:
1) Abstractive (if Transformers available)
2) Simple extractive fallback (frequency-based sentence scoring)
"""

import re
import math

def _try_transformers_summarize(text: str, max_tokens: int) -> str:
    """
    Try to use Hugging Face Transformers for abstractive summarization.
    Falls back to None if transformers not installed/available at runtime.
    """
    try:
        from transformers import pipeline
        # Use a small, commonly available summarization model
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        # max_tokens ~ max_length in tokens for this pipeline (approximate). Set min_length smaller.
        max_length = max(64, min(300, max_tokens))
        min_length = max(30, min(120, max_tokens // 2))
        chunks = _split_into_chunks(text, max_chars=3000)  # chunk long docs
        out = []
        for ch in chunks:
            s = summarizer(ch, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]
            out.append(s.strip())
        return " ".join(out).strip()
    except Exception:
        return None

def _split_into_chunks(text: str, max_chars: int = 3000):
    """
    Split large text into chunks, trying to break on sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) + 1 > max_chars:
            if cur:
                chunks.append(cur.strip())
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        chunks.append(cur.strip())
    return chunks

def _extractive_fallback(text: str, target_sentences: int = 7) -> str:
    """
    Simple frequency-based extractive summarizer:
    - Tokenize sentences
    - Score sentences by word frequency (after basic normalization)
    - Return top-N in original order
    """
    if not text:
        return ""

    # Basic cleanup
    clean = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    if len(sentences) <= target_sentences:
        return clean

    # Build word frequencies
    words = re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", clean.lower())
    stop = set("""a an the and or but if while of for in on at to from by is are was were be been being this that those these with without within as into than then so such not no nor too very can could would should may might must will just over under between about above below up down out off again further more most less few many each other same own once here there""".split())
    freqs = {}
    for w in words:
        if w in stop or len(w) <= 2:
            continue
        freqs[w] = freqs.get(w, 0) + 1

    # Sentence scores
    sentence_scores = []
    for i, s in enumerate(sentences):
        tokens = re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", s.lower())
        score = sum(freqs.get(t, 0) for t in tokens) / (len(tokens) + 1)
        sentence_scores.append((i, score, s))

    # Pick top sentences by score, then sort back by original order
    top = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:target_sentences]
    top_sorted = sorted(top, key=lambda x: x[0])
    return " ".join(s for (_, _, s) in top_sorted)

def summarize_text(text: str, max_tokens: int = 200) -> str:
    """
    Summarize text. Try Transformers; if unavailable, use extractive fallback.
    """
    if not text or len(text.strip()) == 0:
        return "No content to summarize."
    # First try abstractive
    abstr = _try_transformers_summarize(text, max_tokens=max_tokens)
    if abstr:
        return abstr
    # Fallback extractive: number of sentences based on desired "max_tokens"
    # Rough mapping: assume ~20 tokens per sentence
    target_sentences = max(4, min(15, max_tokens // 20))
    return _extractive_fallback(text, target_sentences=target_sentences)

def get_key_points(summary: str, max_points: int = 5):
    """
    Create bullet-style key points by splitting the summary into concise sentences.
    """
    if not summary:
        return []
    sents = re.split(r'(?<=[.!?])\s+', summary.strip())
    # Keep short-ish sentences as "points"
    points = []
    for s in sents:
        if len(s) < 20:
            continue
        points.append(s.strip())
        if len(points) >= max_points:
            break
    if not points and summary:
        points = [summary.strip()[:120] + ("..." if len(summary) > 120 else "")]
    return points
