import streamlit as st
import re
import fitz

# --- Highlighting Function ---
def highlight_keywords(text, keyword_dict):
    sorted_keywords = sorted(keyword_dict.keys(), key=len, reverse=True)

    for phrase in sorted_keywords:
        explanation = keyword_dict[phrase]

        # Choose a color based on explanation category
        if "Broad" in explanation:
            color = "#c8f7c5"  # soft green
        elif "Narrow" in explanation:
            color = "#f7c6c7"  # soft red
        elif "vague" in explanation.lower():
            color = "#fff3cd"  # yellow-ish
        elif "functional" in explanation.lower():
            color = "#dbeafe"  # soft blue
        elif "means-plus-function" in explanation.lower():
            color = "#fce4ec"  # pink
        else:
            color = "#e0e0e0"  # gray fallback

        # ✅ Define the regex pattern here (previously missing)
        pattern = re.compile(rf"\b({re.escape(phrase)})\b", re.IGNORECASE)

        # Apply highlight with visible black text
        replacement = (
            rf'<span style="background-color: {color}; color: black; padding: 2px 4px; border-radius: 4px;" '
            rf'title="{explanation}">\1</span>'
        )
        text = pattern.sub(replacement, text)

    return text

def extract_text_from_pdf(file):
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip()
    except Exception as e:
        return f"⚠️ Error reading PDF: {e}"

def calculate_breadth_score(text):
    score = 0

    scoring_rules = {
        "comprising": 2,
        "consisting essentially of": 1,
        "consisting of": -2,
        "configured to": 1,
        "adapted to": 1,
        "means for": -1,
        "substantially": -1,
        "about": -1,
    }

    for phrase, points in scoring_rules.items():
        occurrences = len(re.findall(rf"\b{re.escape(phrase)}\b", text, re.IGNORECASE))
        score += occurrences * points

    return score

def get_claim_stats(text, keywords):
    word_count = len(re.findall(r"\b\w+\b", text))

    keyword_hits = 0
    transition_type = "None"
    is_dependent = False

    for word in keywords:
        count = len(re.findall(rf"\b{re.escape(word)}\b", text, re.IGNORECASE))
        keyword_hits += count

        # Detect transition type
        if word in ["comprising", "consisting of", "consisting essentially of"] and count > 0:
            transition_type = word

    # Look for dependent claim indicators
    if re.search(r"\b(wherein|according to)\b", text, re.IGNORECASE):
        is_dependent = True

    return {
        "word_count": word_count,
        "keyword_hits": keyword_hits,
        "transition_type": transition_type,
        "is_dependent": is_dependent
    }

# --- Config ---
st.set_page_config(page_title="Claim Language Analyzer", layout="centered")

st.markdown("## 📂 Optional: Upload .txt Files")

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    uploaded_file_1 = st.file_uploader("Upload Claim 1 (.txt or .pdf)", type=["txt", "pdf"], key="file1")

with upload_col2:
    uploaded_file_2 = st.file_uploader("Upload Claim 2 (.txt or .pdf)", type=["txt", "pdf"], key="file2")
# Read uploaded files if available
claim_text_1 = ""
claim_text_2 = ""

if uploaded_file_1 is not None:
    if uploaded_file_1.name.endswith(".pdf"):
        claim_text_1 = extract_text_from_pdf(uploaded_file_1)
    else:
        claim_text_1 = uploaded_file_1.read().decode("utf-8")

if uploaded_file_2 is not None:
    if uploaded_file_2.name.endswith(".pdf"):
        claim_text_2 = extract_text_from_pdf(uploaded_file_2)
    else:
        claim_text_2 = uploaded_file_2.read().decode("utf-8")


st.title("🔍 Claim Language Analyzer")
st.markdown("Paste a **patent claim** below. We'll highlight key legal phrases and structures.")

# --- Input ---
st.markdown("## ✍️ Or Enter Claims Manually")

col1, col2 = st.columns(2)

with col1:
    if not claim_text_1:
        claim_text_1 = st.text_area("📄 Claim 1", height=250, key="claim1")

with col2:
    if not claim_text_2:
        claim_text_2 = st.text_area("📄 Claim 2", height=250, key="claim2")

# --- Keyword Rules ---
keywords = {
    "comprising": "🟢 Broad transition word",
    "consisting of": "🔴 Narrow transition word",
    "consisting essentially of": "🟠 Semi-narrow transition",
    "adapted to": "⚙️ Functional language",
    "configured to": "⚙️ Functional language",
    "means for": "⚠️ Possible means-plus-function",
    "wherein": "📌 Dependent claim marker",
    "substantially": "⚠️ Vague modifier",
    "about": "⚠️ Vague modifier",
}

# --- Output ---
if claim_text_1.strip() or claim_text_2.strip():
    st.markdown("## 🔬 Comparison Results")
    
    if claim_text_1.strip() and claim_text_2.strip():
        score1 = calculate_breadth_score(claim_text_1)
        score2 = calculate_breadth_score(claim_text_2)

        st.markdown("### ⚖️ Breadth Score Comparison")
        if score1 > score2:
            st.success("Claim 1 appears broader.")
        elif score1 < score2:
            st.success("Claim 2 appears broader.")
        else:
            st.info("Both claims are equally broad.")

    if claim_text_1.strip():
        st.subheader("📄 Claim 1")
        score1 = calculate_breadth_score(claim_text_1)
        stats1 = get_claim_stats(claim_text_1, keywords)
        highlighted1 = highlight_keywords(claim_text_1, keywords)

        col1a, col1b = st.columns(2)
        col1a.metric("Breadth Score", score1)
        col1b.metric("Transition", stats1["transition_type"].capitalize() if stats1["transition_type"] != "None" else "Not found")

        col2a, col2b = st.columns(2)
        col2a.metric("Word Count", stats1["word_count"])
        col2b.metric("Dependent", "✅ Yes" if stats1["is_dependent"] else "❌ No")

        st.markdown("**🔦 Highlighted Claim**")
        st.markdown(highlighted1, unsafe_allow_html=True)
        st.divider()

    if claim_text_2.strip():
        st.subheader("📄 Claim 2")
        score2 = calculate_breadth_score(claim_text_2)
        stats2 = get_claim_stats(claim_text_2, keywords)
        highlighted2 = highlight_keywords(claim_text_2, keywords)

        col1a, col1b = st.columns(2)
        col1a.metric("Breadth Score", score2)
        col1b.metric("Transition", stats2["transition_type"].capitalize() if stats2["transition_type"] != "None" else "Not found")

        col2a, col2b = st.columns(2)
        col2a.metric("Word Count", stats2["word_count"])
        col2b.metric("Dependent", "✅ Yes" if stats2["is_dependent"] else "❌ No")

        st.markdown("**🔦 Highlighted Claim**")
        st.markdown(highlighted2, unsafe_allow_html=True)



