from pathlib import Path
from typing import Dict, Any

from .preprocessing import preprocess_data
from .models import train_models, predict_with_model


def train_pipeline(
    data_path: str, target_var: str, save_path: str = "models/"
) -> Dict[str, Dict[str, float]]:
    """
    Complete pipeline for training: preprocess data and train models

    Args:
        data_path: Path to the CSV file
        target_var: Name of the target variable
        save_path: Directory to save models and preprocessing objects

    Returns:
        Dictionary with model names and their metrics (accuracy, precision, recall, f1_score, mse)
    """
    # Ensure save directory exists
    Path(save_path).mkdir(parents=True, exist_ok=True)

    # Preprocess data
    X, y = preprocess_data(data_path, target_var, save_path)

    # Train models
    results = train_models(X, y, save_path)

    return results


def predict_pipeline(
    input_data: Dict[str, Any],
    model_name: str = "RandomForestClassifier",
    save_path: str = "models/",
) -> Dict[str, Any]:
    """
    Complete pipeline for prediction: preprocess input and make prediction

    Args:
        input_data: Dictionary with feature names and values
        model_name: Name of the model to use
        save_path: Directory where models and preprocessing objects are stored

    Returns:
        Dictionary with prediction and probabilities
    """
    from .preprocessing import prepare_prediction_input

    # Prepare input data
    processed_input = prepare_prediction_input(input_data, save_path)

    # Make prediction
    prediction, probabilities = predict_with_model(
        f"{save_path}{model_name}.pkl", processed_input
    )

    return {"prediction": prediction, "probabilities": probabilities}
