from sklearn.feature_extraction.text import TfidfVectorizer
import difflib, re
from collections import Counter

def extract_keywords_from_jd(jd_text):
    m = re.search(r"(Required|Responsibilities|Must[- ]?have|Skills)[:\-]?(.*)", jd_text, re.IGNORECASE | re.DOTALL)
    if m:
        parts = m.group(2)
        keywords = [p.strip() for p in re.split("[,;\n]", parts) if p.strip()]
        return keywords
    tokens = [w.lower() for w in jd_text.split() if len(w)>2]
    most = [w for w,_ in Counter(tokens).most_common(10)]
    return most

def hard_match_score(jd_text, res_text):
    keywords = extract_keywords_from_jd(jd_text)
    found = 0
    for k in keywords:
        if k.lower() in res_text.lower():
            found += 1
        else:
            seq = difflib.SequenceMatcher(None, k.lower(), res_text.lower())
            if seq.ratio() > 0.7:
                found += 1
    kw_score = (found / max(1, len(keywords))) * 100 if keywords else 0
    try:
        vec = TfidfVectorizer(stop_words='english').fit_transform([jd_text, res_text])
        sim = (vec * vec.T).A[0,1]
        tfidf_score = sim * 100
    except Exception:
        tfidf_score = 0
    return round(0.6 * kw_score + 0.4 * tfidf_score, 2)
