import dask.array as da

def advanced_compute(array, chunks=None, verbose=True):
    """
    An advanced version of Dask's compute function.
    Adds additional metadata about the computation process.

    Parameters:
        array (dask.array): The input Dask array.
        chunks (tuple): Chunk size for the Dask array (optional).
        verbose (bool): Whether to print metadata.

    Returns:
        dict: A dictionary containing the computed result and metadata.
    """
    if chunks:
        array = array.rechunk(chunks)
    
    result = array.compute()
    
    if verbose:
        print(f"Array Shape: {array.shape}")
        print(f"Chunks: {array.chunks}")
        print(f"Computed Result: {result}")
    
    return {
        "result": result,
        "metadata": {
            "shape": array.shape,
            "chunks": array.chunks
        }
    }