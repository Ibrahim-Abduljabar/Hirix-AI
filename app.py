
import streamlit as st
from weasyprint import HTML
from io import BytesIO

def generate_questions(name, position, cv_text):
    base = [
        f"احكي لنا عن خبرتك في مجال {position}.",
        "ما أصعب مشروع اشتغلت عليه وكيف تعاملت معه؟",
        "اذكر موقف واجهت فيه مشكلة كبيرة وكيف حلّيتها.",
        "ما المهارة اللي تحس أنك متميز فيها عن غيرك؟",
        "ما أكثر إنجاز تفتخر فيه؟",
        "كيف تتعامل مع الضغط في بيئة العمل؟"
    ]

    extra = []
    if "Python" in cv_text:
        extra.append("ذكرت أنك تجيد Python، ما آخر مشروع استخدمتها فيه؟")
    if "Team" in cv_text or "فريق" in cv_text:
        extra.append("احكي لنا عن تجربة عملك ضمن فريق.")

    return base + extra

def build_html(c):
    return f"""
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}

            body {{
                font-family: "Segoe UI", Tahoma, sans-serif;
                background: #ffffff;
                color: #222;
            }}

            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}

            .title {{
                font-size: 28px;
                font-weight: 700;
                color: #1a73e8;
                margin-bottom: 5px;
            }}

            .subtitle {{
                font-size: 16px;
                color: #555;
            }}

            .section {{
                margin-top: 30px;
                padding: 20px;
                border-radius: 12px;
                background: #f7f9fc;
                border: 1px solid #e3e8ef;
            }}

            .section h2 {{
                font-size: 20px;
                margin-bottom: 10px;
                color: #333;
            }}

            ul {{
                margin-top: 15px;
                padding-left: 20px;
            }}

            li {{
                margin-bottom: 12px;
                line-height: 1.6;
                font-size: 15px;
            }}

            .footer {{
                margin-top: 40px;
                text-align: center;
                font-size: 13px;
                color: #777;
            }}
        </style>
    </head>

    <body>
        <div class="header">
            <div class="title">أسئلة مقابلة – {c['name']}</div>
            <div class="subtitle">المسمى الوظيفي: {c['position']}</div>
        </div>

        <div class="section">
            <h2>الأسئلة المولّدة</h2>
            <ul>
                {''.join(f'<li>{q}</li>' for q in c['questions'])}
            </ul>
        </div>

        <div class="footer">
            تم توليد هذا الملف بواسطة Hirix AI – HR Interview Generator
        </div>
    </body>
    </html>
    """

def html_to_pdf(html):
    pdf_bytes = HTML(string=html).write_pdf()
    return pdf_bytes

st.set_page_config(page_title="Hirix HR Interview", layout="wide")
st.title("Hirix AI – مولّد أسئلة المقابلات من الـ CV")

if "candidates" not in st.session_state:
    st.session_state["candidates"] = []

if st.button("➕ إضافة مرشح جديد"):
    st.session_state["candidates"].append({
        "name": "",
        "position": "",
        "cv_text": "",
        "questions": []
    })

for idx, c in enumerate(st.session_state["candidates"]):
    st.markdown("---")
    st.markdown(f"### المرشح رقم {idx + 1}")

    col1, col2 = st.columns(2)

    with col1:
        c["name"] = st.text_input("اسم المرشح", key=f"name_{idx}")
        c["position"] = st.text_input("المسمى الوظيفي", key=f"position_{idx}")
        cv_file = st.file_uploader("ارفع الـ CV", key=f"cv_{idx}")

        if cv_file:
            if cv_file.type == "application/pdf":
                c["cv_text"] = "نص مستخرج من PDF (ركّب pdfplumber لو تبغى)"
            else:
                c["cv_text"] = cv_file.read().decode("utf-8")

        if st.button("توليد أسئلة", key=f"gen_{idx}"):
            if c["name"] and c["position"] and c["cv_text"]:
                c["questions"] = generate_questions(c["name"], c["position"], c["cv_text"])
            else:
                st.warning("أكمل البيانات قبل توليد الأسئلة.")

    with col2:
        st.markdown("#### الأسئلة")
        if c["questions"]:
            for q in c["questions"]:
                st.markdown(f"- {q}")

            if st.button("📄 تحميل PDF", key=f"pdf_{idx}"):
                html = build_html(c)
                pdf = html_to_pdf(html)
                st.download_button(
                    "تحميل ملف PDF",
                    pdf,
                    file_name=f"{c['name']}_interview.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("لم يتم توليد أسئلة بعد.")
