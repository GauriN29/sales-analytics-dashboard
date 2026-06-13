import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("superstore.csv",encoding="latin1")

st.title("📊 Superstore Sales Analytics Dashboard")
st.markdown("Analyze sales, profit, customers, and product performance across regions and categories.")

#Preprocessing
df['Order Date'] = pd.to_datetime(df['Order Date'])

# def find_year(order_date):
#     yr = str(order_date).split('-')[0]
#     return yr
# df['Year'] = df['Order Date'].apply(find_year)
df['Year'] = df['Order Date'].dt.year.astype(str)
df['Month'] = df['Order Date'].dt.month


#filters
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Select Year",["All"]+list(df['Year'].unique()))
region = st.sidebar.selectbox("Select Region",["All"]+list(df['Region'].unique()))
category = st.sidebar.selectbox("Select Category",["All"]+list(df['Category'].unique()))

filtered_df = df.copy()

if year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == year]

if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]

if category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category]


#Kpi Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")

with col2:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")

with col3:
    st.metric("Total Orders",filtered_df['Order ID'].nunique())

with col4:
    st.metric("Total Customers",filtered_df['Customer ID'].nunique())

#charts
#yearly sales
st.subheader("📈 Yearly Sales Trend")
yearly_sales = filtered_df.groupby('Year')['Sales'].sum()
st.bar_chart(yearly_sales)

#monthly sales
st.subheader("📅 Monthly Sales Trend")
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().sort_index()
st.line_chart(monthly_sales)

#Top Sub Category
st.subheader("🏆 Top 10 Sub-Categories by Sales")
Top_Sub_category = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
st.bar_chart(Top_Sub_category,horizontal=True)

#Category Sales
st.subheader("Sales by Category")
category_sales = filtered_df.groupby('Category')['Sales'].sum()
fig,ax = plt.subplots(figsize=(6,6))
ax.pie(category_sales,labels=category_sales.index,
    autopct='%1.1f%%')

ax.set_title('Sales by Category')
st.pyplot(fig)

#Insight selection
high_sales = filtered_df.groupby('Category')['Sales'].sum().idxmax()
high_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
loss_state = filtered_df.groupby('State')['Profit'].sum().sort_values(ascending=True).idxmin()


st.subheader("📌 Key Insights")

st.success(f"• Highest Sales Category: {high_sales}")
st.success(f"• Best Performing Region: {high_region}")
st.success(f"• Highest Loss State: {loss_state}")


csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


st.markdown("---")
st.caption("Built with Python, Pandas, Streamlit and Matplotlib")