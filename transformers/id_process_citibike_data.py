if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    data_filtered = data[~data['start_station_id'].astype(str).str.contains('\.') & ~data['end_station_id'].astype(str).str.contains('\.')]
    data = data_filtered.copy()
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
