"""Pytest configuration and fixtures for test suite."""

import os
import pytest


def pytest_configure(config):
    """Register custom pytest marks."""
    config.addinivalue_line(
        "markers", "gui: mark test as a GUI test that requires display"
    )


@pytest.fixture(autouse=True)
def skip_gui_tests_in_headless(request):
    """Automatically skip GUI tests when DISPLAY is not available."""
    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    if not has_display:
        test_path = str(request.fspath)
        if "test_gui" in test_path:
            pytest.skip("GUI tests skipped in headless environment (no DISPLAY)")
