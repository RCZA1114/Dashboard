from data import *
import streamlit as st

import plotly.express as px



st.header("Data for the past Months")

st.sidebar.success("Select a page above.")



@st.cache_data
def load_data():
    #data = pd.read_csv("2023.csv", usecols=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure', 'date', 'time'])
    data = pd.DataFrame(sql_query, columns=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure','last_update'])

    data['last_update'] = pd.to_datetime(data['last_update'])

    data.rename(
        columns={"tower_id": "Tower ID", "pm2_5": "PM2.5", "voc": "VOC", "humidity": "Humidity", "temp": "Temperature", "pressure": "Pressure", "last_update": "Date/Time"},
        inplace=True,
    )

    data['date'] = data['Date/Time'].dt.date

    data['Hour'] = data['Date/Time'].dt.hour
    data['Month'] = data['Date/Time'].dt.month

    data = data.replace({'Tower ID': {'T0703220001': 'Tower 1', 'T0703220002': 'Tower 2', 'T0703220005': 'Tower 5',
                                      'T0703220006': 'Tower 6', 'T0703220008': 'Tower 8', 'T0703220009': 'Tower 9'}})

    return data


data = load_data()



selected_measurement = st.selectbox('Select Measurement', ('PM2.5', 'Humidity', 'Temperature', 'VOC', 'Pressure'),  key="var")

tower_ids = data['Tower ID'].unique()  # First I need to filter based on the Towers.

selected_tower = st.selectbox('Which Tower would you want to select?', tower_ids, key="tower")

filtered_data = data[(data['Tower ID'] == selected_tower)]

#selected_month = st.slider('Select month(s)', value=(1, 13), max_value=13, min_value=1, key="slider")
selected_month = st.slider('Select month(s)', value=(1, 13), max_value=13, min_value=1, key="slider")

#filtered_data = filtered_data[filtered_data['Month'].isin(range(selected_month[0], selected_month[1], + 1))]
filtered_data = filtered_data[filtered_data['Month'].isin(range(selected_month[0], selected_month[1]))]

#filtered_data["Hour"] == filtered_data["datetime"].dt.hour

filtered_data = filtered_data.groupby(["Month", "Hour"])[selected_measurement].mean().reset_index()

fig = px.line(filtered_data, x='Hour', y=selected_measurement, title="Monthly Average Chart", color='Month')

# fig = filtered_data.groupby('Hour')[selected_measurement].plot(legend=True)

st.plotly_chart(fig, use_container_width=True)