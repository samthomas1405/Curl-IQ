"""
ML Service for Outcome Prediction
Uses scikit-learn to predict hair routine outcomes based on:
- Hair profile (curl pattern, porosity, etc.)
- Routine attributes (products, methods)
- Weather conditions
- Historical patterns
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from pathlib import Path


class MLPredictionService:
    """Machine Learning service for predicting routine outcomes"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.model_path = Path(__file__).parent.parent.parent / "models" / "outcome_predictor.pkl"
        self.scaler_path = Path(__file__).parent.parent.parent / "models" / "scaler.pkl"
        self.encoders_path = Path(__file__).parent.parent.parent / "models" / "encoders.pkl"
        self._ensure_model_dir()
    
    def _ensure_model_dir(self):
        """Ensure models directory exists"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features"""
        categorical_cols = ['curl_pattern', 'porosity', 'density', 'thickness', 'scalp_type', 
                           'drying_method', 'product_type']
        
        for col in categorical_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    # Fit on non-null values
                    non_null = df[col].dropna()
                    if len(non_null) > 0:
                        self.label_encoders[col].fit(non_null)
                
                # Transform
                df[col] = df[col].apply(
                    lambda x: self.label_encoders[col].transform([x])[0] 
                    if pd.notna(x) and x in self.label_encoders[col].classes_ 
                    else -1
                )
        
        return df
    
    def _prepare_features(self, data: List[Dict]) -> pd.DataFrame:
        """Prepare features from raw data"""
        df = pd.DataFrame(data)
        
        # One-hot encode curl pattern (2A, 2B, 3A, etc.)
        if 'curl_pattern' in df.columns:
            curl_numeric = df['curl_pattern'].str.extract(r'(\d)([A-C])')
            df['curl_number'] = curl_numeric[0].astype(float)
            df['curl_letter'] = curl_numeric[1].map({'A': 1, 'B': 2, 'C': 3}).fillna(0)
        
        # Encode categorical features
        df = self._encode_features(df)
        
        # Fill missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        return df
    
    def train_model(self, training_data: List[Dict], target: str = 'overall_score') -> Dict:
        """
        Train the prediction model
        
        Args:
            training_data: List of dictionaries with features and outcomes
            target: Target variable to predict (default: 'overall_score')
        
        Returns:
            Dictionary with training metrics
        """
        if len(training_data) < 10:
            return {
                "error": "Insufficient data",
                "message": "Need at least 10 data points to train model"
            }
        
        df = pd.DataFrame(training_data)
        
        # Prepare features
        feature_cols = [
            'curl_number', 'curl_letter', 'porosity', 'density', 'thickness', 'scalp_type',
            'humidity', 'temperature', 'dew_point',
            'drying_method', 'product_type', 'num_products',
            'historical_avg_score'
        ]
        
        # Prepare feature dataframe
        feature_df = self._prepare_features(training_data)
        
        # Select available features
        available_features = [col for col in feature_cols if col in feature_df.columns]
        X = feature_df[available_features]
        y = df[target]
        
        # Split data
        if len(X) < 20:
            X_train, X_test = X, X
            y_train, y_test = y, y
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model
        self.save_model()
        
        return {
            "mae": float(mae),
            "r2_score": float(r2),
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "features_used": available_features
        }
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict outcome for given features
        
        Args:
            features: Dictionary with feature values
        
        Returns:
            Dictionary with predictions and confidence
        """
        if self.model is None:
            # Try to load saved model
            if not self.load_model():
                return {
                    "error": "Model not trained",
                    "message": "Model needs to be trained first. Use /api/v1/ai/train-model endpoint."
                }
        
        # Prepare features
        feature_df = self._prepare_features([features])
        
        # Get feature columns
        feature_cols = [
            'curl_number', 'curl_letter', 'porosity', 'density', 'thickness', 'scalp_type',
            'humidity', 'temperature', 'dew_point',
            'drying_method', 'product_type', 'num_products',
            'historical_avg_score'
        ]
        
        available_features = [col for col in feature_cols if col in feature_df.columns]
        X = feature_df[available_features]
        
        # Scale (handle case where scaler hasn't been fitted)
        try:
            X_scaled = self.scaler.transform(X)
        except Exception:
            # If scaler not fitted, return error
            return {
                "error": "Model not properly initialized",
                "message": "Model needs to be retrained"
            }
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        
        # Get feature importance for explanation
        feature_importance = dict(zip(
            available_features,
            self.model.feature_importances_[:len(available_features)]
        ))
        
        # Calculate confidence (based on tree variance)
        tree_predictions = [tree.predict(X_scaled)[0] for tree in self.model.estimators_]
        confidence = 1.0 - (np.std(tree_predictions) / (np.mean(tree_predictions) + 1e-6))
        confidence = max(0.0, min(1.0, confidence))
        
        return {
            "predicted_score": float(prediction),
            "confidence": float(confidence),
            "feature_importance": {k: float(v) for k, v in sorted(
                feature_importance.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]},
            "prediction_range": {
                "min": float(prediction - np.std(tree_predictions)),
                "max": float(prediction + np.std(tree_predictions))
            }
        }
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            joblib.dump(self.label_encoders, self.encoders_path)
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self) -> bool:
        """Load trained model from disk"""
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.label_encoders = joblib.load(self.encoders_path)
                return True
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


# Singleton instance
ml_service = MLPredictionService()
