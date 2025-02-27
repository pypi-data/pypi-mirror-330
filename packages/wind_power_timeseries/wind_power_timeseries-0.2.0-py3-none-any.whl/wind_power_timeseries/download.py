import pathlib

from metocean_api import ts

from .const import Products


def retrieve_nora3(locations, time_start, time_end, use_cache=True, data_path=None, reload=False, save_csv=True):
    """Download or reload NORA3 wind speed and wind direction data. Save to csv files

    Arguments:
    - ocations : pandas dataframe with lat,lon columns
    - time_start, time_end : str, time period to download data for
    - use_cache : boolean, whether to use local cache
    - data_path : pathlib.Path, location of where to save downloaded data (csv files)
    - reload : boolean - If True, reload data from local CSV files
    - save_csv : boolean - If True, save data to CSV files

    Returns:
    - dictionary of metocean_api.ts.TimeSeries objects
    """
    all_ts = retrieve_wind_data(
        locations,
        time_start,
        time_end,
        source="NORA3",
        variables=None,
        use_cache=use_cache,
        data_path=data_path,
        reload=reload,
    )
    return all_ts


def retrieve_era5(locations, time_start, time_end, use_cache=True, data_path=None, reload=False, save_csv=True):
    """Download or reload ERA5 wind speed and wind direction data. Save to csv files

    Arguments:
    - locations : pandas dataframe with lat,lon columns
    - time_start, time_end : str, time period to download data for
    - use_cache : boolean, whether to use local cache
    - data_path : pathlib.Path, location of where to save downloaded data (csv files)
    - reload : boolean - If True, reload data from local CSV files
    - save_csv : boolean - If True, save data to CSV files

    Returns:
    - dictionary of metocean_api.ts.TimeSeries objects.
        Columns are wind speed in u and v directions at 10 and 100 m (u100,v100,u10,v10)
    """
    era5_variables = [
        "100m_u_component_of_wind",
        "100m_v_component_of_wind",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
    ]
    all_ts = retrieve_wind_data(
        locations,
        time_start,
        time_end,
        source="ERA5",
        variables=era5_variables,
        use_cache=use_cache,
        data_path=data_path,
        reload=reload,
    )
    return all_ts


def retrieve_wind_data(
    locations,
    time_start,
    time_end,
    source,
    variables=None,
    use_cache=True,
    data_path=None,
    reload=False,
    save_csv=True,
):
    """Retrieve wind speed and wind direction data. Save to csv files

    Arguments:
    - locations : pandas dataframe with lat,lon columns
    - time_start, time_end : str, time period to download data for
    - source : str, which data source ("ERA5" or "NORA3")
    - variables : list of str, which variables to retreive from the dataset. None=get all
    - use_cache : boolean, whether to use local cache
    - data_path : pathlib.Path, location of where to save downloaded data (csv files)
    - reload : boolean - If True, reload data from local CSV files
    - save_csv : boolean - If True, save data to CSV files

    Returns:
    - dictionary of metocean_api.ts.TimeSeries objects.
        Columns are wind speed in u and v directions at 10 and 100 m (u100,v100,u10,v10)
    """
    if source == "ERA5":
        product = Products.ERA5
    elif source == "NORA3":
        product = Products.NORA3
    else:
        raise ValueError(f"Unknown source {source}.")

    if data_path is not None:
        # create folder if it does not exist:
        data_path.mkdir(parents=True, exist_ok=True)
    all_ts = dict()
    for i, row in locations.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        ts_data = ts.TimeSeries(
            lon=lon,
            lat=lat,
            start_time=time_start,
            end_time=time_end,
            product=product,
            variable=variables,
            datafile=None,
        )
        if data_path is not None:
            ts_data.datafile = data_path / ts_data.datafile
        if reload:
            ts_data.load_data(local_file=ts_data.datafile)
        else:
            ts_data.import_data(save_csv=save_csv, save_nc=False, use_cache=use_cache)
        all_ts[i] = ts_data
    return all_ts
