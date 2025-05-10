import streamlit as st

from langchain_openai import ChatOpenAI

from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Initialize that ChatOpenAI object
chat = None

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ''
else:
    chat = ChatOpenAI(
        openai_api_key = st.session_state['OPENAI_API_KEY'],
        model="gpt-4o-mini"
    )

if 'PINECONE_API_KEY' not in st.session_state:
    st.session_state['PINECONE_API_KEY'] = ''

if 'PINECONE_ENVIRONMENT' not in st.session_state:
    st.session_state['PINECONE_ENVIRONMENT'] = ''

st.set_page_config(page_title='Homepage', layout='wide')

st.title('Welcome to Kris\'s AI Chatbox 😝')

# 插入俩个container 分别显示Open AI 和 Pinecone 的 信息

# with st.container():
#     st.header('OpenAI Settings')
#     st.markdown(f"""
#         | OpenAI API Key |
#         | ----------  |
#         | {st.session_state['OPENAI_API_KEY']}   |
#     """)

# with st.container():
#     st.header('Pinecone Settings')
#     st.markdown(f"""
#         | Pinecone API Key |
#         | ----------  |
#         | {st.session_state['PINECONE_API_KEY']}   |
#     """)

if chat:
    with st.container():
        st.header('Chat with GPT')
        prompt = st.text_input('Prompt', value='', max_chars=None, key=None, type='default')
        asked = st.button('Ask')
        if asked:
            ai_message = chat([HumanMessage(content=prompt)])
            st.write(ai_message.content)
else:
    with st.container():
        st.warning('Please config your OpenAI API Key before using GPT function!')