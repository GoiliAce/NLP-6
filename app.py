import streamlit as st
import pickle
from utils import ProcessText, get_dict_trans, is_url, crawler

# Load model and label encoder
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    lb = pickle.load(f)

def user_input():
    st.subheader("Nhập văn bản của bạn")
    text = st.text_area("Nhập văn bản của bạn, có thể dán vào link (ưu tiên VNExpress)")

    if is_url(text):
        with st.spinner("Đang tải dữ liệu từ URL..."):
            text = crawler(text)

    st.subheader("Hoặc upload file txt")
    uploaded_file = st.file_uploader("Chọn file txt", type="txt")

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

    return text

def predict(text, model):
    return model.predict(text)

def main():
    st.title("Dự đoán chủ đề của văn bản")
    doc = user_input()
    button = st.button("Dự đoán")
    if button and doc:
        st.subheader("Kết quả dự đoán:")
        pred = predict(doc, model)
        pred = lb.inverse_transform(pred)
        dict_trans = get_dict_trans()
        res = [dict_trans[x] for x in pred.tolist()]
        st.write(res[0])
        doc = ''

if __name__ == '__main__':
    main()
