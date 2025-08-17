import pickle
from pathlib import Path
from typing import Tuple, Dict, Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder


def preprocess_data(
    data_path: str, target_var: str, save_path: str = "models/"
) -> Tuple[np.ndarray, np.ndarray]:
    Path(save_path).mkdir(parents=True, exist_ok=True)

    # Load data
    data = pd.read_csv(data_path)

    # Handle missing values in numeric columns
    imputer = SimpleImputer(strategy="mean")
    numeric_cols = data.select_dtypes(include=["float64", "int64"]).columns
    data[numeric_cols] = imputer.fit_transform(data[numeric_cols])

    # Encode categorical variables except for target if it's categorical
    for col in data.select_dtypes(include=["object"]).columns:
        if col != target_var:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])

    # Separate features and target
    X = data.drop(target_var, axis=1)
    y = data[target_var]

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save preprocessing objects
    with open(f"{save_path}scaler.pkl", "wb") as file:
        pickle.dump(scaler, file)

    with open(f"{save_path}imputer.pkl", "wb") as file:
        pickle.dump(imputer, file)

    # Save feature column names for later use
    with open(f"{save_path}feature_names.pkl", "wb") as file:
        pickle.dump(X.columns.tolist(), file)

    return X_scaled, y


def prepare_prediction_input(
    input_data: Dict[str, Any], save_path: str = "models/"
) -> np.ndarray:
    # Load feature names
    with open(f"{save_path}feature_names.pkl", "rb") as file:
        feature_names = pickle.load(file)

    # Load imputer
    with open(f"{save_path}imputer.pkl", "rb") as file:
        imputer = pickle.load(file)

    # Load scaler
    with open(f"{save_path}scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    # Create input dataframe with correct feature order
    input_df = pd.DataFrame(
        {name: [input_data.get(name, np.nan)] for name in feature_names}
    )

    # Apply imputation
    input_imputed = imputer.transform(input_df)

    # Apply scaling
    input_scaled = scaler.transform(input_imputed)

    return input_scaled
