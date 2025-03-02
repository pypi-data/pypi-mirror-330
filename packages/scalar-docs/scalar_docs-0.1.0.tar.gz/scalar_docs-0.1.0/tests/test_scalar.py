import json
import os
import pytest
from unittest.mock import patch, mock_open
from scalar_py import (
    Options,
    Spec,
    api_reference_html,
    safe_json_configuration,
    ensure_file_url,
    fetch_content_from_url,
    read_file_from_url,
    specContent_handler
)

def test_safe_json_configuration():
    options = Options(spec=Spec(url="https://example.com/spec.json"))
    json_output = safe_json_configuration(options)
    assert "&quot;" in json_output 

def test_specContent_handler():
    spec_dict = {"openapi": "3.0.0", "info": {"title": "Test API"}}
    assert json.loads(specContent_handler(spec_dict)) == spec_dict
    
    spec_str = '{"openapi": "3.0.0"}'
    assert specContent_handler(spec_str) == spec_str
    
    assert json.loads(specContent_handler(lambda: spec_dict)) == spec_dict

def test_ensure_file_url():
    file_path = "test.yaml"
    expected_url = f"file://{os.path.abspath(file_path)}"
    assert ensure_file_url(file_path) == expected_url

@patch("requests.get")
def test_fetch_content_from_url(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "mock content"
    content = fetch_content_from_url("https://example.com")
    assert content == "mock content"

@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_read_file_from_url(mock_file):
    file_url = "file:///tmp/test.json"
    with patch("os.path.exists", return_value=True):
        content = read_file_from_url(file_url)
    assert content == '{"key": "value"}'

def test_api_reference_html():
    options = Options(spec=Spec(content='{"openapi": "3.0.0"}'))
    html = api_reference_html(options)
    assert "<html>" in html
    assert "application/json" in html

if __name__ == "__main__":
    pytest.main()
