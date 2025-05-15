import streamlit as st

import pandas as pd

import openpyxl

import tabulate

# Define custom functions start
def delete_selected_files():
    st.session_state['UPLOADED_FILES_DATAFRAME_KEY'] += 1
    for record in st.session_state['UPLOADED_FILES']:
        if record['fileIndex'] in selected_file_indexs:
            # st.write(record)
            # st.session_state['UPLOADED_FILES'].remove(record)
            record['fileStatus'] = 'Deleted'
            # st.session_state['UPLOADED_FILES'].remove(record)

    # st.session_state['UPLOADED_FILES'] = [record for record in st.session_state['UPLOADED_FILES'] if record['fileIndex'] not in selected_file_indexs]
def active_selected_files():
    st.session_state['UPLOADED_FILES_DATAFRAME_KEY'] += 1
    for record in st.session_state['UPLOADED_FILES']:
        if record['fileIndex'] in selected_file_indexs:
            # st.write(record)
            # st.session_state['UPLOADED_FILES'].remove(record)
            record['fileStatus'] = 'Active'
# Define  custom functions end

st.set_page_config('RAG Config', layout='wide')

st.title('RAG Config')

if 'UPLOADED_FILES' not in st.session_state:
    st.session_state['UPLOADED_FILES'] = []

if 'UPLOADED_FILES_DATAFRAME_KEY' not in st.session_state:
    st.session_state['UPLOADED_FILES_DATAFRAME_KEY'] = 0



# Insert a Uploader component
uploader_files = st.file_uploader(
    'Files Uploader',
    ['xlsx','csv'],
    accept_multiple_files=True,
)

# st.write(uploader_files)
# Store temporary uploader files object
tab_datapreview, tab_uploadedfiles = st.tabs(['Data Preview','Uploaded Files'])

# Obtain File Names list
filenames_list = [record['fileName'] for record in st.session_state['UPLOADED_FILES']]
# sheetnames_list = [record['sheetName'] for record in st.session_state['UPLOADED_FILES']]

with tab_datapreview:
    if uploader_files is not None and len(uploader_files) > 0:
        # st.subheader('Preview')
        # st.write(filenames_list)

        # 遍历所有的文件
        for file_object in uploader_files:
            if file_object.name.endswith('csv'):
                df = pd.read_csv(file_object)
                if file_object.name not in filenames_list:
                    st.session_state['UPLOADED_FILES'].append({'fileName': file_object.name,'fileContent':df, 'sheetName': None,'fileIndex': len(st.session_state['UPLOADED_FILES'])+1,'fileStatus': 'Active'})
                st.write(df)
            elif file_object.name.endswith('xlsx'):
                # sheet_name = None 表示读取所有sheet 数据
                dfs = pd.read_excel(file_object, sheet_name=None)
                # 遍历所有的sheet 数据
                for k, v in dfs.items():
                    if file_object.name not in filenames_list:
                        st.session_state['UPLOADED_FILES'].append({'fileName': file_object.name,'fileContent':v, 'sheetName': k, 'fileIndex': len(st.session_state['UPLOADED_FILES'])+1,'fileStatus': 'Active'})
                    st.write(k)
                    st.write(v)
            else:
                st.error('Current file type is not supported!')

        # st.dataframe(df)
        # st.write(df)

with tab_uploadedfiles:
    if st.session_state['UPLOADED_FILES']:
        df_uploaded_files = pd.DataFrame(st.session_state['UPLOADED_FILES'])

        # st.write(df_uploaded_files)
        # st.subheader('Uploaded Files')
        # filter_condition = df_uploaded_files['filestatus'] == 'Active'

        df_select_event = st.dataframe(
            df_uploaded_files.loc[:,['fileName','sheetName','fileContent','fileStatus']],
            on_select='rerun',
            selection_mode=['multi-row'],
            hide_index=True,
            key=st.session_state['UPLOADED_FILES_DATAFRAME_KEY']
        )

        # st.write(df_select_event.selection)

        if len(df_select_event.selection.rows) > 0:
            # st.write(df_select_event.selection.rows)
            selected_file_indexs = [df_uploaded_files.at[i,'fileIndex'] for i in df_select_event.selection.rows]
            # st.write(selected_file_indexs)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button('Delete Selected Files', key='delete_files', icon=':material/delete:', on_click=delete_selected_files)
            with col2:
                st.button('Active Selected Files', key='active_files', icon=':material/check:', on_click=active_selected_files)
