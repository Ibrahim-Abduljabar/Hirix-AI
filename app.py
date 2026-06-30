import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO

pdfmetrics.registerFont(TTFont("Arabic", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

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

def build_pdf(name, position, questions):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Arabic", 18)
    pdf.drawString(50, 800, f"أسئلة مقابلة – {name}")

    pdf.setFont("Arabic", 14)
    pdf.drawString(50, 770, f"المسمى الوظيفي: {position}")

    pdf.setFont("Arabic", 16)
    pdf.drawString(50, 740, "الأسئلة:")

    y = 710
    pdf.setFont("Arabic", 14)
    for q in questions:
        pdf.drawString(50, y, f"- {q}")
        y -= 25

    pdf.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

st.title("Hirix AI – مولّد أسئلة المقابلات")

name = st.text_input("اسم المرشح")
position = st.text_input("المسمى الوظيفي")
cv_file = st.file_uploader("ارفع الـ CV")

if st.button("توليد الأسئلة"):
    if name and position and cv_file:
        cv_text = "تم رفع السيرة الذاتية"
        st.session_state["questions"] = generate_questions(name, position, cv_text)
    else:
        st.warning("أكمل البيانات قبل توليد الأسئلة.")

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
