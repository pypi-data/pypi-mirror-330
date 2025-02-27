import pytest

from skaha.utils.threaded import scale


@pytest.mark.asyncio
async def test_scale():
    # Define a simple function for testing
    def square(x: int) -> int:
        return x**2

    # Define the arguments for the function
    arguments = [{"x": i} for i in range(10)]

    # Call the scale function
    results = await scale(square, arguments)

    # Check the results
    for i in range(10):
        assert results[i] == i**2


@pytest.mark.asyncio
async def test_scale_with_error():
    # Define a simple function for testing that raises an error for a specific input
    def square_or_error(x: int) -> int:
        if x == 5:
            raise ValueError("An error occurred!")
        return x**2

    # Define the arguments for the function
    arguments = [{"x": i} for i in range(10)]

    # Call the scale function
    results = await scale(square_or_error, arguments)

    # Check the results
    for i in range(10):
        if i == 5:
            assert isinstance(results[i], ValueError)
        else:
            assert results[i] == i**2
