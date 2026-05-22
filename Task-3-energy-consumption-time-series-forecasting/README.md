# Energy Consumption Time Series Forecasting

## Project Overview

This project forecasts short-term household energy consumption using historical time-series data.

Three forecasting approaches were compared:
- ARIMA
- Prophet
- XGBoost

The project includes:
- Time series preprocessing
- Feature engineering
- Model evaluation
- Forecast visualization

---

## Dataset

Dataset used:
- Household Power Consumption Dataset

Expected local file:
- `data/household_power_consumption.txt`

Main target feature:
- `Global_active_power`

Note: the `data/` directory is ignored by Git because the dataset is large. Download the dataset separately and place the text file in the `data/` folder before running the notebook.

---

## Objectives

- Parse and preprocess time-series data
- Resample energy consumption data to hourly averages
- Engineer temporal features
- Train forecasting models
- Compare model performance using MAE and RMSE
- Visualize actual vs. forecasted energy usage

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Statsmodels
- Prophet
- XGBoost
- Scikit-learn

---

## Setup and Usage

1. Create and activate a Python environment.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Add `household_power_consumption.txt` to the `data/` directory.
4. Move into the notebook folder and open the notebook:

```bash
cd notebook
jupyter notebook energy-forecasting.ipynb
```

The notebook reads the first 50,000 rows, resamples the data to hourly averages, trains the forecasting models, and saves plots in the `images/` folder.

---

## Models Used

### ARIMA
Classical statistical forecasting model for time-series analysis.

### Prophet
Prophet forecasting model for trend and seasonality analysis.

### XGBoost
Machine learning regression model using engineered time features.

---

## Evaluation Metrics

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

---

## Key Insights

- Time-based patterns strongly influence energy consumption.
- Feature engineering improves machine learning forecasting performance.
- Different forecasting models produce different prediction behaviors.
- Visual comparison helps evaluate forecast quality.

---

## Project Structure

```text
energy-consumption-time-series-forecasting/
|
|-- data/
|   `-- household_power_consumption.txt
|-- images/
|   |-- hourly_consumption_pattern.png
|   |-- hourly_energy_consumption.png
|   `-- model_forecasts.png
|-- notebook/
|   `-- energy-forecasting.ipynb
|-- README.md
`-- requirements.txt
```

---

## Results

The forecasting models captured short-term energy usage patterns and produced meaningful predictions for household energy consumption.

Generated visualizations:
- `images/hourly_energy_consumption.png`
- `images/hourly_consumption_pattern.png`
- `images/model_forecasts.png`

---

## Author

Muneeb Ur Rehman
