import streamlit as st
import pandas as pd
import joblib
from fetch_airnow import get_airnow_by_latlon
from fetch_weather import get_weather_open_meteo
from read_tempo import read_tempo_granule

st.set_page_config(layout="wide",page_title="Cleaner Safer Skies")

lat=st.sidebar.number_input("Latitude",value=40.7128)
lon=st.sidebar.number_input("Longitude",value=-74.0060)
if st.sidebar.button("Fetch & Predict"):
    airnow=get_airnow_by_latlon(lat,lon)
    weather=get_weather_open_meteo(lat,lon)
    tempo_file=st.sidebar.text_input("TEMPO granule path (optional)","")
    tempo_df=None
    if tempo_file:
        tempo_df=read_tempo_granule(tempo_file,varname="NO2")
    try:
        model=joblib.load("model.pkl")
        from preprocess import build_features
        X_train,X_test,y_train,y_test,merged=build_features(airnow,weather,tempo_df)
        pred=model.predict(merged.drop(columns=['AQI_value','Latitude','Longitude']))
        merged['predicted_AQI']=pred
        latest=merged.iloc[-1]
        st.metric("Predicted AQI (next hour)",int(latest['predicted_AQI']))
        if latest['predicted_AQI']>150:
            st.warning("Unhealthy air predicted — consider limiting outdoor exertion")
        st.dataframe(merged[['DateObserved','AQI_value','predicted_AQI']].tail(24))
        st.map(merged.rename(columns={"Latitude":"lat","Longitude":"lon"})[['lat','lon']].dropna())
    except Exception as e:
        st.error(str(e))
