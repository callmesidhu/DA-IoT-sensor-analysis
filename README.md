# IoT Sensor Monitoring & Data Analytics

Welcome to the **IoT Sensor Monitoring & Data Analytics** project. This project provides a comprehensive, professional-grade data cleaning, exploratory data analysis (EDA), anomaly detection, and KPI dashboarding pipeline for four different IoT sensor datasets:
1. **Temperature & Humidity Sensor** (`temp_hum_sensor.csv`)
2. **MQ-Series Gas Sensors** (`gas_sensor.csv`)
3. **Ultrasonic Proximity Sensor** (`ultrasonic_sensor.csv`)
4. **Earthquake Vibration Sensor** (`earthquake_sensor.csv`)

The complete analysis is implemented in the local Jupyter Notebook: **[IoT_Sensor_Analysis.ipynb](file:///c:/Users/sidha/Downloads/DA-IoT-sensor-monitoring/IoT_Sensor_Analysis.ipynb)**.

---

## 📊 Analytics Questions & Answers

### 🌡️ Temperature & Humidity
* **What is the average temperature?**
  * The average (mean) temperature recorded is **21.35 °C** (Median: 20.00 °C, Mode: 21.00 °C).
* **What is the average humidity?**
  * The average (mean) relative humidity is **21.87%** (Median: 21.00%, Mode: 21.00%).
* **What is the highest and lowest value?**
  * **Temperature:** The highest temperature is **37.00 °C**; the lowest is **9.00 °C**.
  * **Humidity:** The highest humidity is **140.00%** (representing an anomalous, physically out-of-bounds reading); the lowest is **12.00%**.
* **How do they change over time?**
  * Both metrics remain fairly stable over the timeline. Temperature oscillates around its 20-21 °C baseline, while humidity hovers around 21% with a few distinct spikes (such as the 140% anomaly). Exploratory analysis reveals a strong negative correlation: as temperature goes up, relative humidity drops, which can be useful for predicting missing values.

---

### 💨 MQ Gas Sensors
* **Which sensor reacts most strongly?**
  * **MQ8** sensor reacts most strongly to gas presence, showing a massive mean voltage/resistance drop from a baseline of **637.15 (NoGas)** down to **315.25** in the presence of a **Mixture**. **MQ135** also reacts strongly to **Smoke**, dropping from **474.47 (NoGas)** down to **308.11**.
* **Which gas produces the highest readings?**
  * The raw readings are highest in **NoGas** (clean air) and **Perfume** conditions across all MQ sensors (e.g., MQ2 averages 748.39 in NoGas and 745.33 in Perfume). Readings drop significantly when exposed to **Smoke** and **Mixture**.
* **Which sensors overlap?**
  * The correlation heatmap shows that **MQ2, MQ3, MQ5, MQ6, and MQ135** have highly overlapping responses (very high correlation blocks). In a production IoT device, we could safely remove several of these sensors to reduce hardware costs without losing key detection capabilities.

---

### 📏 Ultrasonic Proximity
* **How does distance affect risk?**
  * Distance is the primary driver of threat risk. As an object gets closer, the safety status escalates quickly from Clear (0) to Warning (1) and finally Danger (2).
* **How does speed affect risk?**
  * High velocity correlates with higher threat risk (Danger states average 22.99 units of speed, while Clear states average 2.57 units), but speed is secondary to the distance boundary.
* **Which ranges correspond to Clear/Warning/Danger?**
  * 🟢 **Clear (Status 0):** Distance > ~50 units (Average distance: **70.82**, Average speed: **2.57**)
  * 🟡 **Warning (Status 1):** Distance between ~20 and ~50 units (Average distance: **30.04**, Average speed: **9.92**)
  * 🔴 **Danger (Status 2):** Distance < ~20 units (Average distance: **12.72**, Average speed: **22.99**)

---

### 🫨 Earthquake Vibration
* **What is the vibration magnitude?**
  * The overall vibration magnitude is calculated as the Euclidean norm: $\text{magnitude} = \sqrt{X^2 + Y^2 + Z^2}$. The average magnitude is **9.89**, which perfectly aligns with the standard gravitational acceleration baseline (~9.8 m/s²).
* **Are there unusual spikes?**
  * Yes. There is a massive, unusual seismic spike reaching a maximum vibration magnitude of **373.01**, primarily registering along the X-axis (Max X = 373.00), indicating a major earthquake event.
* **What percentage of readings are abnormal?**
  * Defining abnormal vibration as any reading deviating significantly from the gravitational baseline (magnitude > 12 or < 6), **3.23%** (968 out of 30,000 readings) of the dataset is classified as abnormal.

---

## 📈 Executive KPI Dashboard
Here is the summary output generated from the final cells of the analysis notebook:
```text
============================================================
             EXECUTIVE KPI DASHBOARD            
============================================================
[1] Temp / Hum Sensor
    - Average Temperature:     21.35 °C
    - Temperature Anomalies:   15 flags (Isolation Forest)
    - Average Humidity:        21.87 %
    - Humidity Anomalies:      10 flags (Isolation Forest)

[2] Gas Sensor
    - Most Detected Gas:       Mixture

[3] Ultrasonic Proximity
    - Critical Danger Events:  113

[4] Earthquake Vibration
    - Max Vibration Spike:     373.01 (Magnitude)
============================================================
```

---

## 🚀 How to Run the Analysis
1. Ensure you have the required Python packages installed:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn
   ```
2. Open the Jupyter Notebook locally:
   ```bash
   jupyter notebook IoT_Sensor_Analysis.ipynb
   ```
3. Run all cells to clean the data, display interactive visualizations, execute the Isolation Forest anomaly detection, and print the Executive KPI Dashboard.

*Note: This notebook is fully compatible with Google Colab. To run on Colab, upload the notebook and ensure the `dataset/` folder is uploaded to your Colab directory.*