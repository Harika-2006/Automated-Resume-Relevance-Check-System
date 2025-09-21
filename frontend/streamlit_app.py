import streamlit as st
import requests, os
st.set_page_config(page_title="Resume Relevance Dashboard", layout="wide")
st.title("Automated Resume Relevance Check - MVP")
st.sidebar.header("Upload")
jd_file = st.sidebar.file_uploader("Upload Job Description (pdf/docx/txt)", type=['pdf','docx','txt'])
resume_file = st.sidebar.file_uploader("Upload Resume (pdf/docx/txt)", type=['pdf','docx','txt'])
if 'api_url' not in st.session_state:
    st.session_state['api_url'] = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000")
if jd_file:
    jd_path = os.path.join("tmp", "uploaded_jd_" + jd_file.name)
    os.makedirs("tmp", exist_ok=True)
    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())
    st.success("JD saved locally.")
    st.session_state['last_jd'] = jd_path
if resume_file:
    rpath = os.path.join("tmp", "uploaded_resume_" + resume_file.name)
    with open(rpath, "wb") as f:
        f.write(resume_file.getbuffer())
    st.success("Resume saved locally.")
    st.session_state['last_resume'] = rpath
if st.button("Evaluate (local)"):
    api = st.session_state['api_url']
    if 'last_jd' not in st.session_state or 'last_resume' not in st.session_state:
        st.error("Upload both JD and Resume first.")
    else:
        try:
            resp = requests.post(f"{api}/evaluate/", data={"jd_path": st.session_state['last_jd'], "resume_path": st.session_state['last_resume']}, timeout=30)
            if resp.status_code==200:
                data = resp.json()
                st.metric("Relevance Score", data.get("relevance_score"))
                st.write("Verdict:", data.get("verdict"))
                st.write("Missing Elements:", data.get("missing_elements"))
                st.write("Recommendations:", data.get("recommendations"))
            else:
                st.error(f"Error: {resp.text}")
        except Exception as e:
            st.error(str(e))
