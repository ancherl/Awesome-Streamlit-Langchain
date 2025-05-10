import streamlit as st

# 判断当前Session 是否存储了OPEN AI API Key
if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ''

st.set_page_config(page_title='Open AI Settings', layout='wide')

# 设置Title
st.title('Open AI Settings')

# 插入一个文本
openai_api_key = st.text_input('API Key', value=st.session_state['OPENAI_API_KEY'], max_chars=None, key=None, type='password')

# 插入提交按钮
submitted = st.button('Save')

if submitted:
    st.session_state['OPENAI_API_KEY'] = openai_api_key