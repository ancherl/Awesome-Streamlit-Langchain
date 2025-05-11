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

# 显示历史对话记录，需要通过session state 进行存储
if 'messages' not in st.session_state:
    st.session_state['messages'] = []


# 根据user input 调用LLM分析
if chat:
    # Insert a chatbox input at the bottom
    prompt = st.chat_input('Type something you want to ask...')
    with st.container():
        st.header('Chat with GPT')
        # 遍历session state 对话历史
        for message in st.session_state['messages']:
            if isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message('assistant'):
                    st.markdown(message.content)
        
        # asked = st.button('Ask')
        if prompt:
            # Insert user input into session state
            st.session_state['messages'].append(HumanMessage(content=prompt))
            with st.chat_message('user'):
                st.markdown(prompt)
            ai_message = chat([HumanMessage(content=prompt)])
            # Insert AI output into session state
            st.session_state['messages'].append(ai_message)
            # st.write(ai_message.content)
            with st.chat_message('assistant'):
                st.markdown(ai_message.content)
else:
    with st.container():
        st.warning('Please config your OpenAI API Key before using GPT function!')