import streamlit as st
import datetime
import requests

st.set_page_config(
            page_title="Taxi NY", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

'''
# Taxi NY

## Select the parameters of the ride

'''
columns = st.columns(3)
columns[0].write("When's your go")
d = columns[1].date_input("Days", datetime.date(2022, 5, 27))
t = columns[2].time_input('Hours', datetime.time(8, 45))
pickup_datetime = str(d) + ' ' + str(t)


columns = st.columns(3)
columns[0].write('Insert a pickup')
pickup_longitude = columns[1].number_input('Longitude',min_value=39.0, max_value=42.0, value=40.7614327)
pickup_latitude = columns[2].number_input('Latitude',min_value=-76.0, max_value=-70.0, value=-73.9798156)

columns = st.columns(3)
columns[0].write('Insert a dropoff')
dropoff_longitude = columns[1].number_input('Longitude',min_value=39.0, max_value=42.0, value=40.6331166)
dropoff_latitude = columns[2].number_input('Latitude',min_value=-76.0, max_value=-70.0, value=-73.8874078)

passenger_count = st.slider("Select a passenger count",1, 8, 2)

url = 'https://taxifare.lewagon.ai/predict'

params = dict(
  pickup_datetime=pickup_datetime,
  pickup_longitude = pickup_longitude,
  pickup_latitude = pickup_latitude,
  dropoff_longitude = dropoff_longitude,
  dropoff_latitude = dropoff_latitude,
  passenger_count = passenger_count
)

# retrieve the response
response = requests.get(
    url,
    params=params
)

if response.status_code == 200:
    f=round(response.json().get("fare", "no fare"),2)
    st.success(
        'Fare :'+ f' **{f}** '+ '$'
    )
else:
    st.error('Sorry ...')

'''
### Thank's for your visit
'''
