
from data import *
import streamlit as st
import datetime
import plotly.express as px
from datetime import timedelta

def start(year, month, day):
    if "start" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.start = datetime.date(year, month, day)


def end(year, month, day):
    if "end" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.end = datetime.date(year, month, day)

st.header("Data for the Week")

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

    data = data.replace({'Tower ID': {'T0703220001': 'Tower 1', 'T0703220002': 'Tower 2', 'T0703220005': 'Tower 5',
                                      'T0703220006': 'Tower 6', 'T0703220008': 'Tower 8', 'T0703220009': 'Tower 9'}})

    return data


data = load_data()


#datetime_str = str(data['date']) + ' ' + str(data['time'])
#end_datetime = pd.to_datetime(datetime_str)

#start_datetime = end_datetime - timedelta(days=7)  # - 24 hours

tower_ids = data['Tower ID'].unique()

selected_measurement = st.selectbox('Select Measurement', ('PM2.5', 'Humidity', 'Temperature', 'VOC', 'Pressure'), key="var")

selected_tower = st.selectbox('Which Tower would you want to select?', tower_ids, key="tower")


filtered_data = data[(data['Tower ID'] == selected_tower)]

#filtered_data

end_date = st.date_input('Select date(s) (End Date)',  key="end")

start_datetime = end_date - timedelta(days=7)

start_date = st.date_input('Select date(s) (Start Date)', on_change = start(start_datetime.year, start_datetime.month, start_datetime.day), key="start")

#end_date = st.date_input('Select date(s)', on_change = end(end_datetime.year, end_datetime.month, end_datetime.day), key="end")



filter = filtered_data[(filtered_data['date'] >= start_date) & (filtered_data['date'] <= end_date)]

filtered_data = filtered_data[(filtered_data['date'] >= start_date) & (filtered_data['date'] <= end_date)]

filtered_data = filtered_data.groupby(["date", "Hour"])[selected_measurement].mean().reset_index()


fig = px.line(filtered_data, x='Hour', y=selected_measurement, title="Line Chart of Data for the Past Week", color='date')

st.plotly_chart(fig, use_container_width=True)