import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load Data from CSV
url = 'https://raw.githubusercontent.com/Cidolf/Project_submission/main/dashboard/data_ecommerce.csv'
data_ecommerce_df = pd.read_csv(url)

# Data Preparation
order_by_month = data_ecommerce_df.groupby('purchase_month_year').order_id.nunique().reset_index()
order_by_month = order_by_month.sort_values('purchase_month_year')

revenue_by_month = data_ecommerce_df.groupby('purchase_month_year').price.sum().reset_index()
revenue_by_month = revenue_by_month.sort_values('purchase_month_year')

ecommerce_product = data_ecommerce_df.groupby(by='product_category_name').order_id.nunique().sort_values(ascending=False).reset_index().head(10)

ecommerce_city = data_ecommerce_df.groupby(by='customer_city').order_id.nunique().sort_values(ascending=False).reset_index().head(10)

# Streamlit App
st.title('Dashboard E-commerce 🛍️')
st.sidebar.title('Navigation')

# Sidebar Navigation
nav_selection = st.sidebar.radio('Go to', ('Order Stats', 'Revenue Stats', 'Product Stats', 'City Stats'))

# Main Content
if nav_selection == 'Order Stats':
    st.subheader('Total Orders per Month (2017-2018)')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(order_by_month['purchase_month_year'], order_by_month['order_id'], marker='o')
    ax.set_xlabel('Order Date', fontsize=17)
    ax.set_ylabel('Total Order', fontsize=17)
    ax.tick_params(axis='x', rotation=45, labelsize=15)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

elif nav_selection == 'Revenue Stats':
    st.subheader('Total Revenue per Month (2017-2018)')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(revenue_by_month['purchase_month_year'], revenue_by_month['price'], marker='o')
    ax.set_xlabel('Order Date', fontsize=20)
    ax.set_ylabel('Total Revenue', fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=15)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

elif nav_selection == 'Product Stats':
    st.subheader('Best & Worst Performing Product')
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="order_id", y="product_category_name", data=ecommerce_product.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis ='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

    sns.barplot(x="order_id", y="product_category_name", data=ecommerce_product.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

    st.pyplot(fig)

elif nav_selection == 'City Stats':
    st.subheader('Cities with The Most Orders')
    fig, ax = plt.subplots(figsize=(20, 10))
    top_color = '#72BCD4'
    default_color = '#D3D3D3'
    ax.barh(ecommerce_city['customer_city'], ecommerce_city['order_id'], color=[top_color if city == ecommerce_city['customer_city'].iloc[0] else default_color for city in ecommerce_city['customer_city']])
    ax.set_xlabel('Total Order', fontsize=20)
    ax.set_ylabel('City Name', fontsize=20)
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
