import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://s3-pipeline-andresmpaws.s3.amazonaws.com/2023-citibike-tripdata.zip'

    dtype_mapping = {
        'ride_id': str,
        'rideable_type': str,
        'start_station_name': str,
        'start_station_id': str,
        'end_station_name': str,
        'end_station_id': str,
        'start_lat': float,
        'start_lng': float,
        'end_lat': float,
        'end_lng': float,
        'member_casual': str
    }
    parse_dates = ['started_at','ended_at']
    return pd.read_csv(url, sep = ",", compression = "zip", dtype=dtype_mapping, parse_dates=parse_dates)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

