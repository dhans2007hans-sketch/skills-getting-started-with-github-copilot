"""Pytest fixtures for FastAPI backend tests."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def temp_excel_path():
    """Create a temporary Excel workbook for test isolation."""
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        temp_path = Path(tmp.name)

    app_module.create_workbook(temp_path, app_module.INITIAL_ACTIVITIES)
    yield temp_path

    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def app_module_with_temp_data(temp_excel_path, monkeypatch):
    """Patch the app to use a temporary Excel file and reload activities."""
    monkeypatch.setattr(app_module, "DATA_FILE", temp_excel_path)
    app_module.activities = app_module.load_data_from_excel(temp_excel_path)
    yield app_module


@pytest.fixture
def client(app_module_with_temp_data):
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app_module_with_temp_data.app)
