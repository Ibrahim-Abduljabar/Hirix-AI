import streamlit as st

def generate_questions(name, position):
    return [
        f"احكي لنا عن خبرتك في مجال {position}.",
        "ما أصعب مشروع اشتغلت عليه وكيف تعاملت معه؟",
        "اذكر موقف واجهت فيه مشكلة كبيرة وكيف حلّيتها.",
        "ما المهارة اللي تحس أنك متميز فيها عن غيرك؟",
        "ما أكثر إنجاز تفتخر فيه؟",
        "كيف تتعامل مع الضغط في بيئة العمل؟"
    ]

st.set_page_config(page_title="Hirix AI")

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

    st.write("---")
    st.write("### نسخة PDF جاهزة للطباعة")

    html = f"""
    <div style='direction:rtl; text-align:right; font-family:Arial; padding:40px;'>
        <h1 style='color:#1E50A2;'>أسئلة مقابلة – {name}</h1>
        <h2 style='color:#444;'>المسمى الوظيفي: {position}</h2>
        <h2>الأسئلة:</h2>
        {''.join([f"<p style='font-size:20px;'>- {q}</p>" for q in st.session_state["questions"]])}
        <br><br>
        <div style='text-align:center; color:#777;'>تم توليد هذا الملف بواسطة Hirix AI</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    st.info("لطباعة الملف كـ PDF: اضغط Ctrl+P ثم اختر حفظ كـ PDF.")
