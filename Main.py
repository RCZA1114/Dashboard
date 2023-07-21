import streamlit as st
from datetime import timedelta
import plotly.express as px
from data import *
from streamlit_autorefresh import st_autorefresh
#from matplotlib import pyplot as plt


for k, v in st.session_state.items():
    st.session_state[k] = v

st.set_page_config(
    page_title="Dashboard",
    page_icon="👋",
)

st.title("Dashboard")

st.sidebar.success("Select a page above.")

st.header("Data for the Day!!!!")
@st.cache_data
def load_data():
    #data = pd.read_csv("2023.csv", usecols=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure', 'date', 'time'])
    data = pd.DataFrame(sql_query, columns=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure','last_update'])

    data['last_update'] = pd.to_datetime(data['last_update'])

    data.rename(
        columns={"tower_id": "Tower ID", "pm2_5": "PM2.5", "voc": "VOC", "humidity": "Humidity", "temp": "Temperature", "pressure": "Pressure", "last_update": "Date/Time"},
        inplace=True,
    )

    data = data.replace({'Tower ID': {'T0703220001': 'Tower 1', 'T0703220002': 'Tower 2', 'T0703220005': 'Tower 5',
                                      'T0703220006': 'Tower 6', 'T0703220008': 'Tower 8', 'T0703220009': 'Tower 9'}})

    return data


data = load_data()





date = st.date_input('Input Date')
time = st.time_input('Input Time')

# Filter data
datetime_str = str(date) + ' ' + str(time)
current_datetime = pd.to_datetime(datetime_str)

start_datetime = current_datetime - timedelta(hours=24)  # - 24 hours

fifteen = current_datetime - timedelta(minutes=15)

filtered_data = data[(data['Date/Time'] >= start_datetime) & (data['Date/Time'] <= current_datetime)]

filtered_data_2 = data[(data['Date/Time'] >= fifteen) & (data['Date/Time'] <= current_datetime)]



selected_measurement = st.selectbox('Select Measurement', ('PM2.5', 'Humidity', 'Temperature', 'VOC', 'Pressure'))

tower_ids = data['Tower ID'].unique()

selected_towers = st.multiselect('Select tower(s)', options = tower_ids, default=tower_ids)

#___________________________________________________________________________________________________
# Filter the data based on selected tower
filtered_data = filtered_data[filtered_data['Tower ID'].isin(selected_towers)]

fig = px.line(filtered_data, x='Date/Time', y=selected_measurement, title="Line Chart of the measurement for the last 24 hours", color='Tower ID',)

st.plotly_chart(fig, use_container_width=True)

#_______________________________________________________________________________________


# Bar Chart






filtered_data_2 = filtered_data_2[filtered_data_2['Tower ID'].isin(selected_towers)]
fig2 = px.bar(filtered_data_2, x='Date/Time', y=selected_measurement, title="Bar Chart of the measurement for the last 24 hours", color='Tower ID')

#fig3 = px.line(fifteen_min, x='datetime', y=selected_measurement, title="Title", color='tower_id')

st.plotly_chart(fig2, use_container_width=True)
#st.plotly_chart(fig3, use_container_width=True)

st.dataframe(filtered_data)


count = st_autorefresh(interval=300000, key="fizzbuzzcounter")