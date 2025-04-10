import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# Google Gemini API Setup
GEMINI_API_KEY = "AIzaSyAgO5I6sN-2euuM_ZeomQG-ZVZ2EYqEOA4"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI Config
st.set_page_config(page_title="🧾 Invoice Reader & Budget Categorizer", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #3F51B5;
        text-shadow: 2px 2px 5px rgba(63, 81, 181, 0.4);
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #ccc;
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(to right, #3F51B5, #303F9F);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #303F9F, #1A237E);
    }
    .result-card {
        background: rgba(63, 81, 181, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(63, 81, 181, 0.2);
    }
    .success-banner {
        background: linear-gradient(to right, #1A237E, #0D133D);
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(63, 81, 181, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar instructions
st.sidebar.title("📘 How to Use")
st.sidebar.write("- Upload an invoice in PDF format.")
st.sidebar.write("- The AI will extract and analyze the invoice data.")
st.sidebar.write("- You'll receive a categorized budget breakdown and expense summary.")

st.markdown('<h1 class="main-title">📊 Invoice Reader & Budget Categorizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your invoice PDF to extract and analyze budget details</p>', unsafe_allow_html=True)

# Upload section
uploaded_file = st.file_uploader("📂 Upload Invoice PDF", type=["pdf"], help="Only PDF files supported")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_invoice_data(text):
    model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
    prompt = f"""
    Analyze the following invoice data and generate a budget categorization and summary:
    {text}
    
    Provide your analysis in this format:
    Invoice Summary
    - Invoice Date: [Date]
    - Invoice Number: [Number]
    - Vendor Name: [Name]
    - Total Amount: ₹[Total]
    
    Categorized Expenses:
    - [Category 1]: ₹[Amount]
    - [Category 2]: ₹[Amount]
    - ...

    Key Insights:
    - Largest Expense Category: [Category]
    - Budget Recommendation: [Suggestions for cost saving or optimization]

    If any values are missing, try to infer them or mention "Not Found".
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠ Unable to analyze the invoice."

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from invoice..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠ No text found. Ensure the invoice is not a scanned image.")
    else:
        progress_bar = st.progress(0)
        with st.spinner("🔍 Analyzing invoice data..."):
            insights = analyze_invoice_data(extracted_text)
        progress_bar.progress(100)

        st.subheader("🧾 Invoice Analysis Report")
        st.markdown(f'<div class="result-card"><b>📄 Invoice: {uploaded_file.name}</b></div>', unsafe_allow_html=True)
        st.write(insights)
        st.markdown('<div class="success-banner">🎯 Analysis Complete! Optimize your budget based on insights. 💡</div>', unsafe_allow_html=True)
        st.balloons()

    os.remove(file_path)