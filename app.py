import streamlit as st
from fpdf import FPDF
from html2image import Html2Image

hti = Html2Image(output_path=".")

def generate_questions(name, position):
    return [
        f"احكي لنا عن خبرتك في مجال {position}.",
        "ما أصعب مشروع اشتغلت عليه وكيف تعاملت معه؟",
        "اذكر موقف واجهت فيه مشكلة كبيرة وكيف حلّيتها.",
        "ما المهارة اللي تحس أنك متميز فيها عن غيرك؟",
        "ما أكثر إنجاز تفتخر فيه؟",
        "كيف تتعامل مع الضغط في بيئة العمل؟"
    ]

def build_pdf(html_content):
    hti.screenshot(html_str=html_content, save_as="page.png")

    pdf = FPDF()
    pdf.add_page()
    pdf.image("page.png", x=0, y=0, w=210, h=297)  # A4
    return pdf.output(dest="S").encode("latin-1")

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
    st.write("## الأسئلة:")
    for q in st.session_state["questions"]:
        st.write(f"- {q}")

    if st.button("تحميل PDF"):
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    direction: rtl;
                    text-align: right;
                    font-family: Arial;
                    padding: 40px;
                }}
                h1 {{
                    color: #1E50A2;
                }}
                h2 {{
                    color: #444;
                }}
                .q {{
                    margin-bottom: 12px;
                    font-size: 20px;
                }}
            </style>
        </head>
        <body>
            <h1>أسئلة مقابلة – {name}</h1>
            <h2>المسمى الوظيفي: {position}</h2>
            <h2>الأسئلة:</h2>
            {''.join([f"<div class='q'>- {q}</div>" for q in st.session_state["questions"]])}
            <br><br>
            <div style="text-align:center; color:#777;">
                تم توليد هذا الملف بواسطة Hirix AI
            </div>
        </body>
        </html>
        """

        pdf_bytes = build_pdf(html)

        st.download_button(
            "تحميل PDF",
            pdf_bytes,
            file_name=f"{name}_interview.pdf",
            mime="application/pdf"
        )
