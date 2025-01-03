import pandas as pd

def get_file_type(file):
    
    if file.name.endswith(".csv"):
        return "csv"
    elif file.name.endswith(".xlsx"):
        return "xlsx"
    elif file.name.endswith(".xls"):
        return 'xls'
    
def processing_amazon_sellerboard(amz_df, amz_listing_df, date = False):

    amz_listing_df = amz_listing_df[['ASIN', 'PRODUCT', 'NAME', 'SKU', 'BRAND', 'PRODUCTO']]
    amz_listing_df = amz_listing_df.rename(columns = {'PRODUCTO': 'Type of product', 'BRAND': 'Brand'})

    if date:
        amz_df = amz_df[['FECHA', 'Product', 'ASIN', 'SKU', 'Units', 'Sales', 'Ads']]
    else:
        amz_df = amz_df[['Product', 'ASIN', 'SKU', 'Units', 'Sales', 'Ads']]

    amz_df['Ads'] = amz_df['Ads'].abs()

    amz_listing_merge = amz_listing_df[['SKU', 'Brand', 'Type of product']]
    amz_df = pd.merge(amz_df, amz_listing_merge, on = 'SKU', how = 'left').drop_duplicates()

    na_mask = amz_df['Brand'].isna() | amz_df['Type of product'].isna()

    if date:
        amz_na_df = amz_df[na_mask][['FECHA', 'Product', 'ASIN', 'SKU', 'Units', 'Sales', 'Ads']]
        amz_grouped_df = amz_df.groupby(['FECHA', 'Brand', 'Type of product'])[['Ads', 'Units', 'Sales']].sum()
    else:
        amz_na_df = amz_df[na_mask][['Product', 'ASIN', 'SKU', 'Units', 'Sales', 'Ads']]
        amz_grouped_df = amz_df.groupby(['Brand', 'Type of product'])[['Ads', 'Units', 'Sales']].sum()

    return amz_grouped_df, amz_na_df

def processing_amazon_sellercentral(amz_df, amz_listing_df, date = False):

    amz_listing_df = amz_listing_df[['ASIN', 'PRODUCT', 'NAME', 'SKU', 'BRAND', 'PRODUCTO']]
    amz_listing_df = amz_listing_df.rename(columns = {'PRODUCTO': 'Type of product', 'BRAND': 'Brand'})

    if date:
        amz_df = amz_df[['FECHA', 'ASIN (parent)', 'ASIN (child)', 'Título', 'SKU', 'Sesiones: total', 'Visitas: total']]
    else:
        amz_df = amz_df[['ASIN (parent)', 'ASIN (child)', 'Título', 'SKU', 'Sesiones: total', 'Visitas: total']]

    try:
        amz_df['Sesiones: total'] = amz_df['Sesiones: total'].str.replace(',', '').astype(int)
    except:
        pass

    try:
        amz_df['Visitas: total'] = amz_df['Visitas: total'].str.replace(',', '').astype(int)
    except:
        pass

    amz_listing_merge = amz_listing_df[['SKU', 'Brand', 'Type of product']]
    amz_df = pd.merge(amz_df, amz_listing_merge, on = 'SKU', how = 'left').drop_duplicates()

    na_mask = amz_df['Brand'].isna() | amz_df['Type of product'].isna()

    if date:
        amz_na_df = amz_df[na_mask][['FECHA', 'ASIN (parent)', 'ASIN (child)', 'Título', 'SKU', 'Sesiones: total', 'Visitas: total']]
        amz_grouped_df = amz_df.groupby(['FECHA', 'Brand', 'Type of product'])[['Sesiones: total', 'Visitas: total']].sum()
    else:
        amz_na_df = amz_df[na_mask][['ASIN (parent)', 'ASIN (child)', 'Título', 'SKU', 'Sesiones: total', 'Visitas: total']]
        amz_grouped_df = amz_df.groupby(['Brand', 'Type of product'])[['Sesiones: total', 'Visitas: total']].sum()

    return amz_grouped_df, amz_na_df
