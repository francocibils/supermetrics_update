import pandas as pd
import streamlit as st

from helper_functions import *

app_mode = st.sidebar.selectbox('Select source to upload', ['Amazon Sellerboard', 'Amazon Sellercentral'])

if app_mode == 'Amazon Sellerboard':
    st.title('Amazon Sellerboard')
    st.header('File upload')
    st.markdown('Upload file to obtain Ads, Units and Sales for each Brand and Type of product.')

    amz_file = st.file_uploader('Upload Amazon Sellerboard file', type = ['xlsx', 'xls', 'csv'])
    amz_listing = st.file_uploader('Upload Amazon listing file (optional)', type = ['xlsx'])

    if amz_file is not None:
        file_type = get_file_type(amz_file)
        
        if file_type == 'csv':
            amz_df = pd.read_csv(amz_file)
        elif file_type == 'xlsx' or file_type == 'xls':
            amz_df = pd.read_excel(amz_file)
        
        st.success('Amazon Sellerboard file uploaded successfully.')

    if amz_listing is not None:
        amz_listing_df = pd.read_excel(amz_listing, engine = 'openpyxl')
        st.success('Amazon listing uploaded successfully.')
    else:
        amz_listing_df = pd.read_excel(r'.\Datasets\amazon_sku_listado.xlsx', engine = 'openpyxl')
        st.info('Default Amazon listing used.')

    if st.button('Process file'):
        if amz_file is None:
            raise ValueError('Amazon Sellerboard file has not been provided, please provide one.')

        amz_grouped_df, amz_na_df = processing_amazon_sellerboard(amz_df = amz_df, amz_listing_df = amz_listing_df)

        st.header('Processed data')
        st.success('Amazon file has been processed successfully.')
        
        if amz_na_df.shape[0] > 0:
            st.warning('There were SKU not listed in the Amazon listing. Please see below.')
            st.subheader('Data grouped by Brand and Type of product')
            st.dataframe(amz_grouped_df)
            st.subheader('Items not found in SKU listing')
            st.dataframe(amz_na_df)
        else:
            st.subheader('Data grouped by Brand and Type of product')
            st.info('All items were listed in the Amazon listing.')
            st.dataframe(amz_grouped_df)

if app_mode == 'Amazon Sellercentral':
    st.title('Amazon Sellercentral')
    st.header('File upload')
    st.markdown('Upload file to obtain Sessions and Page Views for each Brand and Type of product.')

    amz_file = st.file_uploader('Upload Amazon Sellercentral file', type = ['xlsx', 'xls', 'csv'])
    amz_listing = st.file_uploader('Upload Amazon listing file (optional)', type = ['xlsx'])

    if amz_file is not None:
        file_type = get_file_type(amz_file)
        
        if file_type == 'csv':
            amz_df = pd.read_csv(amz_file)
        elif file_type == 'xlsx' or file_type == 'xls':
            amz_df = pd.read_excel(amz_file)
        
        st.success('Amazon Sellercentral file uploaded successfully.')

    if amz_listing is not None:
        amz_listing_df = pd.read_excel(amz_listing, engine = 'openpyxl')
        st.success('Amazon listing uploaded successfully.')
    else:
        amz_listing_df = pd.read_excel(r'.\Datasets\amazon_sku_listado.xlsx', engine = 'openpyxl')
        st.info('Default Amazon listing used.')

    if st.button('Process file'):
        if amz_file is None:
            raise ValueError('Amazon Sellercentral file has not been provided, please provide one.')

        amz_grouped_df, amz_na_df = processing_amazon_sellercentral(amz_df = amz_df, amz_listing_df = amz_listing_df)

        st.header('Processed data')
        st.success('Amazon file has been processed successfully.')
        
        if amz_na_df.shape[0] > 0:
            st.warning('There were SKU not listed in the Amazon listing. Please see below.')
            st.subheader('Data grouped by Brand and Type of product')
            st.dataframe(amz_grouped_df)
            st.subheader('Items not found in SKU listing')
            st.dataframe(amz_na_df)
        else:
            st.subheader('Data grouped by Brand and Type of product')
            st.info('All items were listed in the Amazon listing.')
            st.dataframe(amz_grouped_df)