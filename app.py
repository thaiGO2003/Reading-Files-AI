import streamlit as st
import google.generativeai as genai
from docx import Document
import PyPDF2
import os

# Cấu hình Gemini API
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

# Hàm đọc file txt
def read_txt(file):
    return file.getvalue().decode('utf-8')

# Hàm đọc file docx
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs if para.text])

# Hàm đọc file pdf
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Hàm gọi Gemini API để trả lời câu hỏi
def ask_gemini(model, content, question):
    prompt = f"Nội dung tài liệu:\n{content}\n\nCâu hỏi: {question}"
    response = model.generate_content(prompt)
    return response.text

# Giao diện Streamlit
st.title("Ứng dụng đọc và phân tích tài liệu với Gemini")

# Nhập API key
api_key = st.text_input("Nhập Google API Key:", type="password")

if api_key:
    try:
        model = configure_gemini(api_key)
        
        # Tải file lên
        uploaded_file = st.file_uploader("Tải file lên (txt, docx, pdf)", type=['txt', 'docx', 'pdf'])
        
        if uploaded_file:
            # Đọc nội dung file
            file_extension = uploaded_file.name.split('.')[-1].lower()
            content = ""
            
            try:
                if file_extension == 'txt':
                    content = read_txt(uploaded_file)
                elif file_extension == 'docx':
                    content = read_docx(uploaded_file)
                elif file_extension == 'pdf':
                    content = read_pdf(uploaded_file)
                
                # Hiển thị nội dung file
                st.subheader("Nội dung tài liệu:")
                st.text_area("Nội dung", content, height=300)
                
                # Nhập câu hỏi
                question = st.text_input("Câu hỏi về nội dung tài liệu:")
                
                if question:
                    with st.spinner("Đang xử lý..."):
                        response = ask_gemini(model, content, question)
                        st.subheader("Trả lời từ Gemini:")
                        st.write(response)
            
            except Exception as e:
                st.error(f"Lỗi khi đọc file: {str(e)}")
                
    except Exception as e:
        st.error(f"Lỗi khi cấu hình Gemini API: {str(e)}")
else:
    st.warning("Vui lòng nhập API key để tiếp tục.")