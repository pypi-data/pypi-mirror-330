import pandas as pd
import influxdb_client
from prophet import Prophet  # Facebook Prophet for forecasting


class BGP_PrefixPredictor_prophet:
    def __init__(self, influx_url, influx_token, influx_org, influx_bucket, peer_address, measurement, field, time_range):
        """
        Initialize the BGP Prefix Predictor with InfluxDB connection parameters and filtering details.
        """
        self.influx_url = influx_url
        self.influx_token = influx_token
        self.influx_org = influx_org
        self.influx_bucket = influx_bucket
        self.peer_address = peer_address
        self.measurement = measurement
        self.field = field
        self.time_range = time_range  # Dynamic time range (e.g., -240h)

    def fetch_data(self):
        """Fetch historical BGP prefix count data from InfluxDB while keeping 1-minute granularity."""
        client = influxdb_client.InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        query_api = client.query_api()

        query = f"""
        from(bucket: "{self.influx_bucket}")
          |> range(start: {self.time_range})
          |> filter(fn: (r) => r._measurement == "{self.measurement}")
          |> filter(fn: (r) => r.peer_address == "{self.peer_address}")
          |> filter(fn: (r) => r._field == "{self.field}")
          |> keep(columns: ["_time", "_value"])
        """

        tables = query_api.query(query)
        bgp_data = [(record.get_time(), record.get_value()) for table in tables for record in table.records]
        client.close()

        df = pd.DataFrame(bgp_data, columns=["ds", "y"])
        df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)

        return df

    def predict(self, df, minutes):
        """Predict the next `n` minutes of inet_0_received_prefix_count using Prophet model."""
        model = Prophet(interval_width=0.95, daily_seasonality=True)
        model.fit(df)  # Train model on fetched data

        # Create future dataframe for the next `minutes` minutes
        future = model.make_future_dataframe(periods=minutes, freq='min')  # 'T' means minute
        forecast = model.predict(future)

        # Extract relevant predictions
        predicted_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        return predicted_values