"""
Utility functions for the Streamlit ML Platform Frontend
"""

import streamlit as st
import pandas as pd
import base64
import requests
from typing import Optional, Dict, Any


def display_base64_image(base64_data: str, title: str = "", caption: str = ""):
    """
    Display base64 encoded image in Streamlit

    Args:
        base64_data (str): Base64 encoded image data
        title (str): Title to display above the image
        caption (str): Caption to display below the image
    """
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(base64_data)

        if title:
            st.subheader(title)

        st.image(image_bytes, caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format

    Args:
        size_bytes (int): Size in bytes

    Returns:
        str: Formatted file size
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"


def validate_csv_file(file) -> tuple[bool, str]:
    """
    Validate uploaded CSV file

    Args:
        file: Streamlit uploaded file object

    Returns:
        tuple: (is_valid, error_message)
    """
    if file is None:
        return False, "No file uploaded"

    if not file.name.endswith(".csv"):
        return False, "File must be a CSV file"

    try:
        # Try to read the file to check if it's valid CSV
        file_content = file.read()
        file.seek(0)  # Reset file pointer

        # Check if file is empty
        if len(file_content) == 0:
            return False, "File is empty"

        # Try to parse as CSV
        df = pd.read_csv(file)

        # Check if DataFrame has data
        if df.empty:
            return False, "CSV file contains no data"

        # Check if DataFrame has columns
        if len(df.columns) == 0:
            return False, "CSV file contains no columns"

        return True, "File is valid"

    except Exception as e:
        return False, f"Error reading CSV file: {str(e)}"


def create_download_link(df: pd.DataFrame, filename: str, link_text: str) -> str:
    """
    Create a download link for a DataFrame

    Args:
        df (pd.DataFrame): DataFrame to download
        filename (str): Name for the downloaded file
        link_text (str): Text to display for the link

    Returns:
        str: HTML download link
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href


def handle_api_error(response: requests.Response) -> Optional[str]:
    """
    Handle API error responses

    Args:
        response: requests.Response object

    Returns:
        str: Error message or None if no error
    """
    if response.status_code == 200:
        return None

    try:
        error_detail = response.json().get("detail", "Unknown error")
    except Exception:
        error_detail = response.text or f"HTTP {response.status_code} error"

    return f"API Error ({response.status_code}): {error_detail}"


def safe_json_loads(json_str: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Safely load JSON string

    Args:
        json_str (str): JSON string to parse
        default (dict): Default value if parsing fails

    Returns:
        dict: Parsed JSON or default value
    """
    if default is None:
        default = {}

    try:
        import json

        return json.loads(json_str)
    except Exception:
        return default


def display_metric_card(
    title: str, value: str, delta: str = None, delta_color: str = "normal"
):
    """
    Display a metric card with title, value, and optional delta

    Args:
        title (str): Metric title
        value (str): Metric value
        delta (str): Delta value (optional)
        delta_color (str): Color for delta ("normal", "inverse")
    """
    st.metric(label=title, value=value, delta=delta, delta_color=delta_color)


def create_info_box(title: str, content: str, box_type: str = "info"):
    """
    Create an information box

    Args:
        title (str): Box title
        content (str): Box content
        box_type (str): Type of box ("info", "success", "warning", "error")
    """
    if box_type == "info":
        st.info(f"**{title}**\n\n{content}")
    elif box_type == "success":
        st.success(f"**{title}**\n\n{content}")
    elif box_type == "warning":
        st.warning(f"**{title}**\n\n{content}")
    elif box_type == "error":
        st.error(f"**{title}**\n\n{content}")
    else:
        st.info(f"**{title}**\n\n{content}")


def format_number(number: float, decimals: int = 2) -> str:
    """
    Format number with specified decimal places

    Args:
        number (float): Number to format
        decimals (int): Number of decimal places

    Returns:
        str: Formatted number
    """
    try:
        return f"{number:.{decimals}f}"
    except Exception:
        return str(number)


def get_column_types(df: pd.DataFrame) -> Dict[str, list]:
    """
    Get column types from DataFrame

    Args:
        df (pd.DataFrame): DataFrame to analyze

    Returns:
        dict: Dictionary with 'numerical' and 'categorical' column lists
    """
    numerical_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    return {"numerical": numerical_cols, "categorical": categorical_cols}


def display_dataframe_info(df: pd.DataFrame):
    """
    Display comprehensive DataFrame information

    Args:
        df (pd.DataFrame): DataFrame to analyze
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", f"{df.shape[0]:,}")

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        memory_usage = df.memory_usage(deep=True).sum()
        st.metric("Memory Usage", format_file_size(memory_usage))

    with col4:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing_values:,}")


def create_feature_selector(
    features: list, label: str, key: str, help_text: str = None
) -> str:
    """
    Create a feature selector widget

    Args:
        features (list): List of available features
        label (str): Label for the selector
        key (str): Unique key for the widget
        help_text (str): Help text for the widget

    Returns:
        str: Selected feature
    """
    return st.selectbox(label=label, options=features, key=key, help=help_text)


def display_loading_spinner(message: str = "Loading..."):
    """
    Display a loading spinner with custom message

    Args:
        message (str): Loading message to display
    """
    return st.spinner(message)


def check_api_connection(api_base_url: str) -> tuple[bool, str]:
    """
    Check if API server is accessible

    Args:
        api_base_url (str): Base URL of the API

    Returns:
        tuple: (is_connected, message)
    """
    try:
        response = requests.get(f"{api_base_url}/", timeout=5)
        if response.status_code == 200:
            return True, "API server is accessible"
        else:
            return False, f"API server returned status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API server. Please ensure it's running."
    except requests.exceptions.Timeout:
        return False, "API server connection timed out"
    except Exception as e:
        return False, f"Error connecting to API server: {str(e)}"
