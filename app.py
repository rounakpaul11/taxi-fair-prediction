import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Taxi Fare Prediction", page_icon=":car:", layout="wide")

st.title(":car: Taxi Fare Prediction")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="ISO-8859-1")  # Modified to read directly from file uploader
else:
    os.chdir(r"C:\Users\ranja\Desktop\mlproject")
    df = pd.read_csv("cabdata.csv")

col1, col2 = st.columns((2))

# Visualization: Category-wise Fare Amount
with col1:
    st.subheader("Category-wise Fare Amount")
    category_fare_df = df.groupby("model")["fare_amount"].sum().reset_index()
    fig1 = px.bar(category_fare_df, x="model", y="fare_amount", title="Total Fare Amount by Category")
    st.plotly_chart(fig1, use_container_width=True)

# Visualization: Region-wise Fare Amount
with col2:
    st.subheader("Region-wise Fare Amount")
    region_fare_df = df.groupby("pickup_location_id")["fare_amount"].sum().reset_index()
    fig2 = px.pie(region_fare_df, values="fare_amount", names="pickup_location_id", title="Fare Amount by Region")
    st.plotly_chart(fig2, use_container_width=True)

# Visualization: Segment-wise Fare Amount
st.subheader("Segment-wise Fare Amount")
segment_fare_df = df.groupby("passenger_count")["fare_amount"].sum().reset_index()
fig3 = px.pie(segment_fare_df, values="fare_amount", names="passenger_count", title="Fare Amount by Passenger Count")
st.plotly_chart(fig3, use_container_width=True)

# Additional Visualizations:
# Visualization: Month-wise Fare Amount Summary
st.subheader("Month-wise Fare Amount Summary")
df["month_year"] = df["year"].astype(str) + '-' + df["month"].astype(str)
fare_month_summary = df.groupby("month_year")["fare_amount"].sum().reset_index()
fig4 = px.line(fare_month_summary, x="month_year", y="fare_amount", title="Fare Amount by Month", markers=True)
st.plotly_chart(fig4, use_container_width=True)

# Scatter Plot: Relationship between Fare Amount and Trip Duration
st.subheader("Relationship between Fare Amount and Trip Duration")
fig5 = px.scatter(df, x="trip_duration", y="fare_amount", title="Scatter Plot: Fare Amount vs. Trip Duration")
st.plotly_chart(fig5, use_container_width=True)

# Additional Visualizations:
# Visualization: Trip Distance vs. Fare Amount
st.subheader("Trip Distance vs. Fare Amount")
fig6 = px.scatter(df, x="trip_distance", y="fare_amount", title="Trip Distance vs. Fare Amount")
st.plotly_chart(fig6, use_container_width=True)

# Visualization: Rate Code vs. Fare Amount
st.subheader("Rate Code vs. Fare Amount")
fig7 = px.box(df, x="rate_code", y="fare_amount", title="Rate Code vs. Fare Amount")
st.plotly_chart(fig7, use_container_width=True)

# Visualization: Tip Amount Distribution
st.subheader("Tip Amount Distribution")
fig8 = px.histogram(df, x="tip_amount", title="Tip Amount Distribution")
st.plotly_chart(fig8, use_container_width=True)

# Visualization: Tolls Amount Distribution
st.subheader("Tolls Amount Distribution")
fig9 = px.histogram(df, x="tolls_amount", title="Tolls Amount Distribution")
st.plotly_chart(fig9, use_container_width=True)

# Visualization: Trip Duration Distribution
st.subheader("Trip Duration Distribution")
fig10 = px.histogram(df, x="trip_duration", title="Trip Duration Distribution")
st.plotly_chart(fig10, use_container_width=True)

# Sidebar with sliders
st.sidebar.title("Interactive Controls")
trip_distance_range = st.sidebar.slider("Select Trip Distance Range", min_value=int(df["trip_distance"].min()),
                                        max_value=int(df["trip_distance"].max()), value=(0, int(df["trip_distance"].max())))
fare_amount_range = st.sidebar.slider("Select Fare Amount Range", min_value=int(df["fare_amount"].min()),
                                      max_value=int(df["fare_amount"].max()), value=(0, int(df["fare_amount"].max())))
trip_duration_range = st.sidebar.slider("Select Trip Duration Range", min_value=int(df["trip_duration"].min()),
                                        max_value=int(df["trip_duration"].max()), value=(0, int(df["trip_duration"].max())))
year_range = st.sidebar.slider("Select Year Range", min_value=int(df["year"].min()),
                               max_value=int(df["year"].max()), value=(int(df["year"].min()), int(df["year"].max())))

# Filter data based on slider values
filtered_df = df[(df["trip_distance"] >= trip_distance_range[0]) & (df["trip_distance"] <= trip_distance_range[1]) &
                 (df["fare_amount"] >= fare_amount_range[0]) & (df["fare_amount"] <= fare_amount_range[1]) &
                 (df["trip_duration"] >= trip_duration_range[0]) & (df["trip_duration"] <= trip_duration_range[1]) &
                 (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Create interactive scatter plot with filtered data
st.subheader("Interactive Scatter Plot")
fig11 = px.scatter(filtered_df, x="trip_distance", y="fare_amount", title="Scatter Plot: Trip Distance vs Fare Amount",
                   labels={"trip_distance": "Trip Distance", "fare_amount": "Fare Amount"},
                   hover_name="model", hover_data=["rate_code", "trip_duration"])
st.plotly_chart(fig11)

# Create interactive histogram with filtered data
st.subheader("Interactive Histogram")
fig12 = px.histogram(filtered_df, x="trip_duration", title="Histogram: Trip Duration",
                     labels={"trip_duration": "Trip Duration"}, nbins=50)
st.plotly_chart(fig12)

# Create interactive line plot with filtered data
st.subheader("Interactive Line Plot")
fig13 = px.line(filtered_df, x="year", y="total_amount", title="Line Plot: Total Amount Over the Years",
                labels={"year": "Year", "total_amount": "Total Amount"})
st.plotly_chart(fig13)

# Create interactive bar chart with filtered data
st.subheader("Interactive Bar Chart")
fig14 = px.bar(filtered_df, x="day_of_week", y="fare_amount", title="Bar Chart: Fare Amount by Day of Week",
               labels={"day_of_week": "Day of Week", "fare_amount": "Fare Amount"})
st.plotly_chart(fig14)
