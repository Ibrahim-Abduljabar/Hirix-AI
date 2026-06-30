import streamlit as st
from weasyprint import HTML
from io import BytesIO

def generate_questions(name, position):
    return [
        f"احكي لنا عن خبرتك في مجال {position}.",
        "ما أصعب مشروع اشتغلت عليه وكيف تعاملت معه؟",
        "اذكر موقف واجهت فيه مشكلة كبيرة وكيف حلّيتها.",
        "ما المهارة اللي تحس أنك متميز فيها عن غيرك؟",
        "ما أكثر إنجاز تفتخر فيه؟",
        "كيف تتعامل مع الضغط في بيئة العمل؟"
    ]

def build_pdf(name, position, questions):
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                direction: rtl;
                text-align: right;
                padding: 40px;
            }}
            h1 {{
                color: #1E50A2;
            }}
            h2 {{
                color: #444;
            }}
            .question {{
                margin-bottom: 12px;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <h1>أسئلة مقابلة – {name}</h1>
        <h2>المسمى الوظيفي: {position}</h2>
        <h2>الأسئلة:</h2>
        {''.join([f"<div class='question'>- {q}</div>" for q in questions])}
        <br><br>
        <div style="text-align:center; color:#777;">
            تم توليد هذا الملف بواسطة Hirix AI
        </div>
    </body>
    </html>
    """

    pdf_bytes = HTML(string=html).write_pdf()
    return pdf_bytes

st.title("Hirix AI – مولّد أسئلة المقابلات")

name = st.text_input("اسم المرشح")
position = st.text_input("المسمى الوظيفي")
cv = st.file_uploader("ارفع الـ CV")

if st.button("توليد الأسئلة"):
    if name and position and cv:
        st.session_state["questions"] = generate_questions(name, position)
    else:
        st.warning("أكمل البيانات.")

if "questions" in st.session_state:
    st.write("### الأسئلة:")
    for q in st.session_state["questions"]:
        st.write(f"- {q}")

    if st.button("تحميل PDF"):
        pdf_bytes = build_pdf(name, position, st.session_state["questions"])
        st.download_button(
            "تحميل ملف PDF",
            pdf_bytes,
            file_name=f"{name}_interview.pdf",
            mime="application/pdf"
        )
