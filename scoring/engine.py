from .parser import extract_text_from_file
from .hard_match import hard_match_score
from .semantic import semantic_score, semantic_feedback

def evaluate_resume_for_jd(jd_path, resume_path):
    jd_text = extract_text_from_file(jd_path)
    res_text = extract_text_from_file(resume_path)
    hard = hard_match_score(jd_text, res_text)
    soft = semantic_score(jd_text, res_text)
    feedback = semantic_feedback(jd_text, res_text)
    final = round(0.6 * hard + 0.4 * soft, 2)
    verdict = "High" if final >= 75 else ("Medium" if final >= 50 else "Low")
    missing = identify_missing(jd_text, res_text)
    return {"relevance_score": final, "verdict": verdict, "hard_score": hard, "soft_score": soft, "missing_elements": missing, "recommendations": feedback}

def identify_missing(jd_text, res_text):
    import re
    must = []
    m = re.search(r"Must[- ]?have[:\-]?(.*)", jd_text, re.IGNORECASE)
    if m:
        skills = [s.strip() for s in re.split("[,;\n]", m.group(1)) if s.strip()]
        for s in skills:
            if s.lower() not in res_text.lower():
                must.append(s)
    return must
