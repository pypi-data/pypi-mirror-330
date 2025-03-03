def analyze_dataset(file_path, target_column=None):
    """Analyze a dataset and return summary statistics and visualizations."""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler

    # Load and prepare data
    df = pd.read_csv(file_path)

    # Basic data cleaning
    df = df.dropna()

    # Feature analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Summary statistics
    summary = {
        "numeric_stats": df[numeric_cols].describe(),
        "categorical_counts": {col: df[col].value_counts() for col in categorical_cols[:5]},
        "correlation": df[numeric_cols].corr()
    }

    # Visualization
    plt.figure(figsize=(12, 8))
    df[numeric_cols[:5]].boxplot()
    plt.title("Distribution of Numeric Features")
    plt.savefig("numeric_distribution.png")

    # Optional target analysis
    if target_column and target_column in df.columns:
        # Correlation with target
        if target_column in numeric_cols:
            target_corr = df[numeric_cols].corrwith(df[target_column]).sort_values(ascending=False)
            summary["target_correlation"] = target_corr

        # Feature importance
        if target_column in numeric_cols:
            X = df.drop(columns=[target_column])
            y = df[target_column]

            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X[numeric_cols])

            # Train a simple model
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X_scaled, y)

            # Get feature importance
            importance = model.feature_importances_
            feature_imp = pd.DataFrame({
                "Feature": numeric_cols,
                "Importance": importance
            }).sort_values("Importance", ascending=False)

            summary["feature_importance"] = feature_imp

    return summary
