from fpdf import FPDF
import streamlit as st
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

def build_pdf(candidate):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(30, 80, 200)
    pdf.cell(0, 10, f"أسئلة مقابلة – {candidate['name']}", ln=True)

    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"المسمى الوظيفي: {candidate['position']}", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "الأسئلة المولّدة:", ln=True)

    pdf.set_font("Arial", "", 13)
    pdf.set_text_color(40, 40, 40)

    for q in candidate["questions"]:
        pdf.multi_cell(0, 8, f"- {q}")
        pdf.ln(1)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "تم توليد هذا الملف بواسطة Hirix AI – HR Interview Generator", ln=True, align="C")

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes

st.title("Hirix AI – مولّد أسئلة المقابلات")

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
    st.subheader(f"المرشح رقم {idx + 1}")

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
                pdf_bytes = build_pdf(c)
                st.download_button(
                    "تحميل ملف PDF",
                    pdf_bytes,
                    file_name=f"{c['name']}_interview.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("لم يتم توليد أسئلة بعد.")
