import dask.array as da
from advdask.core import advanced_compute

def test_advanced_compute():
    # Create a simple Dask array
    x = da.arange(10, chunks=5)

    # Perform computation
    result = advanced_compute(x, verbose=False)

    # Validate results
    assert result["result"].tolist() == list(range(10)), "Test failed: Incorrect computation result"
    print("Test passed!")
if __name__ == "__main__":
    test_advanced_compute()