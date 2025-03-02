import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from propano.anomaly_detector import AnomalyDetector


def plot_anomalies_interactive(df, metric="packet_count"):
    total_anomalies = df["is_anomaly"].sum()
    total_persistent_anomalies = df["persistent_anomaly"].sum()

    # Create subplot layout: 1 row, 2 columns (spanning full width)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            f"All Anomalies ({total_anomalies})",
            f"Reduced False Positives ({total_persistent_anomalies})",
        ],
        horizontal_spacing=0.1,  # Adjust spacing between plots
    )

    # Common traces (actual values, predicted values, bounds)
    for col in [1, 2]:
        fig.add_trace(
            go.Scatter(
                x=df["ds"],
                y=df["y"],
                mode="lines",
                name="Actual",
                line={"color": "blue"},
            ),
            row=1,
            col=col,
        )

        fig.add_trace(
            go.Scatter(
                x=df["ds"],
                y=df["yhat"],
                mode="lines",
                name="Predicted",
                line={"color": "green", "dash": "dash"},
            ),
            row=1,
            col=col,
        )

        fig.add_trace(
            go.Scatter(
                x=df["ds"],
                y=df["yhat_upper"],
                mode="lines",
                name="Upper Bound",
                line={"color": "gray"},
            ),
            row=1,
            col=col,
        )

        fig.add_trace(
            go.Scatter(
                x=df["ds"],
                y=df["yhat_lower"],
                mode="lines",
                name="Lower Bound",
                line={"color": "gray"},
                fill="tonexty",
                fillcolor="rgba(169, 169, 169, 0.3)",
            ),
            row=1,
            col=col,
        )

    # Raw anomalies (before persistence filtering)
    anomalies = df[df["is_anomaly"]]
    fig.add_trace(
        go.Scatter(
            x=anomalies["ds"],
            y=anomalies["y"],
            mode="markers",
            name="All Anomalies",
            marker={"color": "red", "size": 8, "symbol": "x"},
        ),
        row=1,
        col=1,
    )

    # Persistent anomalies (after false positive reduction)
    persistent_anomalies = df[df["persistent_anomaly"]]
    fig.add_trace(
        go.Scatter(
            x=persistent_anomalies["ds"],
            y=persistent_anomalies["y"],
            mode="markers",
            name="Persistent Anomalies",
            marker={"color": "orange", "size": 10, "symbol": "star"},
        ),
        row=1,
        col=2,
    )

    # Layout settings
    fig.update_layout(
        title=f"Anomaly Detection in {metric.replace('_', ' ').title()}",
        xaxis_title="Timestamp",
        yaxis_title=metric.replace("_", " ").title(),
        template="plotly_white",
        legend={"x": 1.05, "y": 1, "bgcolor": "rgba(255,255,255,0.6)"},
        width=1800,  # Increased width for full-screen stretching
        height=600,  # Set height for better readability
    )

    # Expand x and y axes
    fig.update_xaxes(title_text="Timestamp", row=1, col=1)
    fig.update_xaxes(title_text="Timestamp", row=1, col=2)
    fig.update_yaxes(title_text=metric.replace("_", " ").title(), row=1, col=1)
    fig.update_yaxes(title_text=metric.replace("_", " ").title(), row=1, col=2)

    # Show the interactive plot
    fig.show()
    return fig


if __name__ == "__main__":
    #file = "../data/processed/cpu_usage_data_1hr.csv"
    file = "../data/processed/cpu_usage_data_with_anomalies.csv"
    # Load sample data
    df = pd.read_csv(file, parse_dates=["timestamp"])

    # Run anomaly detection
    detector = AnomalyDetector()
    anomalies_df = detector.detect_anomalies(df, "cpu_usage")

    df["is_anomaly"] = anomalies_df["is_anomaly"]

    # Save theupdated dataframe to the new original dataframe
    df.to_csv(file, index=False)

    # Show interactive plot with both views
    plot_anomalies_interactive(anomalies_df, "cpu_usage")
