import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import seaborn as sns
import matplotlib.pyplot as plt

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

# Interactive Controls
st.sidebar.title("Interactive Controls")

# Dropdown for selecting model
model_choice = st.sidebar.selectbox("Select Model", df["model"].unique())

# Slider for Trip Distance
trip_distance_range = st.sidebar.slider("Select Trip Distance Range", float(df["trip_distance"].min()),
                                        float(df["trip_distance"].max()), (float(df["trip_distance"].min()), float(df["trip_distance"].max())))

# Slider for Fare Amount
fare_amount_range = st.sidebar.slider("Select Fare Amount Range", float(df["fare_amount"].min()),
                                      float(df["fare_amount"].max()), (float(df["fare_amount"].min()), float(df["fare_amount"].max())))

# Slider for Trip Duration
trip_duration_range = st.sidebar.slider("Select Trip Duration Range", float(df["trip_duration"].min()),
                                        float(df["trip_duration"].max()), (float(df["trip_duration"].min()), float(df["trip_duration"].max())))

# Filter data based on interactive controls
filtered_df = df[df["model"] == model_choice]

trip_distance_min, trip_distance_max = trip_distance_range
fare_amount_min, fare_amount_max = fare_amount_range
trip_duration_min, trip_duration_max = trip_duration_range

filtered_df = filtered_df[
    (filtered_df["trip_distance"] >= trip_distance_min) & (filtered_df["trip_distance"] <= trip_distance_max) &
    (filtered_df["fare_amount"] >= fare_amount_min) & (filtered_df["fare_amount"] <= fare_amount_max) &
    (filtered_df["trip_duration"] >= trip_duration_min) & (filtered_df["trip_duration"] <= trip_duration_max)
]

col1, col2 = st.columns((2))

# Visualization: Category-wise Fare Amount
with col1:
    st.subheader("Category-wise Fare Amount")
    category_fare_df = filtered_df.groupby("model")["fare_amount"].sum().reset_index()
    fig1 = px.bar(category_fare_df, x="model", y="fare_amount", title="Total Fare Amount by Category")
    st.plotly_chart(fig1, use_container_width=True)

# # Heatmap of Fare Amount by Hour and Day of Week
# st.subheader("Heatmap of Fare Amount by Hour and Day of Week")
# pivot_df = filtered_df.pivot_table(values="fare_amount", index="hour_of_day", columns="day_of_week", aggfunc="mean")
# plt.figure(figsize=(12, 8))
# sns.heatmap(pivot_df, cmap="YlGnBu", annot=True, fmt=".2f")
# st.pyplot(plt)

# Box Plot of Fare Amount by Model
st.subheader("Box Plot of Fare Amount by Model")
plt.figure(figsize=(12, 8))
sns.boxplot(x="model", y="fare_amount", data=filtered_df)
st.pyplot(plt)

# Pie Chart of Passenger Count Distribution
st.subheader("Pie Chart of Passenger Count Distribution")
passenger_count_df = filtered_df["passenger_count"].value_counts().reset_index()
passenger_count_df.columns = ["Passenger Count", "Count"]
fig3 = px.pie(passenger_count_df, values="Count", names="Passenger Count", title="Passenger Count Distribution")
st.plotly_chart(fig3)

# Pairplot for Correlation Analysis
st.subheader("Pairplot for Correlation Analysis")
st.set_option('deprecation.showPyplotGlobalUse', False)
sns.pairplot(filtered_df[["trip_distance", "fare_amount", "trip_duration", "passenger_count"]])
st.pyplot()

# Line Plot of Fare Amount Over Time
st.subheader("Line Plot of Fare Amount Over Time")
fare_over_time_df = filtered_df.groupby("year")["fare_amount"].mean().reset_index()
fig4 = px.line(fare_over_time_df, x="year", y="fare_amount", title="Average Fare Amount Over Time")
st.plotly_chart(fig4)

# Interactive scatter plot with filtered data
st.subheader("Interactive Scatter Plot")
fig11 = px.scatter(filtered_df, x="trip_distance", y="fare_amount", title="Scatter Plot: Trip Distance vs Fare Amount",
                   labels={"trip_distance": "Trip Distance", "fare_amount": "Fare Amount"},
                   hover_name="model", hover_data=["rate_code", "trip_duration"])
st.plotly_chart(fig11)

# Interactive histogram with filtered data
st.subheader("Interactive Histogram")
fig12 = px.histogram(filtered_df, x="trip_duration", title="Histogram: Trip Duration",
                     labels={"trip_duration": "Trip Duration"}, nbins=50)
st.plotly_chart(fig12)

# Interactive bar chart with filtered data
st.subheader("Interactive Bar Chart")
fig14 = px.bar(filtered_df, x="day_of_week", y="fare_amount", title="Bar Chart: Fare Amount by Day of Week",
               labels={"day_of_week": "Day of Week", "fare_amount": "Fare Amount"})
st.plotly_chart(fig14)

# Visualization: Region-wise Fare Amount
st.subheader("Region-wise Fare Amount")
region_fare_df = filtered_df.groupby("Delhi_location_id")["fare_amount"].sum().reset_index()
fig2 = px.pie(region_fare_df, values="fare_amount", names="Delhi_location_id", title="Fare Amount by Region")
st.plotly_chart(fig2)

# Visualization: Region-wise Fare Amount
with col2:
    st.subheader("Region-wise Fare Amount")
    region_fare_df = filtered_df.groupby("Delhi_location_id")["fare_amount"].sum().reset_index()
    fig2 = px.pie(region_fare_df, values="fare_amount", names="Delhi_location_id", title="Fare Amount by Region")
    st.plotly_chart(fig2, use_container_width=True)

# Interactive scatter plot with filtered data
st.subheader("Interactive Scatter Plot")
fig11 = px.scatter(filtered_df, x="trip_distance", y="fare_amount", title="Scatter Plot: Trip Distance vs Fare Amount",
                   labels={"trip_distance": "Trip Distance", "fare_amount": "Fare Amount"},
                   hover_name="model", hover_data=["rate_code", "trip_duration"])
st.plotly_chart(fig11)

# Interactive histogram with filtered data
st.subheader("Interactive Histogram")
fig12 = px.histogram(filtered_df, x="trip_duration", title="Histogram: Trip Duration",
                     labels={"trip_duration": "Trip Duration"}, nbins=50)
st.plotly_chart(fig12)

# Interactive line plot with filtered data
st.subheader("Interactive Line Plot")
fig13 = px.line(filtered_df, x="year", y="fare_amount", title="Line Plot: Fare Amount Over the Years",
                labels={"year": "Year", "fare_amount": "Fare Amount"})
st.plotly_chart(fig13)

# Interactive bar chart with filtered data
st.subheader("Interactive Bar Chart")
fig14 = px.bar(filtered_df, x="day_of_week", y="fare_amount", title="Bar Chart: Fare Amount by Day of Week",
               labels={"day_of_week": "Day of Week", "fare_amount": "Fare Amount"})
st.plotly_chart(fig14)
