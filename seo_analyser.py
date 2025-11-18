import nltk
from collections import Counter
import math

# Ensure NLTK tokenizers exist
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def simple_tfidf(text_list):
    """
    Lightweight TF-IDF alternative without sklearn.
    text_list = list of documents (strings)
    Returns dict with scores for each word.
    """

    # Tokenize documents
    docs = [nltk.word_tokenize(doc.lower()) for doc in text_list]

    # Compute TF
    tf = []
    for doc in docs:
        counts = Counter(doc)
        total = len(doc)
        tf.append({word: counts[word] / total for word in counts})

    # Compute IDF
    doc_count = len(docs)
    idf = {}
    all_words = set(word for doc in docs for word in doc)

    for word in all_words:
        containing = sum(1 for doc in docs if word in doc)
        idf[word] = math.log((doc_count + 1) / (containing + 1)) + 1  # smoothed

    # Compute TF-IDF for each document (if needed)
    tfidf_scores = []
    for doc_tf in tf:
        tfidf_scores.append({word: doc_tf[word] * idf[word] for word in doc_tf})

    # Global score (top overall words)
    global_scores = Counter()
    for tfidf in tfidf_scores:
        for w, s in tfidf.items():
            global_scores[w] += s

    return dict(global_scores)


def seo_recommendations(industry: str):
    """
    Lightweight SEO recommender without scikit-learn.
    Adds auto-generated keyword ideas based on TF-IDF from industry text samples.
    """

    base_keywords = {
        "tech": ["innovation", "cloud", "AI", "scalable", "automation"],
        "design": ["UX", "responsive", "aesthetic", "branding", "typography"],
        "marketing": ["engagement", "analytics", "conversion", "audience", "brand"],
        "business": ["strategy", "leadership", "growth", "insights", "operations"],
    }

    # Some tiny sample documents (safe, small, won't slow Render)
    sample_docs = {
        "tech": [
            "We build scalable AI-driven systems using cloud technologies.",
            "Our focus is innovation and automation for enterprise growth."
        ],
        "design": [
            "Our design approach combines UX principles with modern aesthetics.",
            "We create responsive branding systems with strong visual identity."
        ],
        "marketing": [
            "Data-driven marketing strategies improve engagement and conversion rates.",
            "We optimize audience targeting and brand visibility with analytics."
        ],
        "business": [
            "We provide leadership insights and operational strategy consulting.",
            "Our business solutions focus on sustainable growth and efficiency."
        ]
    }

    industry = industry.lower()

    # Compute TF-IDF suggestions
    if industry in sample_docs:
        tfidf_words = simple_tfidf(sample_docs[industry])
        suggested_keywords = [
            w for w, s in sorted(tfidf_words.items(), key=lambda x: x[1], reverse=True)
            if w.isalpha() and len(w) > 3
        ][:5]  # top 5
    else:
        suggested_keywords = ["portfolio", "professional", "services", "experience"]

    return {
        "recommended_keywords": base_keywords.get(industry, []) + suggested_keywords,
        "meta_tags": [
            "title",
            "description",
            "keywords",
            "og:title",
            "og:description",
            "twitter:card"
        ]
    }
