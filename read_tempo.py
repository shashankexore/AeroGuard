import xarray as xr
import pandas as pd
import numpy as np

def read_tempo_granule(path,varname="NO2"):
    ds=xr.open_dataset(path,mask_and_scale=True)
    if varname not in ds.variables:
        varname=list(ds.data_vars)[0]
    da=ds[varname]
    lat=ds['lat'].values if 'lat' in ds else ds['Latitude'].values
    lon=ds['lon'].values if 'lon' in ds else ds['Longitude'].values
    arr=da.values
    mask=np.isfinite(arr)
    lats=np.repeat(lat.reshape(-1,1),arr.shape[1],axis=1)
    lons=np.repeat(lon.reshape(1,-1),arr.shape[0],axis=0)
    flat={'lat':lats[mask].flatten(),'lon':lons[mask].flatten(),'value':arr[mask].flatten()}
    df=pd.DataFrame(flat)
    return df

if __name__=="__main__":
    print(read_tempo_granule("sample_tempo.nc").head())
