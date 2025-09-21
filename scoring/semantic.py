def semantic_score(jd_text, res_text):
    jd_words = set([w.lower() for w in jd_text.split() if len(w)>3])
    res_words = set([w.lower() for w in res_text.split() if len(w)>3])
    if not jd_words:
        return 0
    overlap = jd_words.intersection(res_words)
    return round((len(overlap)/len(jd_words))*100, 2)

def semantic_feedback(jd_text, res_text):
    jd_words = set([w.lower() for w in jd_text.split() if len(w)>3])
    res_words = set([w.lower() for w in res_text.split() if len(w)>3])
    missing = list(jd_words - res_words)[:10]
    if not missing:
        return "Good semantic coverage. Consider adding quantifiable achievements."
    return "Consider adding or emphasizing: " + ", ".join(missing)
