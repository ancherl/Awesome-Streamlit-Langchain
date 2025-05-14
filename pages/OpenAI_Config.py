import streamlit as st

import time

# 判断当前Session 是否存储了OPEN AI API Key
if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ''

if 'OPENAI_MODEL_NAME' not in st.session_state:
    st.session_state['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

if 'OPENAI_TEMPERATURE' not in st.session_state:
    st.session_state['OPENAI_TEMPERATURE'] = 0.97

if 'OPENAI_MAX_TOKENS' not in st.session_state:
     st.session_state['OPENAI_MAX_TOKENS'] = 2048

if 'OPENAI_TOP_P' not in st.session_state:
    st.session_state['OPENAI_TOP_P'] = 1.0

st.set_page_config(page_title='Open AI Settings', layout='wide')

# 设置Title
st.title('Open AI Settings')

# 插入一个文本
openai_api_key = st.text_input('API Key', value=st.session_state['OPENAI_API_KEY'], max_chars=None, key=None, type='password')

model_name_options = [
        'gpt-4.1',
        'gpt-4.1-mini',
        'gpt-4o',
        'gpt-4o-mini' 
]
openai_model_name = st.selectbox(
    'Open AI Model',
    model_name_options,
    index=model_name_options.index(st.session_state['OPENAI_MODEL_NAME'])
)

temperature = st.slider('Temperature',0.0, 2.0, value=st.session_state['OPENAI_TEMPERATURE'])

max_tokens = st.slider('Max tokens', 1, 4096, value=st.session_state['OPENAI_MAX_TOKENS'])

top_p = st.slider('Top P', 0.0, 1.0, value=st.session_state['OPENAI_TOP_P'])

# 插入提交按钮
submitted = st.button('Save')


if submitted:
    st.session_state['OPENAI_API_KEY'] = openai_api_key
    st.session_state['OPENAI_MODEL_NAME'] = openai_model_name
    st.session_state['OPENAI_TEMPERATURE'] = temperature
    st.session_state['OPENAI_MAX_TOKENS'] = max_tokens
    st.session_state['OPENAI_TOP_P'] = top_p

    # placeholder = st.empty()

    # placeholder.success('Saved successfully!')

    # time.sleep(3)

    # placeholder.empty()

    with st.empty():
        st.success('Saved successfully!')

        time.sleep(1)

        st.empty().empty()