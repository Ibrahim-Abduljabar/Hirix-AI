
import streamlit as st
from io import BytesIO
from xhtml2pdf import pisa
import requests
import json


def generate_questions(candidate_name: str, position: str, cv_text: str):

    base_questions = [
        f"احكي لنا عن خبرتك في مجال {position}.",
        "ما أصعب مشروع اشتغلت عليه وكيف تعاملت معه؟",
        "اذكر موقف واجهت فيه مشكلة كبيرة وكيف حلّيتها.",
        "ما المهارة اللي تحس أنك متميز فيها عن غيرك؟",
        "ما أكثر إنجاز تفتخر فيه في مسيرتك المهنية؟",
        "كيف تتعامل مع الضغط في بيئة العمل؟",
    ]

    extra = []
    if "Python" in cv_text:
        extra.append("ذكرت أنك تجيد Python، ما آخر مشروع استخدمتها فيه؟")
    if "Team" in cv_text or "فريق" in cv_text:
        extra.append("احكي لنا عن تجربة عملك ضمن فريق، وما دورك بالتحديد؟")

    return base_questions + extra

def build_html(candidate):
    return f"""
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
            body {{
                font-family: Tahoma, Arial, sans-serif;
                background: #f5f5f5;
                padding: 40px;
            }}
            .card {{
                background: #ffffff;
                padding: 30px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.12);
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                margin-bottom: 5px;
                font-size: 26px;
                color: #222;
            }}
            h2 {{
                margin-top: 0;
                font-size: 18px;
                color: #666;
            }}
            .meta {{
                margin-top: 8px;
                font-size: 13px;
                color: #999;
            }}
            ul {{
                margin-top: 20px;
                padding-left: 22px;
            }}
            li {{
                margin-bottom: 10px;
                line-height: 1.6;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>أسئلة مقابلة – {candidate['name']}</h1>
            <h2>المسمى الوظيفي: {candidate['position']}</h2>
            <div class="meta">تم توليد الأسئلة بواسطة Hirix AI – HR Interview Generator</div>
            <ul>
                {''.join(f'<li>{q}</li>' for q in candidate['questions'])}
            </ul>
        </div>
    </body>
    </html>
    """

def html_to_pdf_bytes(html_content: str) -> bytes:
    result = BytesIO()
    pisa.CreatePDF(html_content, dest=result)
    return result.getvalue()

st.set_page_config(page_title="Hirix HR Interview", layout="wide")
st.title("Hirix AI – مولّد أسئلة المقابلات من الـ CV للـ HR")

if "candidates" not in st.session_state:
    st.session_state["candidates"] = []

if st.button("➕ إضافة مرشح جديد"):
    st.session_state["candidates"].append({
        "name": "",
        "position": "",
        "cv_text": "",
        "questions": []
    })

for idx, candidate in enumerate(st.session_state["candidates"]):
    st.markdown(f"---")
    st.markdown(f"### المرشح رقم {idx + 1}")

    col1, col2 = st.columns(2)

    with col1:
        candidate["name"] = st.text_input("اسم المرشح", key=f"name_{idx}")
        candidate["position"] = st.text_input("المسمى الوظيفي", key=f"position_{idx}")
        cv_file = st.file_uploader("ارفع الـ CV (PDF أو ملف نصي)", key=f"cv_{idx}")

        if cv_file is not None:
            if cv_file.type == "application/pdf":
                candidate["cv_text"] = "نص مستخرج من PDF (ركّب pdfplumber هنا)"
            else:
                candidate["cv_text"] = cv_file.read().decode("utf-8")

        if st.button("توليد أسئلة المقابلة", key=f"generate_{idx}"):
            if candidate["name"] and candidate["position"] and candidate["cv_text"]:
                candidate["questions"] = generate_questions(
                    candidate["name"],
                    candidate["position"],
                    candidate["cv_text"]
                )
            else:
                st.warning("أكمل الاسم، المسمى الوظيفي، والـ CV قبل توليد الأسئلة.")

    with col2:
        st.markdown("#### الأسئلة المولّدة")
        if candidate["questions"]:
            for q in candidate["questions"]:
                st.markdown(f"- {q}")

            if st.button("📄 تحميل الأسئلة كـ PDF", key=f"pdf_{idx}"):
                html = build_html(candidate)
                pdf_bytes = html_to_pdf_bytes(html)
                st.download_button(
                    label="تحميل ملف PDF",
                    data=pdf_bytes,
                    file_name=f"{candidate['name']}_interview_questions.pdf",
                    mime="application/pdf",
                    key=f"download_{idx}"
                )
        else:
            st.info("لم يتم توليد أسئلة بعد لهذا المرشح.")

