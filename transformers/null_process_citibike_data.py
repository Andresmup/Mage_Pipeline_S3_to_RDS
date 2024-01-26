if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    null_counts = data.isnull().sum()
    print(f"Preprocessing rows with null values:\n{null_counts}")

    return data.dropna()



@test
def test_output(output, *args) -> None:
    assert output.isnull().any().any() == False, 'There are rows with null values in the dataset'