import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def build_features(airnow_df, weather_df, tempo_df=None, window_hours=24):
    if airnow_df.empty:
        return None, None, None, None, pd.DataFrame()
    airnow_df = airnow_df.sort_values("DateObserved")
    pm25 = airnow_df[['DateObserved', 'pm2_5', 'Latitude', 'Longitude']].rename(columns={'pm2_5': 'AQI_value'})
    pm25 = pm25.set_index('DateObserved').resample('1H').mean().fillna(method='ffill').reset_index()
    weather_df = weather_df.rename(columns={"time": "DateObserved"})
    weather_df['DateObserved'] = pd.to_datetime(weather_df['DateObserved'])
    pm25['DateObserved'] = pd.to_datetime(pm25['DateObserved'])
    merged = pd.merge_asof(pm25.sort_values('DateObserved'), weather_df.sort_values('DateObserved'), on='DateObserved', direction='nearest', tolerance=pd.Timedelta('1H'))
    if tempo_df is not None and not tempo_df.empty:
        try:
            tempo_agg = tempo_df.groupby([pd.cut(tempo_df['lat'], 10), pd.cut(tempo_df['lon'], 10)])['value'].mean().reset_index()
            merged['tempo_no2_mean'] = tempo_agg['value'].mean()
        except Exception:
            merged['tempo_no2_mean'] = np.nan
    merged = merged.dropna()
    if merged.empty:
        return None, None, None, None, merged
    X = merged.drop(columns=['AQI_value', 'Latitude', 'Longitude'])
    y = merged['AQI_value']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    return X_train, X_test, y_train, y_test, merged
