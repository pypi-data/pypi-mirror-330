import argparse
import pandas as pd
import plotly.io as pio
from propano.anomaly_detector import AnomalyDetector
from propano.visualization import plot_anomalies_interactive


def validate_growth(growth):
    """Validate growth parameter."""
    valid_growth = ["linear", "logistic", "flat"]
    if growth.lower() not in valid_growth:
        raise argparse.ArgumentTypeError(f"Growth must be one of {valid_growth}, got '{growth}'")
    return growth.lower()


def validate_interval_width(value):
    """Validate interval width is between 0 and 1."""
    try:
        float_value = float(value)
        if float_value <= 0 or float_value >= 1:
            raise argparse.ArgumentTypeError(f"Interval width must be between 0 and 1, got {value}")
        return float_value
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid interval width value: {value}") from exc


def validate_float_range(value, min_val=0, max_val=1, param_name="Value"):
    """Validate float value within a range."""
    try:
        float_value = float(value)
        if float_value < min_val or float_value > max_val:
            raise argparse.ArgumentTypeError(
                f"{param_name} must be between {min_val} and {max_val}, got {value}"
            )
        return float_value
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid {param_name}: {value}") from exc


def validate_seasonality(value):
    """Validate seasonality parameter."""
    if value.lower() == "auto" or value.lower() == "true" or value.lower() == "false":
        return value.lower()
    try:
        return int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Seasonality must be 'auto', 'True', 'False', or an integer, got {value}"
        ) from exc


def validate_positive_int(value):
    """Validate positive integer."""
    try:
        int_value = int(value)
        if int_value < 0:
            raise argparse.ArgumentTypeError(f"Value must be positive, got {value}")
        return int_value
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid integer value: {value}") from exc


def main():
    parser = argparse.ArgumentParser(
        description="Propano: Detect anomalies in network time series data."
    )

    parser.add_argument(
        "data_file",
        type=str,
        help="Path to the CSV file containing network time series data.",
    )
    parser.add_argument(
        "--metric",
        type=str,
        default="packet_count",
        help="Column to analyze for anomalies.",
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Path to save the plot (e.g., anomalies_plot.html).",
        default=None,
    )
    parser.add_argument(
        "--growth",
        type=validate_growth,
        help="A string out of 'linear', 'logistic' or 'flat' to specify a linear, logistic or flat trend.",
        default="linear",
    )
    # Changepoint parameters
    parser.add_argument(
        "--changepoints",
        type=str,
        nargs="*",
        help="List of dates for potential changepoints (format: YYYY-MM-DD).",
    )
    parser.add_argument(
        "--n_changepoints",
        type=validate_positive_int,
        default=25,
        help="Number of potential changepoints to include.",
    )
    parser.add_argument(
        "--changepoint_range",
        type=lambda x: validate_float_range(x, 0, 1, "Changepoint range"),
        default=0.8,
        help="Proportion of history for estimating trend changepoints (0-1).",
    )
    parser.add_argument(
        "--changepoint_prior_scale",
        type=float,
        default=0.05,
        help="Parameter modulating the flexibility of automatic changepoint selection.",
    )

    # Seasonality parameters
    parser.add_argument(
        "--yearly_seasonality",
        type=validate_seasonality,
        default="auto",
        help="Fit yearly seasonality: 'auto', True, False, or number of Fourier terms.",
    )
    parser.add_argument(
        "--weekly_seasonality",
        type=validate_seasonality,
        default="auto",
        help="Fit weekly seasonality: 'auto', True, False, or number of Fourier terms.",
    )
    parser.add_argument(
        "--daily_seasonality",
        type=validate_seasonality,
        default="auto",
        help="Fit daily seasonality: 'auto', True, False, or number of Fourier terms.",
    )
    parser.add_argument(
        "--seasonality_mode",
        choices=["additive", "multiplicative"],
        default="additive",
        help="Seasonality mode: 'additive' or 'multiplicative'.",
    )
    parser.add_argument(
        "--seasonality_prior_scale",
        type=float,
        default=10.0,
        help="Parameter modulating the strength of the seasonality model.",
    )

    # Holiday parameters
    parser.add_argument(
        "--holidays_file",
        type=str,
        help="Path to CSV file containing holiday definitions.",
    )
    parser.add_argument(
        "--holidays_prior_scale",
        type=float,
        default=10.0,
        help="Parameter modulating the strength of the holiday components.",
    )
    parser.add_argument(
        "--holidays_mode",
        choices=["additive", "multiplicative"],
        help="Holiday mode. Defaults to seasonality_mode if not specified.",
    )

    # Uncertainty parameters
    parser.add_argument(
        "--interval_width",
        type=lambda x: validate_float_range(x, 0, 1, "Interval width"),
        default=0.95,
        help="Width of the uncertainty intervals (0-1).",
    )
    parser.add_argument(
        "--mcmc_samples",
        type=validate_positive_int,
        default=0,
        help="Number of MCMC samples for full Bayesian inference.",
    )
    parser.add_argument(
        "--uncertainty_samples",
        type=validate_positive_int,
        default=1000,
        help="Number of simulated draws for uncertainty intervals.",
    )

    # Other parameters
    parser.add_argument("--stan_backend", type=str, help="Stan backend to use for inference.")

    # Adding threshold and alpha factor
    parser.add_argument(
        "--anomaly_threshold",
        type=lambda x: validate_float_range(x, 0, 1, "Anomaly Threshold"),
        default=0.5,
        help="Will be used to filter out anomalies",
    )

    parser.add_argument(
        "--alpha",
        type=float,
        default=1.0,
        help="Alpha will be used to generate the anomaly function used to detect anomalies",
    )

    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.data_file, parse_dates=["timestamp"])

    # Run anomaly detection
    detector = AnomalyDetector(args)
    anomalies_df = detector.detect_anomalies(df, args.metric)

    # Generate interactive plot
    fig = plot_anomalies_interactive(anomalies_df, args.metric)

    if args.save:
        # Save as an interactive HTML file
        pio.write_html(fig, args.save)
        print(f"Plot saved to {args.save}")
    else:
        # Show interactive plot in browser
        fig.show()


if __name__ == "__main__":
    main()
