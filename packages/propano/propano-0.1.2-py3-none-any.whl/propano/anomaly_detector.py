import numpy as np
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler


class AnomalyDetector:
    def __init__(self, args=None):
        if args is None:
            args = {}
        self.interval_width = getattr(args, "interval_width", 0.6)
        self.alpha = getattr(args, "alpha", 1.0)
        self.anomaly_threshold = getattr(args, "anomaly_threshold", 0.5)
        self.persistence_minutes = getattr(
            args, "persistence_minutes", 5
        )  # Minimum persistence time
        self.input_temporal_granularity = getattr(args, "input_temporal_granularity", 5)

        # Store Prophet-specific parameters
        self.prophet_params = {
            "interval_width": self.interval_width,
            "growth": getattr(args, "growth", "linear"),
            "n_changepoints": getattr(args, "n_changepoints", 25),
            "changepoint_range": getattr(args, "changepoint_range", 0.8),
            "changepoint_prior_scale": getattr(args, "changepoint_prior_scale", 0.05),
            "yearly_seasonality": getattr(args, "yearly_seasonality", "auto"),
            "weekly_seasonality": getattr(args, "weekly_seasonality", "auto"),
            "daily_seasonality": getattr(args, "daily_seasonality", "auto"),
            "seasonality_mode": getattr(args, "seasonality_mode", "additive"),
            "seasonality_prior_scale": getattr(args, "seasonality_prior_scale", 10.0),
            "holidays_prior_scale": getattr(args, "holidays_prior_scale", 10.0),
            "mcmc_samples": getattr(args, "mcmc_samples", 0),
            "uncertainty_samples": getattr(args, "uncertainty_samples", 1000),
        }

    def sigmoid_anomaly_score(self, actual, predicted, scale_factor=None):
        deviation = actual - predicted  # Compute deviation
        if scale_factor is None:
            scale_factor = np.std(deviation)  # Default scaling factor

        z_score = deviation / scale_factor  # Normalize deviation
        sigmoid_score = 2 * (1 / (1 + np.exp(-self.alpha * z_score))) - 1  # Sigmoid transformation
        return np.abs(sigmoid_score)  # Return absolute anomaly score

    def apply_persistence_filter(self, df):
        if self.persistence_minutes <= 0:
            return df

        df = df.sort_values("ds").reset_index(drop=True)  # Ensure proper ordering

        # Convert persistence time to row count
        persistence_window = self.persistence_minutes // self.input_temporal_granularity

        # Identify anomaly type
        df["anomaly_type"] = "none"
        df.loc[df["y"] > df["yhat_upper"], "anomaly_type"] = "high"
        df.loc[df["y"] < df["yhat_lower"], "anomaly_type"] = "low"

        # Separate upper and lower anomalies
        upper_anomalies = df[df["anomaly_type"] == "high"].index.tolist()
        lower_anomalies = df[df["anomaly_type"] == "low"].index.tolist()

        def find_persistent_blocks(anomaly_indices):
            """Identify persistent blocks for a given anomaly type."""
            if not anomaly_indices:
                return []

            blocks = []
            current_block = [anomaly_indices[0]]

            for i in range(1, len(anomaly_indices)):
                if (anomaly_indices[i] - anomaly_indices[i - 1]) <= persistence_window:
                    current_block.append(anomaly_indices[i])
                else:
                    blocks.append(current_block)
                    current_block = [anomaly_indices[i]]

            blocks.append(current_block)  # Add last block
            return blocks

        # Find persistent anomaly blocks separately for upper and lower anomalies
        upper_blocks = find_persistent_blocks(upper_anomalies)
        lower_blocks = find_persistent_blocks(lower_anomalies)

        # Reset persistent anomaly column
        df["persistent_anomaly"] = False

        # Mark start and end of each valid block
        for block in upper_blocks + lower_blocks:
            if len(block) >= persistence_window:
                df.loc[block[0], "persistent_anomaly"] = True  # Start of block
                df.loc[block[-1], "persistent_anomaly"] = True  # End of block

        return df

    def detect_anomalies(self, data, metric="packet_count"):
        """Detects anomalies in time series data using Facebook Prophet."""

        # Prepare data for Prophet
        df = data.rename(columns={"timestamp": "ds", metric: "y"})

        # Normalize the data
        scaler = MinMaxScaler()
        df["y"] = scaler.fit_transform(df[["y"]])

        # Fit Prophet model
        model = Prophet(**self.prophet_params)
        model.fit(df)

        # Make future predictions
        future = model.make_future_dataframe(periods=0)  # Predict only for existing data
        forecast = model.predict(future)

        # Merge predictions with original data
        df = df.merge(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds")

        # Identify anomalies (values outside predicted bounds)
        df["is_anomaly"] = (df["y"] > df["yhat_upper"]) | (df["y"] < df["yhat_lower"])

        # Compute anomaly scores
        df["anomaly_score"] = df.apply(
            lambda row: (
                self.sigmoid_anomaly_score(row["y"], row["yhat"]) if row["is_anomaly"] else 0
            ),
            axis=1,
        )

        # Filter anomalies based on score threshold
        df["is_anomaly"] = df["anomaly_score"] > self.anomaly_threshold

        # Apply persistence check
        df = self.apply_persistence_filter(df)

        # Ensure `persistent_anomaly` is a boolean column
        df["persistent_anomaly"] = df["persistent_anomaly"].astype(bool)

        return df  # Return only persistent anomalies
