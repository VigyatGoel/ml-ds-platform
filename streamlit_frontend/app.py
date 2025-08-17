import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import config

st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.SIDEBAR_STATE,
)


class MLPlatformAPI:
    """API client for the ML Platform"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def upload_csv(self, file):
        """Upload CSV file to the API"""
        try:
            files = {"file": (file.name, file, "text/csv")}
            response = requests.post(
                f"{self.base_url}/csv_file/upload_csv", files=files
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error uploading file: {str(e)}")
            return None

    def extract_features(self, file_path: str):
        """Extract features from CSV file"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/csv_file/extract_features", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error extracting features: {str(e)}")
            return None

    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary file"""
        try:
            params = {"file_path": file_path}
            response = requests.delete(
                f"{self.base_url}/csv_file/cleanup_temp_file", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_data_info(self, file_path: str):
        """Get data info"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_summary/data_info", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting data info: {str(e)}")
            return None

    def get_data_description(self, file_path: str):
        """Get data description"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_summary/data_description", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting data description: {str(e)}")
            return None

    def get_file_info(self, file_path: str):
        """Get file info"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_summary/file_info", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting file info: {str(e)}")
            return None

    def get_scatter_plot(self, file_path: str, feature1: str, feature2: str):
        """Get scatter plot data"""
        try:
            params = {"csv_file": file_path, "feature1": feature1, "feature2": feature2}
            response = requests.get(
                f"{self.base_url}/data_science/scatter_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting scatter plot: {str(e)}")
            return None

    def get_histogram_plot(self, file_path: str):
        """Get histogram plot data"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_science/histogram_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting histogram plot: {str(e)}")
            return None

    def get_line_plot(self, file_path: str):
        """Get line plot data"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_science/line_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting line plot: {str(e)}")
            return None

    def get_correlation_matrix(self, file_path: str):
        """Get correlation matrix data"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_science/correlation_matrix", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting correlation matrix: {str(e)}")
            return None

    def get_box_plot(self, file_path: str, feature1: str):
        """Get box plot data"""
        try:
            params = {"csv_file": file_path, "feature1": feature1}
            response = requests.get(
                f"{self.base_url}/data_science/box_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting box plot: {str(e)}")
            return None

    def get_pair_plot(self, file_path: str):
        """Get pair plot data"""
        try:
            params = {"csv_file": file_path}
            response = requests.get(
                f"{self.base_url}/data_science/pair_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting pair plot: {str(e)}")
            return None

    def get_area_plot(self, file_path: str, feature1: str):
        """Get area plot data"""
        try:
            params = {"csv_file": file_path, "feature1": feature1}
            response = requests.get(
                f"{self.base_url}/data_science/area_plot", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting area plot: {str(e)}")
            return None

    def train_models(self, file_path: str, target_var: str):
        """Train machine learning models"""
        try:
            params = {"csv_file": file_path, "target_var": target_var}
            response = requests.get(
                f"{self.base_url}/machine_learning/train", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error training models: {str(e)}")
            return None

    def download_model(self, model_name: str):
        """Download a trained model"""
        try:
            params = {"model_name": model_name}
            response = requests.get(
                f"{self.base_url}/machine_learning/download", params=params
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading model: {str(e)}")
            return None


def initialize_session_state():
    """Initialize session state variables"""
    if "uploaded_file_path" not in st.session_state:
        st.session_state.uploaded_file_path = None
    if "features" not in st.session_state:
        st.session_state.features = None
    if "label_column" not in st.session_state:
        st.session_state.label_column = None
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "df" not in st.session_state:
        st.session_state.df = None
    if "training_completed" not in st.session_state:
        st.session_state.training_completed = False
    if "training_results" not in st.session_state:
        st.session_state.training_results = None


def main():
    """Main Streamlit application"""
    st.markdown(
        """
    <style>
    /* Better spacing and styling */
    .nav-header {
        margin-bottom: 1rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    initialize_session_state()

    api_client = MLPlatformAPI(config.API_BASE_URL)

    st.title("🤖 Machine Learning & Data Science Platform")
    st.markdown("---")

    with st.sidebar:
        st.header("📁 File Upload")

        uploaded_file = st.file_uploader(
            "Choose a CSV file", type=["csv"], help="Upload your dataset in CSV format"
        )

        if uploaded_file is not None and st.session_state.uploaded_file_path is None:
            with st.spinner("Uploading file..."):
                upload_result = api_client.upload_csv(uploaded_file)

                if upload_result:
                    st.session_state.uploaded_file_path = upload_result[
                        "absolute_file_path"
                    ]
                    st.session_state.original_filename = upload_result.get(
                        "original_filename", uploaded_file.name
                    )
                    st.success(
                        f"✅ File '{st.session_state.original_filename}' uploaded successfully to temporary location"
                    )

                    with st.spinner("Extracting features..."):
                        features_result = api_client.extract_features(
                            st.session_state.uploaded_file_path
                        )

                        if features_result:
                            st.session_state.features = features_result[
                                "feature_columns"
                            ]
                            st.session_state.label_column = features_result[
                                "label_column"
                            ]
                            st.session_state.data_loaded = True

                            try:
                                uploaded_file.seek(0)
                                st.session_state.df = pd.read_csv(uploaded_file)
                            except Exception as e:
                                st.error(
                                    f"Error reading CSV from uploaded file: {str(e)}"
                                )

    if not st.session_state.data_loaded:
        st.info("Please upload a CSV file to get started")

        st.subheader("🎯 What you can do with this platform:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            **📊 Data Overview**
            - File information
            - Data description
            - Statistical summary
            """)

        with col2:
            st.markdown("""
            **📈 Visualizations**
            - Scatter plots
            - Histograms
            - Line plots
            - Correlation matrix
            - Box plots
            - Pair plots
            - Area plots
            """)

        with col3:
            st.markdown("""
            **🔍 Data Analysis**
            - Feature exploration
            - Data quality checks
            - Statistical insights
            """)

        with col4:
            st.markdown("""
            **🤖 Machine Learning**
            - Train ML models
            - Compare performance
            - Download trained models
            - Get template code
            """)

    else:
        tab_overview, tab_viz, tab_analysis, tab_ml = st.tabs(
            [
                "📊 Data Overview",
                "📈 Visualizations",
                "🔍 Data Analysis",
                "🤖 Machine Learning",
            ]
        )

        with tab_overview:
            display_data_overview(api_client)
        with tab_viz:
            display_visualizations(api_client)
        with tab_analysis:
            display_data_analysis(api_client)
        with tab_ml:
            display_machine_learning(api_client)


def display_data_overview(api_client):
    """Display data overview page"""
    st.header("📊 Data Overview")

    if st.session_state.df is not None:
        st.subheader("📋 Data Preview")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", st.session_state.df.shape[0])
        with col2:
            st.metric("Columns", st.session_state.df.shape[1])
        with col3:
            st.metric(
                "Memory Usage",
                f"{st.session_state.df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            )

    st.subheader("📄 File Information")
    with st.spinner("Loading file info..."):
        file_info = api_client.get_file_info(st.session_state.uploaded_file_path)
        if file_info:
            col1, col2 = st.columns(2)
            with col1:
                display_name = st.session_state.get(
                    "original_filename", file_info.get("file_name", "N/A")
                )
                st.metric("File Name", display_name)
            with col2:
                file_size = file_info.get("file_size_MB", 0)
                st.metric("File Size", f"{file_size:.4f} MB")

    st.subheader("ℹ️ Data Information")
    with st.spinner("Loading data info..."):
        data_info = api_client.get_data_info(st.session_state.uploaded_file_path)
        if data_info:
            info_text = data_info.get("data_info", "")
            if info_text:
                lines = info_text.split("\n")

                st.markdown("**Dataset Overview:**")
                for line in lines:
                    if (
                        "entries" in line
                        or "columns" in line
                        or "dtypes" in line
                        or "memory usage" in line
                    ):
                        st.text(line.strip())

                st.markdown("**Column Details:**")

                column_data = []
                capture_columns = False

                for line in lines:
                    line = line.strip()
                    if line.startswith("#") and "Column" in line:
                        capture_columns = True
                        continue
                    elif line.startswith("dtypes:"):
                        capture_columns = False
                        continue
                    elif capture_columns and line and not line.startswith("---"):
                        parts = line.split()
                        if len(parts) >= 4:
                            col_num = parts[0]
                            col_name = parts[1]
                            non_null_count = " ".join(parts[2:4])
                            dtype = parts[4] if len(parts) > 4 else "N/A"
                            column_data.append(
                                {
                                    "#": col_num,
                                    "Column": col_name,
                                    "Non-Null Count": non_null_count,
                                    "Data Type": dtype,
                                }
                            )

                if column_data:
                    df_info = pd.DataFrame(column_data)
                    st.dataframe(df_info, use_container_width=True)
                else:
                    st.text(info_text)

    st.subheader("📊 Statistical Description")
    with st.spinner("Loading data description..."):
        data_description = api_client.get_data_description(
            st.session_state.uploaded_file_path
        )
        if data_description:
            try:
                desc_df = pd.DataFrame(data_description)

                if not desc_df.empty:
                    st.dataframe(desc_df.round(3), use_container_width=True)

                    if len(desc_df.columns) > 0:
                        st.markdown("**Key Statistics:**")

                        numeric_cols = desc_df.select_dtypes(include=["number"]).columns

                        if len(numeric_cols) >= 2:
                            col1, col2, col3, col4 = st.columns(4)

                            first_col = numeric_cols[0]
                            if "mean" in desc_df.index:
                                with col1:
                                    st.metric(
                                        f"Mean ({first_col})",
                                        f"{desc_df.loc['mean', first_col]:.3f}",
                                    )
                            if "std" in desc_df.index:
                                with col2:
                                    st.metric(
                                        f"Std Dev ({first_col})",
                                        f"{desc_df.loc['std', first_col]:.3f}",
                                    )
                            if "min" in desc_df.index:
                                with col3:
                                    st.metric(
                                        f"Min ({first_col})",
                                        f"{desc_df.loc['min', first_col]:.3f}",
                                    )
                            if "max" in desc_df.index:
                                with col4:
                                    st.metric(
                                        f"Max ({first_col})",
                                        f"{desc_df.loc['max', first_col]:.3f}",
                                    )
                else:
                    st.warning("No statistical description data available.")

            except Exception as e:
                st.error(f"Error formatting data description: {str(e)}")
                st.json(data_description)


def display_visualizations(api_client):
    """Display visualizations page"""
    st.header("📈 Data Visualizations")

    if st.session_state.features:
        st.subheader("🎛️ Feature Selection")

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Available Features:** {', '.join(st.session_state.features)}")
        with col2:
            st.info(f"**Label Column:** {st.session_state.label_column}")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            [
                "📊 Scatter Plot",
                "📈 Histogram",
                "📉 Line Plot",
                "🔥 Correlation Matrix",
                "📦 Box Plot",
                "🔍 Pair Plot",
                "📈 Area Plot",
            ]
        )

        with tab1:
            display_scatter_plot(api_client)

        with tab2:
            display_histogram_plot(api_client)

        with tab3:
            display_line_plot(api_client)

        with tab4:
            display_correlation_matrix(api_client)

        with tab5:
            display_box_plot(api_client)

        with tab6:
            display_pair_plot(api_client)

        with tab7:
            display_area_plot(api_client)


def display_scatter_plot(api_client):
    """Display scatter plot"""
    st.subheader("📊 Scatter Plot")

    col1, col2 = st.columns(2)
    with col1:
        feature1 = st.selectbox(
            "Select X-axis feature:", st.session_state.features, key="scatter_x"
        )
    with col2:
        feature2 = st.selectbox(
            "Select Y-axis feature:", st.session_state.features, key="scatter_y"
        )

    if st.button("Generate Scatter Plot", key="scatter_btn"):
        with st.spinner("Generating scatter plot..."):
            scatter_data = api_client.get_scatter_plot(
                st.session_state.uploaded_file_path, feature1, feature2
            )
            if scatter_data:
                try:
                    fig = px.scatter(
                        x=scatter_data[feature1],
                        y=scatter_data[feature2],
                        labels={feature1: feature1, feature2: feature2},
                        title=f"Scatter Plot: {feature1} vs {feature2}",
                    )
                    fig.update_layout(width=800, height=500)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating scatter plot: {str(e)}")
                    st.write("Raw data:", scatter_data)


def display_histogram_plot(api_client):
    """Display histogram plot"""
    st.subheader("📈 Histogram")

    if st.button("Generate Histogram", key="hist_btn"):
        with st.spinner("Generating histogram..."):
            hist_data = api_client.get_histogram_plot(
                st.session_state.uploaded_file_path
            )
            if hist_data:
                try:
                    df = pd.DataFrame(hist_data)

                    numerical_cols = df.select_dtypes(include=["number"]).columns

                    if len(numerical_cols) > 0:
                        for col in numerical_cols:
                            fig = px.histogram(
                                df, x=col, title=f"Histogram of {col}", nbins=20
                            )
                            fig.update_layout(width=800, height=400)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No numerical columns found for histogram.")

                except Exception as e:
                    st.error(f"Error creating histogram: {str(e)}")
                    st.write("Raw data:", hist_data)


def display_line_plot(api_client):
    """Display line plot"""
    st.subheader("📉 Line Plot")

    if st.button("Generate Line Plot", key="line_btn"):
        with st.spinner("Generating line plot..."):
            line_data = api_client.get_line_plot(st.session_state.uploaded_file_path)
            if line_data:
                try:
                    df = pd.DataFrame(line_data)

                    numerical_cols = df.select_dtypes(include=["number"]).columns

                    if len(numerical_cols) > 0:
                        fig = px.line(
                            df.reset_index(),
                            x="index",
                            y=numerical_cols.tolist(),
                            title="Line Plot of Numerical Features",
                        )
                        fig.update_layout(
                            width=800,
                            height=500,
                            xaxis_title="Data Point Index",
                            yaxis_title="Values",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No numerical columns found for line plot.")

                except Exception as e:
                    st.error(f"Error creating line plot: {str(e)}")
                    st.write("Raw data:", line_data)


def display_correlation_matrix(api_client):
    """Display correlation matrix"""
    st.subheader("🔥 Correlation Matrix")

    if st.button("Generate Correlation Matrix", key="corr_btn"):
        with st.spinner("Generating correlation matrix..."):
            corr_data = api_client.get_correlation_matrix(
                st.session_state.uploaded_file_path
            )
            if corr_data:
                try:
                    df = pd.DataFrame(corr_data)

                    if not df.empty:
                        fig = px.imshow(
                            df.values,
                            labels=dict(
                                x="Features", y="Features", color="Correlation"
                            ),
                            x=df.columns,
                            y=df.index,
                            color_continuous_scale="RdBu",
                            aspect="auto",
                            title="Correlation Matrix Heatmap",
                        )
                        fig.update_layout(width=800, height=600)
                        st.plotly_chart(fig, use_container_width=True)

                        st.subheader("Correlation Values")
                        st.dataframe(df.round(3))
                    else:
                        st.warning("No correlation data available.")

                except Exception as e:
                    st.error(f"Error creating correlation matrix: {str(e)}")
                    st.write("Raw data:", corr_data)


def display_box_plot(api_client):
    """Display box plot"""
    st.subheader("📦 Box Plot")

    feature = st.selectbox(
        "Select feature for box plot:", st.session_state.features, key="box_feature"
    )

    if st.button("Generate Box Plot", key="box_btn"):
        with st.spinner("Generating box plot..."):
            box_data = api_client.get_box_plot(
                st.session_state.uploaded_file_path, feature
            )
            if box_data:
                try:
                    feature_data = box_data.get(feature, [])

                    if feature_data:
                        fig = px.box(y=feature_data, title=f"Box Plot: {feature}")
                        fig.update_layout(width=600, height=500, yaxis_title=feature)
                        st.plotly_chart(fig, use_container_width=True)

                        series = pd.Series(feature_data)
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Mean", f"{series.mean():.2f}")
                        with col2:
                            st.metric("Median", f"{series.median():.2f}")
                        with col3:
                            st.metric("Std Dev", f"{series.std():.2f}")
                        with col4:
                            st.metric(
                                "IQR",
                                f"{series.quantile(0.75) - series.quantile(0.25):.2f}",
                            )
                    else:
                        st.warning(f"No data available for feature: {feature}")

                except Exception as e:
                    st.error(f"Error creating box plot: {str(e)}")
                    st.write("Raw data:", box_data)


def display_pair_plot(api_client):
    """Display pair plot"""
    st.subheader("🔍 Pair Plot")

    st.info("This plot shows pairwise relationships between all numerical features.")

    if st.button("Generate Pair Plot", key="pair_btn"):
        with st.spinner("Generating pair plot... (this may take a while)"):
            pair_data = api_client.get_pair_plot(st.session_state.uploaded_file_path)
            if pair_data:
                try:
                    df = pd.DataFrame(pair_data)

                    numerical_cols = df.select_dtypes(
                        include=["number"]
                    ).columns.tolist()

                    if len(numerical_cols) >= 2:
                        fig = px.scatter_matrix(
                            df,
                            dimensions=numerical_cols,
                            title="Pair Plot - Scatter Matrix of Numerical Features",
                        )
                        fig.update_layout(width=800, height=800)
                        st.plotly_chart(fig, use_container_width=True)

                        st.info(
                            f"Showing pairwise relationships for {len(numerical_cols)} numerical features: {', '.join(numerical_cols)}"
                        )
                    else:
                        st.warning("Need at least 2 numerical columns for pair plot.")

                except Exception as e:
                    st.error(f"Error creating pair plot: {str(e)}")
                    st.write(
                        "Raw data sample:",
                        str(pair_data)[:500] + "..."
                        if len(str(pair_data)) > 500
                        else str(pair_data),
                    )


def display_area_plot(api_client):
    """Display area plot"""
    st.subheader("📈 Area Plot")

    feature = st.selectbox(
        "Select feature for area plot:", st.session_state.features, key="area_feature"
    )

    if st.button("Generate Area Plot", key="area_btn"):
        with st.spinner("Generating area plot..."):
            area_data = api_client.get_area_plot(
                st.session_state.uploaded_file_path, feature
            )
            if area_data:
                try:
                    feature_data = area_data.get(feature, [])

                    if feature_data:
                        df = pd.DataFrame(
                            {"index": range(len(feature_data)), feature: feature_data}
                        )

                        fig = px.area(
                            df, x="index", y=feature, title=f"Area Plot: {feature}"
                        )
                        fig.update_layout(
                            width=800,
                            height=500,
                            xaxis_title="Data Point Index",
                            yaxis_title=feature,
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        cumsum = pd.Series(feature_data).cumsum()
                        st.subheader("Cumulative Statistics")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Sum", f"{cumsum.iloc[-1]:.2f}")
                        with col2:
                            st.metric("Data Points", len(feature_data))

                    else:
                        st.warning(f"No data available for feature: {feature}")

                except Exception as e:
                    st.error(f"Error creating area plot: {str(e)}")
                    st.write("Raw data:", area_data)


def display_data_analysis(api_client):
    """Display data analysis page"""
    st.header("🔍 Data Analysis")

    if st.session_state.df is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔢 Numerical Columns")
            numerical_cols = st.session_state.df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if numerical_cols:
                for i, col in enumerate(numerical_cols, 1):
                    st.markdown(f"**{i}.** `{col}`")

                st.info(f"Total: {len(numerical_cols)} numerical columns")
            else:
                st.warning("No numerical columns found")

            st.subheader("📊 Missing Values")
            missing_data = st.session_state.df.isnull().sum()
            missing_df = pd.DataFrame(
                {
                    "Column": missing_data.index,
                    "Missing Count": missing_data.values,
                    "Percentage": (missing_data.values / len(st.session_state.df))
                    * 100,
                }
            )

            missing_df_filtered = missing_df[missing_df["Missing Count"] > 0]

            if not missing_df_filtered.empty:
                st.dataframe(missing_df_filtered, use_container_width=True)
            else:
                st.success("✅ No missing values found!")

        with col2:
            st.subheader("🔤 Categorical Columns")
            categorical_cols = st.session_state.df.select_dtypes(
                include=["object"]
            ).columns.tolist()

            if categorical_cols:
                for i, col in enumerate(categorical_cols, 1):
                    st.markdown(f"**{i}.** `{col}`")

                st.info(f"Total: {len(categorical_cols)} categorical columns")
            else:
                st.warning("No categorical columns found")

            st.subheader("🎯 Data Types")
            dtype_df = pd.DataFrame(
                {
                    "Column": st.session_state.df.dtypes.index,
                    "Data Type": st.session_state.df.dtypes.values.astype(str),
                }
            )
            st.dataframe(dtype_df, use_container_width=True)

        st.subheader("📈 Feature Analysis")
        selected_feature = st.selectbox(
            "Select a feature to analyze:", st.session_state.features
        )

        if selected_feature:
            col1, col2, col3 = st.columns(3)

            feature_data = st.session_state.df[selected_feature]

            with col1:
                st.metric(
                    "Mean",
                    f"{feature_data.mean():.2f}"
                    if feature_data.dtype in ["int64", "float64"]
                    else "N/A",
                )
            with col2:
                st.metric(
                    "Std Dev",
                    f"{feature_data.std():.2f}"
                    if feature_data.dtype in ["int64", "float64"]
                    else "N/A",
                )
            with col3:
                st.metric("Unique Values", feature_data.nunique())

            if feature_data.dtype in ["int64", "float64"]:
                fig = px.histogram(
                    x=feature_data, title=f"Distribution of {selected_feature}"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                value_counts = feature_data.value_counts().head(10)
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=f"Top 10 Values in {selected_feature}",
                )
                st.plotly_chart(fig, use_container_width=True)


def display_machine_learning(api_client):
    """Display machine learning page"""
    st.header("🤖 Machine Learning")

    if st.session_state.df is None:
        st.error("No data loaded. Please upload a CSV file first.")
        return

    st.subheader("1. Select Target Variable")
    target_columns = st.session_state.df.columns.tolist()
    selected_target = st.selectbox(
        "Choose the target variable for prediction:",
        target_columns,
        index=len(target_columns) - 1 if target_columns else 0,
        key="target_variable_select",
    )

    st.subheader("2. Data Preprocessing")
    st.info("The system will automatically handle:")
    st.markdown("""
    - Missing values (filled with mean for numerical, mode for categorical)
    - Categorical encoding (Label encoding)
    - Feature scaling (StandardScaler)
    """)

    def render_training_results(models_data):
        st.subheader("3. Model Performance Metrics")
        metrics_df = pd.DataFrame(models_data).T.round(4)
        st.dataframe(metrics_df, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            accuracy_fig = px.bar(
                x=metrics_df.index,
                y=metrics_df["accuracy"],
                title="Model Accuracy Comparison",
                labels={"x": "Model", "y": "Accuracy"},
            )
            st.plotly_chart(
                accuracy_fig, use_container_width=True, key="accuracy_chart"
            )
        with col2:
            f1_fig = px.bar(
                x=metrics_df.index,
                y=metrics_df["f1_score"],
                title="F1 Score Comparison",
                labels={"x": "Model", "y": "F1 Score"},
            )
            st.plotly_chart(f1_fig, use_container_width=True, key="f1_chart")

        st.subheader("4. Download Trained Models")
        for model_name, metrics in models_data.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{model_name}**")
                st.write(
                    f"Accuracy: {metrics['accuracy']:.4f} | F1 Score: {metrics['f1_score']:.4f}"
                )
            with col2:
                model_bytes_key = f"model_bytes_{model_name}"
                if model_bytes_key not in st.session_state:
                    st.session_state[model_bytes_key] = api_client.download_model(
                        f"{model_name}.pkl"
                    )
                if st.session_state[model_bytes_key]:
                    st.download_button(
                        label="⬇️ Model",
                        data=st.session_state[model_bytes_key],
                        file_name=f"{model_name}.pkl",
                        mime="application/octet-stream",
                        key=f"download_{model_name}",
                    )
            with col3:
                st.caption("Template code below ⬇️")

        st.subheader("5. Using Your Models")
        st.markdown("""
        **Quick Steps:**
        1. Download a model (above) and the preprocessing files (below).
        2. Create a simple loader script (example):
        ```python
        import os
        import numpy as np
        import pickle


        def predict(features: dict, model_path: str):
            d = os.path.dirname(model_path) or "."
            model = pickle.load(open(model_path, "rb"))
            scaler = pickle.load(open(os.path.join(d, "scaler.pkl"), "rb"))
            imputer = pickle.load(open(os.path.join(d, "imputer.pkl"), "rb"))

            try:
                names = pickle.load(open(os.path.join(d, "feature_names.pkl"), "rb"))
            except Exception:
                names = list(features.keys())

            ordered = [features.get(n) for n in names]

            X = np.array(ordered).reshape(1, -1)
            X = scaler.transform(imputer.transform(X))

            pred = model.predict(X)[0]
            probs = (
                model.predict_proba(X)[0].tolist() if hasattr(model, "predict_proba") else None
            )

            return {"prediction": pred, "probabilities": probs}


        # usage:
        result = predict(
            {"feature1": 5.1, "feature2": 3.5, "feature3": 1.4}, "./LogisticRegression.pkl"
        )
        print(result)

        ```
        3. Run predictions in your own scripts.
        """)
        st.markdown("**Dependencies (install once):**")
        st.code("pip install numpy scikit-learn", language="bash")
        st.caption("Optional (for data wrangling / inspection): pip install pandas")

        st.subheader("6. Download Preprocessing Files")
        col1, col2, col3 = st.columns(3)
        preprocessing_files = ["scaler.pkl", "imputer.pkl", "feature_names.pkl"]
        for i, file_name in enumerate(preprocessing_files):
            with [col1, col2, col3][i]:
                prep_key = f"prep_bytes_{file_name}"
                if prep_key not in st.session_state:
                    st.session_state[prep_key] = api_client.download_model(file_name)
                if st.session_state[prep_key]:
                    st.download_button(
                        label=f"⬇️ {file_name}",
                        data=st.session_state[prep_key],
                        file_name=file_name,
                        mime="application/octet-stream",
                        key=f"prep_{file_name}",
                    )

    if st.session_state.get("training_completed") and st.session_state.get(
        "training_results"
    ):
        st.info(
            f"Showing previously trained models for target: {st.session_state.get('selected_target', '(unknown)')}"
        )
        render_training_results(st.session_state.training_results)

    if not st.session_state.get("training_completed"):
        if st.button("🚀 Train Models", type="primary"):
            if not selected_target:
                st.error("Please select a target variable")
                return
            with st.spinner("Training models... This may take a few moments."):
                training_result = api_client.train_models(
                    st.session_state.uploaded_file_path, selected_target
                )
                if training_result and "models" in training_result:
                    st.session_state.training_completed = True
                    st.session_state.training_results = training_result["models"]
                    st.session_state.selected_target = selected_target
                    st.success("✅ Models trained successfully!")
                    st.rerun()
                else:
                    st.error(
                        "Failed to train models. Please check your data and try again."
                    )


if __name__ == "__main__":
    main()
