import influxdb_client
import pandas as pd
import numpy as np
import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Bidirectional, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, mean_absolute_error, r2_score

class BGP_PrefixPredictor:
    def __init__(self, influx_url, influx_token, influx_org, influx_bucket, peer_address, measurement, field, log_file_path):
        """Initialize the predictor with InfluxDB parameters and log file path."""
        self.influx_url = influx_url
        self.influx_token = influx_token
        self.influx_org = influx_org
        self.influx_bucket = influx_bucket
        self.peer_address = peer_address
        self.measurement = measurement
        self.field = field
        self.log_file_path = log_file_path  
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = self._build_model()
        self.error_threshold = None  # ✅ Initialize error threshold attribute

    def fetch_data(self):
        """Fetch historical BGP prefix count data from InfluxDB while keeping 1-minute granularity."""
        client = influxdb_client.InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
        query_api = client.query_api()

        query = f"""
        from(bucket: "{self.influx_bucket}")
          |> range(start: -6h)
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

        # Handle Missing Data
        df = df.dropna()
        df = df[df["y"] > 0]

        # ✅ Keep raw 1-minute intervals (NO RESAMPLING)
        df.set_index("ds", inplace=True)  
        df = df.asfreq('1min')  # Ensure 1-minute frequency
        df.interpolate(inplace=True)  # Fill any small gaps using interpolation
        df.reset_index(inplace=True)

        return df

    def preprocess_data(self, df, time_steps=20):
        """Preprocess data: Normalize, split, and create sequences."""
        df[['y']] = self.scaler.fit_transform(df[['y']])

        
        train_size = int(len(df) * 0.80)
        train_df, test_df = df.iloc[:train_size], df.iloc[train_size:]

   
        X_train, y_train = self.create_sequences(train_df['y'].values, time_steps)
        X_test, y_test = self.create_sequences(test_df['y'].values, time_steps)

     
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        return df, train_df, test_df, X_train, y_train, X_test, y_test

    def create_sequences(self, data, time_steps):
        """Create sequences for LSTM training."""
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:i+time_steps])
            y.append(data[i+time_steps])
        return np.array(X), np.array(y)

    def _build_model(self):
        """Define the LSTM-GRU hybrid model."""
        model = Sequential([
            Bidirectional(LSTM(128, activation='tanh', return_sequences=True, input_shape=(50, 1), recurrent_dropout=0.3)),
            BatchNormalization(),
            GRU(128, activation='tanh', return_sequences=True, recurrent_dropout=0.3),
            BatchNormalization(),
            LSTM(64, activation='tanh', return_sequences=False, recurrent_dropout=0.3),
            BatchNormalization(),
            Dense(64, activation='swish'),
            Dense(32, activation='swish'),
            Dense(1)
        ])
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model

    def train_model(self, X_train, y_train):
        """Train the model with adaptive learning rate."""
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-5, verbose=1)

        print("🧠 Training LSTM model...")
        self.model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1, callbacks=[reduce_lr])

    def predict_test_set(self, X_test, y_test, test_df, time_steps=50):
        """Predict values on test set and log performance."""
        print("🔮 Predicting on test data...")
        predictions = self.model.predict(X_test)

        
        predictions_original = self.scaler.inverse_transform(predictions)
        y_test_original = self.scaler.inverse_transform(y_test.reshape(-1, 1))

        
        y_test_original = np.round(y_test_original).astype(int)
        predictions_original = np.round(predictions_original).astype(int)

      
        min_length = min(len(test_df), len(y_test_original))
        test_df = test_df.iloc[-min_length:].reset_index(drop=True)


        test_df['actual'] = y_test_original[:min_length]
        test_df['predicted'] = predictions_original[:min_length]


        rmse = np.sqrt(mean_squared_error(y_test_original[:min_length], predictions_original[:min_length]))
        mape = mean_absolute_percentage_error(y_test_original[:min_length], predictions_original[:min_length]) * 100
        r2 = r2_score(y_test_original[:min_length], predictions_original[:min_length])

        self.error_threshold = int(mean_absolute_error(y_test_original[:min_length], predictions_original[:min_length]))  # ✅ Store as class attribute

        log_message = f"[{datetime.datetime.now()}] RMSE: {rmse:.2f}, MAPE: {mape:.2f}%, R² Score: {r2:.2f}, Error Threshold: ±{self.error_threshold}\n"
        with open(self.log_file_path, "a") as log:
            log.write(log_message)

        print(log_message.strip())
        return test_df


    def predict_future(self, df, future_steps=10, time_steps=10):
        """Predict next time steps after actual data ends."""
        future_predictions = []
        
    
        if len(df) < time_steps:
            print(f"🚨 Not enough data! Data points available: {len(df)}, required: {time_steps}")
            return pd.DataFrame()

        last_sequence = df['y'].values[-time_steps:].reshape(1, time_steps, 1)
        print(f"📊 Last Sequence for Prediction: {last_sequence}")

        for step in range(future_steps):
            next_pred = self.model.predict(last_sequence)[0, 0]
            
            last_actual = df['y'].values[-1]
            corrected_pred = 0.9 * next_pred + 0.1 * last_actual
            if self.error_threshold and abs(corrected_pred - last_actual) > self.error_threshold:
                corrected_pred = last_actual + np.sign(corrected_pred - last_actual) * self.error_threshold

            print(f"🔹 Step {step + 1}: Prediction = {next_pred}, Corrected = {corrected_pred}")
            
            future_predictions.append(corrected_pred)
            last_sequence = np.roll(last_sequence, -1)
            last_sequence[0, -1, 0] = corrected_pred

        if not future_predictions:
            print("🚨 No future predictions were generated!")
            return pd.DataFrame()

   
        future_predictions_original = np.round(self.scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))).astype(int)

        last_timestamp = df['ds'].iloc[-1]
        future_timestamps = [last_timestamp + datetime.timedelta(minutes=i) for i in range(1, future_steps + 1)]

        return pd.DataFrame({'ds': future_timestamps, 'predicted_prefix_count': future_predictions_original.flatten()})

