import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def clean_temp_hum_data(filepath):
    """Loads and cleans temperature/humidity data."""
    df = pd.read_csv(filepath, names=['date', 'time', 'temperature', 'humidity'])
    # Remove 'T=' and 'H=' prefixes
    df['temperature'] = df['temperature'].str.replace('T=', '', regex=False)
    df['humidity'] = df['humidity'].str.replace('H=', '', regex=False)
    # Convert to numeric, coercing errors (like 'error' strings) to NaN
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    # Drop duplicates and NaNs
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    return df

def classify_temp(t):
    if t < 9.0 or t > 28.0:
        return 'Danger'
    elif (9.0 <= t < 18.0) or (23.0 < t <= 28.0):
        return 'Warning'
    else:
        return 'Safe'

def classify_hum(h):
    if h < 12.0 or h > 40.0:
        return 'Danger'
    elif (12.0 <= h < 20.0) or (23.25 < h <= 40.0):
        return 'Warning'
    else:
        return 'Safe'

def classify_env_combined(row):
    t_status = classify_temp(row['temperature'])
    h_status = classify_hum(row['humidity'])
    # Combine status by taking the maximum severity: Danger > Warning > Safe
    if t_status == 'Danger' or h_status == 'Danger':
        return 'Danger'
    elif t_status == 'Warning' or h_status == 'Warning':
        return 'Warning'
    else:
        return 'Safe'

def classify_gas_sensor(val):
    if val < 450.0:
        return 'Danger'
    elif 450.0 <= val <= 600.0:
        return 'Warning'
    else:
        return 'Safe'

def classify_gas_combined(row, sensor_cols):
    statuses = [classify_gas_sensor(row[col]) for col in sensor_cols]
    if 'Danger' in statuses:
        return 'Danger'
    elif 'Warning' in statuses:
        return 'Warning'
    else:
        return 'Safe'

def classify_ultrasonic(row):
    dist = row['distance']
    speed = row['speed']
    # Danger Zone: Distance < 20.0 OR Speed > 15.0
    if dist < 20.0 or speed > 15.0:
        return 'Danger'
    # Safe Zone: Distance > 50.0 AND Speed < 5.0
    elif dist > 50.0 and speed < 5.0:
        return 'Safe'
    # Warning Zone: Otherwise
    else:
        return 'Warning'

def classify_earthquake(row):
    mag = row['magnitude']
    if mag < 6.0 or mag > 15.0:
        return 'Danger'
    elif 6.0 <= mag <= 12.0:
        return 'Safe'
    else:
        return 'Warning'

def main():
    print("=" * 70)
    print("                IoT TELEMETRY ANALYSIS PIPELINE                 ")
    print("=" * 70)
    
    # 1. Load and clean datasets
    print("[*] Ingesting and cleaning datasets...")
    df_th = clean_temp_hum_data("dataset/temp_hum_sensor.csv")
    
    df_gas = pd.read_csv("dataset/gas_sensor.csv")
    df_gas.drop_duplicates(inplace=True)
    df_gas.dropna(inplace=True)
    
    df_ultra = pd.read_csv("dataset/ultrasonic_sensor.csv")
    df_ultra.drop_duplicates(inplace=True)
    df_ultra.dropna(inplace=True)
    
    df_earth = pd.read_csv("dataset/earthquake_sensor.csv")
    df_earth.drop_duplicates(inplace=True)
    df_earth.dropna(inplace=True)
    
    # Calculate magnitude for earthquake
    df_earth['magnitude'] = np.sqrt(df_earth['X']**2 + df_earth['Y']**2 + df_earth['Z']**2)
    
    print(f"    - Temperature/Humidity: {len(df_th)} records")
    print(f"    - MQ Gas Sensors:       {len(df_gas)} records")
    print(f"    - Ultrasonic Proximity: {len(df_ultra)} records")
    print(f"    - Earthquake Vibration: {len(df_earth)} records\n")
    
    # 2. Run Isolation Forest Anomaly Detection (matching notebook settings)
    print("[*] Running Isolation Forest anomaly detection...")
    iso_forest_temp = IsolationForest(contamination=0.05, random_state=42)
    df_th['temp_anomaly'] = iso_forest_temp.fit_predict(df_th[['temperature']])
    df_th['temp_anomaly'] = df_th['temp_anomaly'].map({1: 0, -1: 1})
    
    iso_forest_hum = IsolationForest(contamination=0.05, random_state=42)
    df_th['hum_anomaly'] = iso_forest_hum.fit_predict(df_th[['humidity']])
    df_th['hum_anomaly'] = df_th['hum_anomaly'].map({1: 0, -1: 1})
    
    # 3. Apply threshold classifications
    print("[*] Applying critical telemetry thresholds and classifying status...")
    
    # Temperature and Humidity
    df_th['temp_status'] = df_th['temperature'].apply(classify_temp)
    df_th['hum_status'] = df_th['humidity'].apply(classify_hum)
    df_th['combined_status'] = df_th.apply(classify_env_combined, axis=1)
    
    # Gas Sensors
    mq_cols = [c for c in df_gas.columns if 'MQ' in c]
    for col in mq_cols:
        df_gas[f'{col}_status'] = df_gas[col].apply(classify_gas_sensor)
    df_gas['combined_status'] = df_gas.apply(lambda r: classify_gas_combined(r, mq_cols), axis=1)
    
    # Ultrasonic Proximity
    df_ultra['calculated_status'] = df_ultra.apply(classify_ultrasonic, axis=1)
    
    # Earthquake Vibration
    df_earth['status'] = df_earth.apply(classify_earthquake, axis=1)
    
    # 4. Generate & Display Reports
    print("\n" + "=" * 70)
    print("                         KPI DASHBOARD                          ")
    print("=" * 70)
    
    # Section 1: Temp & Hum
    print("\n[1] Temperature & Humidity Sensor Analysis")
    print(f"    - Temperature Mean / Min / Max: {df_th['temperature'].mean():.2f} °C / {df_th['temperature'].min():.2f} °C / {df_th['temperature'].max():.2f} °C")
    print(f"    - Humidity Mean / Min / Max:    {df_th['humidity'].mean():.2f} % / {df_th['humidity'].min():.2f} % / {df_th['humidity'].max():.2f} %")
    print(f"    - Isolation Forest Anomaly Flags: Temp = {df_th['temp_anomaly'].sum()}, Hum = {df_th['hum_anomaly'].sum()}")
    print("    - Status Threshold Breakdown:")
    for status in ['Safe', 'Warning', 'Danger']:
        cnt_t = (df_th['temp_status'] == status).sum()
        cnt_h = (df_th['hum_status'] == status).sum()
        cnt_c = (df_th['combined_status'] == status).sum()
        pct_c = (cnt_c / len(df_th)) * 100
        print(f"      * {status:7s} -> Temp: {cnt_t:4d} | Hum: {cnt_h:4d} | Combined Env: {cnt_c:4d} ({pct_c:.2f}%)")
        
    # Section 2: Gas Sensor
    print("\n[2] MQ Gas Sensors Analysis")
    print(f"    - Most Common Gas Event: {df_gas['Gas'].mode()[0]}")
    print(f"    - Average MQ8 Reading:   {df_gas['MQ8'].mean():.2f} ADC (Safe > 600)")
    print(f"    - Average MQ135 Reading: {df_gas['MQ135'].mean():.2f} ADC (Safe > 600)")
    print("    - Combined Gas Safety Status Breakdown:")
    for status in ['Safe', 'Warning', 'Danger']:
        cnt = (df_gas['combined_status'] == status).sum()
        pct = (cnt / len(df_gas)) * 100
        print(f"      * {status:7s} -> {cnt:5d} readings ({pct:.2f}%)")
    print("    - Key Gas Sensors Breakdown (MQ8 & MQ135):")
    for status in ['Safe', 'Warning', 'Danger']:
        cnt_mq8 = (df_gas['MQ8_status'] == status).sum()
        cnt_mq135 = (df_gas['MQ135_status'] == status).sum()
        print(f"      * {status:7s} -> MQ8: {cnt_mq8:5d} | MQ135: {cnt_mq135:5d}")
        
    # Section 3: Ultrasonic Proximity
    print("\n[3] Ultrasonic Proximity (Collision Avoidance)")
    print(f"    - Average Distance to Object: {df_ultra['distance'].mean():.2f} cm")
    print(f"    - Average Approach Speed:     {df_ultra['speed'].mean():.2f} units/s")
    print("    - Collision Avoidance Status Breakdown:")
    for status, label in [('Safe', 'Clear (Status 0)'), ('Warning', 'Warning (Status 1)'), ('Danger', 'Danger (Status 2)')]:
        cnt = (df_ultra['calculated_status'] == status).sum()
        pct = (cnt / len(df_ultra)) * 100
        print(f"      * {label:20s} -> {cnt:4d} events ({pct:.2f}%)")
        
    # Section 4: Earthquake Vibration
    print("\n[4] Earthquake Vibration Analysis (Seismic Activity)")
    print(f"    - Average Magnitude:   {df_earth['magnitude'].mean():.4f} (Gravity baseline ~9.8)")
    print(f"    - Max Vibration Spike: {df_earth['magnitude'].max():.2f}")
    print("    - Seismic Activity Breakdown:")
    for status in ['Safe', 'Warning', 'Danger']:
        cnt = (df_earth['status'] == status).sum()
        pct = (cnt / len(df_earth)) * 100
        print(f"      * {status:7s} -> {cnt:5d} readings ({pct:.2f}%)")
        
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
