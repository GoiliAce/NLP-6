import streamlit as st
import pickle
from utils import ProcessText, get_dict_trans, is_url, is_vnexpress_url
import requests
from bs4 import BeautifulSoup
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    lb = pickle.load(f)
    

def crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if is_vnexpress_url(url):
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('p', class_='description')
        for i in description.find_all(class_='location-stamp'):
            i.decompose()
        description = description.text
        content = '\n'.join([p.text for p in soup.find_all('p', class_='Normal')])
        content = description+'\n'+content
        return content
    else:
        return soup.text
def user_input():
    text = st.text_area("Nhập vào văn bản của bạn, có thể dán vào link (ưu tiên VNExpress))")
    if is_url(text):
        text = crawler(text)
        
    st.write("Hoặc upload file txt")
    uploaded_file = st.file_uploader("Chọn file txt", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
    # url = st.text_input("Hoặc dán 1 link bài báo (ưu tiên VNExpress))")
    # text = crawler(url)
    return text


def predict(text, model):
    return model.predict(text)

def main():
    st.title("Dự đoán chủ đề của văn bản")
    doc = user_input()

    if st.button("Dự đoán") and doc:
        st.write("Dự đoán chủ đề của văn bản là:")
        pred = predict(doc, model)
        pred = lb.inverse_transform(pred)
        dict_trans = get_dict_trans()
        res = [dict_trans[x] for x in pred.tolist()]
        st.write(res[0])
if __name__ == '__main__':
    main()