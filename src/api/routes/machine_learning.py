from pathlib import Path

from fastapi import APIRouter, Query, Depends, Form
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import json

from ...machinelearning.main_train_flow import train_pipeline, predict_pipeline

# Import the template content
# Removed model_load_template import since template download endpoint was removed

router = APIRouter()


def common_csv_file(csv_file: str = Query(..., description="Path to the CSV file")):
    return csv_file


def common_target_var(
    target_var: str = Query(..., description="Target variable for training"),
):
    return target_var


MODEL_DIR = Path("models/")

MODEL_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/train")
async def train_endpoint(
    csv_file: str = Depends(common_csv_file),
    target_var: str = Depends(common_target_var),
):
    try:
        csv_path = Path(csv_file)

        data = pd.read_csv(csv_path)
        if target_var not in data.columns:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"Target variable '{target_var}' not found in CSV columns"
                },
            )

        results = train_pipeline(str(csv_path), target_var, str(MODEL_DIR) + "/")

        saved_files = [
            str("LogisticRegression.pkl"),
            str("SVC.pkl"),
            str("RandomForestClassifier.pkl"),
            str("scaler.pkl"),
            str("imputer.pkl"),
            str("feature_names.pkl"),
        ]

        return JSONResponse(
            content={
                "message": "Models trained successfully",
                "models": results,
                "saved_files": saved_files,
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Error during training: {str(e)}"}
        )


@router.get("/download")
def download_model(
    model_name: str = Query(..., description="Name of model file to download"),
):
    file_path = MODEL_DIR / model_name

    if file_path.exists():
        return FileResponse(
            path=file_path, filename=model_name, media_type="application/octet-stream"
        )
    else:
        return JSONResponse(
            status_code=404, content={"error": f"File '{model_name}' not found!"}
        )


@router.post("/predict")  # Add the route decorator that was missing
async def predict_endpoint(
    model_name: str = Form("RandomForestClassifier"),
    features: str = Form(...),  # JSON string of feature values
):
    """
    Make predictions using a trained model

    Args:
        model_name: Name of the model to use (without .pkl extension)
        features: JSON string of features in format [val1, val2, ...]
    """
    try:
        feature_values = json.loads(features)

        if not isinstance(feature_values, list):
            return JSONResponse(
                status_code=400,
                content={"error": "Features must be provided as a JSON array"},
            )

        model_path = MODEL_DIR / f"{model_name}.pkl"
        if not model_path.exists():
            return JSONResponse(
                status_code=404, content={"error": f"Model {model_name} not found"}
            )

        input_dict = {f"feature_{i}": val for i, val in enumerate(feature_values)}

        # Use predict_pipeline from main_train_flow
        prediction_result = predict_pipeline(
            input_data=input_dict, model_name=model_name, save_path=str(MODEL_DIR) + "/"
        )

        return JSONResponse(
            content={
                "prediction": prediction_result["prediction"],
                "probabilities": prediction_result["probabilities"].tolist()
                if hasattr(prediction_result["probabilities"], "tolist")
                else prediction_result["probabilities"],
                "model_used": model_name,
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Error during prediction: {str(e)}"}
        )
