import asyncio
from unittest.mock import patch

from skaha.utils.threaded import get_event_loop


def test_get_event_loop_existing():
    """Test getting an existing event loop."""
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Call the get_event_loop function
    retrieved_loop = get_event_loop()

    # Assertions
    assert (
        retrieved_loop is loop
    )  # The retrieved loop should be the same as the created loop


def test_get_event_loop_new():
    """Test creating a new event loop when none exists."""
    # Patch asyncio.get_event_loop to raise a RuntimeError
    with patch("asyncio.get_event_loop", side_effect=RuntimeError):
        # Call the get_event_loop function
        retrieved_loop = get_event_loop()

        # Assertions
        assert isinstance(
            retrieved_loop, asyncio.AbstractEventLoop
        )  # Should return a new event loop
        assert (
            retrieved_loop.is_running() is False
        )  # The new loop should not be running

    # Clean up by closing the loop
    retrieved_loop.close()
