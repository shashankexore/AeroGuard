import requests
import pandas as pd

def get_weather_open_meteo(lat,lon,hours=48):
    url="https://api.open-meteo.com/v1/forecast"
    params={"latitude":lat,"longitude":lon,"hourly":"temperature_2m,relativehumidity_2m,windspeed_10m,precipitation","forecast_days":2,"timezone":"UTC"}
    r=requests.get(url,params=params,timeout=20)
    r.raise_for_status()
    j=r.json()
    df=pd.DataFrame(j['hourly'])
    df['time']=pd.to_datetime(df['time'])
    return df
