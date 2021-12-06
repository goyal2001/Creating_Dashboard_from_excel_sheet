import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Importing the dataset from disk
data = pd.read_csv(r"C:\Users\DELL\Downloads\Ecommerce.csv")

# https://www.webfx.com/tools/emoji-cheat-sheet/
# These are the configurations of the page
st.set_page_config(
    page_title="Dashboard",
    initial_sidebar_state="auto",
    page_icon=":money_with_wings:",
    layout="wide"
)

# Sidebar
# Heading of Side bar
st.sidebar.header("Options Bar")
# Analysis would be based on these variables
region = st.sidebar.multiselect(
    "Select the Region:",
    options=data["Region"].unique(),
    default=data["Region"].unique()
    # default="Yangon"
)
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=data["Gender"].unique(),
    default=data["Gender"].unique()
)
product_line = st.sidebar.multiselect(
    "Select the Type of Product:",
    options=data["Product_line"].unique(),
    default=data["Product_line"].unique()
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=data["Customer_type"].unique(),
    default=data["Customer_type"].unique()
)

# This is the data with accordance to the side bar
data_selection = data.query(
    "Region == @region & Gender == @gender & Product_line == @product_line & Customer_type == @customer_type"
)

# Main Page
# Title of the whole dashboard
st.title(":bar_chart: Product Purchase Dashboard")
st.markdown("##")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Above function is to get the request from specified url


# Animations
left_column, right_column = st.columns(2)
with left_column:
    dashboard1 = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
    st_lottie(dashboard1, key="Dashboard1", height=400)
with right_column:
    dashboard2 = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qpsnmykx.json")
    st_lottie(dashboard2, key="Dashboard2", height=400)
# st.dataframe(data_selection)
st.markdown("""---""")

# Some calculations
total_price = data_selection["Total"].sum()
average_rating = round(data_selection["Rating"].mean(),1)
star = ":star:" * int(round(average_rating, 0))
average_total = data_selection["Total"].mean()
total_tax = data_selection["Tax_5%"].sum()

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star}")
with right_column:
    st.subheader("Total Price(including TAX):")
    st.subheader(f"₹ {total_price:,}")
st.markdown("""---""")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total TAX paid:")
    st.subheader(f"₹ {total_tax:,}")
with right_column:
    st.subheader("Average Total Price:")
    st.subheader(f"₹ {average_total}")
st.markdown("""---""")

# Total by product line
product_line_total = (
    data_selection.groupby(by=["Product_line"]).sum()[["Total"]].sort_values(by="Total")
)
# Bar chart between product and its total price
product_total_bar = px.bar(
    product_line_total,
    y="Total",
    x=product_line_total.index,
    orientation="v",
    title="<b>Total by Product Line</b>",
    color_discrete_sequence=["cyan"] * len(product_line_total),
    template="plotly_dark"
)
product_total_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
data1 = data_selection["Gender"]
cou = {}
key = []
value = []
for i in data1:
    if i in cou and i in key:
        cou[i] += 1
    else:
        cou[i] = 1
        key.append(i)
for i in range(len(key)):
    value.append(cou[key[i]])
# pie chart of gender
fig_pie = px.pie(
    values=value,
    names=key,
    title="<b>Selected Gender</b>",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(product_total_bar, use_container_width=True)
right_column.plotly_chart(fig_pie, use_container_width=True)
st.markdown("##")

data2 = data_selection["Payment"]
di = {}
key1 = []
value1 = []
for i in data2:
    if i in di and i in key1:
        di[i] += 1
    else:
        di[i] = 1
        key1.append(i)
for i in range(len(key1)):
    value1.append(di[key1[i]])
# Pie chart for different payment methods
fig_pie2 = px.pie(
    values=value1,
    names=key1,
    title="<b>Payment types for selected Gender</b>",
    color_discrete_map="red"
)
# Average Rating by product line
product_line_Rating = (
    data_selection.groupby(by=["Product_line"]).mean()[["Rating"]].sort_values(by="Rating")
)
# Bar chart between rating and product
Product_Rating_bar = px.bar(
    product_line_Rating,
    y="Rating",
    x=product_line_Rating.index,
    orientation="v",
    title="<b>Rating by Product Line</b>",
    color_discrete_sequence=["cyan"] * len(product_line_Rating),
    template="plotly_dark"
)
Product_Rating_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pie2, use_container_width=True)
right_column.plotly_chart(Product_Rating_bar, use_container_width=True)

# Average Quantity by Product
data3 = data_selection.groupby(by=["Product_line"]).mean()[["Quantity"]].sort_values(by="Quantity")
# line chart between quantity and product line
fig_line = px.line(
    data3,
    x=data3.index,
    y="Quantity",
    orientation="v",
    width=1000,
    line_shape="spline",
    title="<b>Quantity by Product line</b>"
)
fig_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_line)
# Scatter plot between date and time
data4_sort_time = data_selection.sort_values(by='Time', ascending=True)
fig_scatter = px.scatter(
    data4_sort_time.sort_values(by='Date', ascending=True),
    x=data4_sort_time["Time"],
    y="Date",
    orientation="h",
    title="<b>Date vs Time</b>",
    width=1500,
    height=1000
)
fig_scatter.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)
st.markdown("##")
st.plotly_chart(fig_scatter)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
