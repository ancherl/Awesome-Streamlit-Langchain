import streamlit as st

import matplotlib.pyplot as plt

from langchain_openai import ChatOpenAI

from langchain.schema import AIMessage, HumanMessage, SystemMessage

import pandas as pd
# import langchain pandas analysis engine
from langchain_experimental.agents import create_pandas_dataframe_agent

import time

import re

def stream_data(ai_message):
    for word in ai_message.split(' '):
        yield word + ' '
        time.sleep(0.02)

# define matplotlib figure process function
# def process_matplotlib_code(agent_output):
#     # 1. 剥离 净化代码块
#     code = agent_output
#     code_block = code

#     # 2. 正则表达式处理
#     matches = re.findall("```(?:python)?\n?([^`]+)```", code, flags=re.DOTALL)

#     if matches:
#         code_block = matches[0]
    
#     # 3. 去掉plt.show() 代码
#     code_block = "\n".join(l for l in code_block.splitlines() if "plt.show()" not in l)
#     with st.expander("LLM 自动生成的代码，可手动查看/复制", expanded=False):
#         st.code(code_block, language="python")
#     # 4. 本地变量空间执行代码并输出图片
#     fig = plt.figure()
#     try:
#         exec(code_block, {"df": df, "plt": plt})
#         st.pyplot(fig)
#     except Exception as e:
#         st.error(f'代码执行错误: {e}')
#     finally:
#         plt.close(fig)

# Config Page Information
st.set_page_config(page_title='Homepage', layout='wide')

st.title('Welcome to Kris\'s AI Chatbox 😝')


# Initialize that ChatOpenAI object
chat = None

if 'OPENAI_MODEL_NAME' not in st.session_state:
    st.session_state['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'
if 'OPENAI_TEMPERATURE' not in st.session_state:
    st.session_state['OPENAI_TEMPERATURE'] = 0.97
if 'ATTACHED_FILES' not in st.session_state:
    st.session_state['ATTACHED_FILES'] = []

if 'OPENAI_API_KEY' not in st.session_state:
    st.warning('Please config your OpenAI API Key before using GPT function!',icon='⚠')
    st.stop()
    

# 初始化chat instance
try:
    chat = ChatOpenAI(
        openai_api_key = st.session_state['OPENAI_API_KEY'],
        model=st.session_state['OPENAI_MODEL_NAME'],
        temperature=st.session_state['OPENAI_TEMPERATURE'],
    )
except Exception as e:
    st.error('OpenAI chat instance initialize exception, make sure you have provided valid open api key!')
    st.stop()

# if 'PINECONE_API_KEY' not in st.session_state:
#     st.session_state['PINECONE_API_KEY'] = ''

# if 'PINECONE_ENVIRONMENT' not in st.session_state:#     st.session_state['PINECONE_ENVIRONMENT'] = ''
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
if chat is not None:
    # Insert a chatbox input at the bottom
    prompt = st.chat_input('Type something you want to ask...', accept_file=True, file_type=['xlsx'])
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
        if prompt and (prompt['files'] or st.session_state['ATTACHED_FILES']):
            st.session_state['messages'].append(HumanMessage(content=prompt.text))
            with st.chat_message('user'):
                st.markdown(prompt.text)
            # Need to analyze the uploaded file
            # 1. Store the uploaded file in session state
            if prompt['files']:
                st.session_state['ATTACHED_FILES'] = prompt['files']
            # 2. Read the file and convert it to a pandas dataframe
            dfs = pd.read_excel(st.session_state['ATTACHED_FILES'][0], sheet_name=None)
            # 3. Initialize agent instance
            agent = create_pandas_dataframe_agent(
                    chat, 
                    [v for k, v in dfs.items()], 
                    verbose=True,
                    # handle_parsing_errors=True,
                    allow_dangerous_code=True,
            )

            # user_prompt = f"""
            #                     You are a data analysis assistant, please help me to analyze the data and provide the result.\n
            #                     If user ask you to generate a visualization chart against the data, please only output runnable matplotlib drawing code directly. Do not explain for this generated Matplotlib code, do not use plt.show(), I will use streamlit to render this chart. The data is in DataFrame list {[v for k, v in dfs.items()]}\n
            #                     Task: {prompt.text}\n
            # """
            with st.spinner('Querying...', show_time=True):
                # querying resources using LLMs
                ai_message = agent.invoke(prompt.text)
                # ai_message = agent.invoke(user_prompt)
                # st.write(ai_message)
            with st.spinner('Generating...'):
                st.session_state['messages'].append(AIMessage(content=ai_message['output']))
                # st.write(ai_message.content)
                with st.chat_message('assistant'):
                    # st.markdown(ai_message.content)
                    st.write_stream(stream_data(ai_message=ai_message['output']))
            st.stop()
        elif prompt and prompt.text:
            # Insert user input into session state
            st.session_state['messages'].append(HumanMessage(content=prompt.text))
            with st.chat_message('user'):
                st.markdown(prompt.text)
            
            with st.spinner('Querying...', show_time=True):
                # querying resources using LLMs
                ai_message = chat([HumanMessage(content=prompt.text)])
            with st.spinner('Generating...'):
                # Insert AI output into session state
                st.session_state['messages'].append(ai_message)
                # st.write(ai_message.content)
                with st.chat_message('assistant'):
                    # st.markdown(ai_message.content)
                    st.write_stream(stream_data(ai_message=ai_message.content))
            st.stop()
else:
    with st.container():
        st.warning('Please config your OpenAI API Key before using GPT function!',icon='⚠')