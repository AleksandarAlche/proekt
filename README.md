### NBA Awards Prediction System

## Overview
This project uses historical NBA player statistics to predict Most Valuable Player (MVP) and Defensive Player of the Year (DPOY) award winners. The system analyzes player performance metrics, applies statistical models, and produces predictions that can be compared against actual award results.

## Features
- Historical MVP and DPOY winner predictions (1983-2023)
- Interactive dashboard to explore predictions
- Filtering and search capabilities
- Detailed accuracy statistics
- Visualization of prediction results
- Feature importance display
- 
## Requirements
- Python 3.7+
- pandas
- numpy
- scikit-learn
- kagglehub
- Web browser with JavaScript enabled
- Internet connection (for Chart.js CDN)

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/nba-awards-prediction.git
cd nba-awards-prediction
```

### 2. Install required Python packages
```bash
pip install pandas numpy scikit-learn kagglehub
```

### 3. Download the dataset
The script uses kagglehub to automatically download the dataset. If you prefer to download manually:
1. Visit [Kaggle NBA/ABA/BAA Stats Dataset](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats)
2. Download "Player Totals.csv"
3. Place it in the data/ directory

### 4. Generate prediction data
```bash
python scripts/prediction_model.py
```
This will create:
- mvp_predictions_data.json
- dpoy_predictions_data.json

### 5. View the dashboard
Open `index.html` in a web browser to interact with the prediction results.

## How It Works

### Data Processing
1. Loads NBA player statistics from the dataset
2. Cleans data by handling team aggregations (TOT entries)
3. Adds derived metrics like per-game statistics
4. Filters for qualifying players each season

### MVP Prediction Model
- Uses a weighted scoring system based on key offensive and all-around metrics
- Normalizes statistics across seasons
- Identifies statistical leaders in each season
- Compares predictions against actual MVP winners

### DPOY Prediction Model
- Focuses on defensive metrics like blocks, steals, and defensive rebounds
- Emphasizes per-game impact rather than raw totals
- Applies weighted scoring for defensive contribution
- Compares predictions against actual DPOY winners

### Dashboard
- Toggles between MVP and DPOY views
- Displays prediction accuracy
- Shows detailed season-by-season results
- Allows filtering by match/no-match
- Provides search functionality for specific players
- Lists features used in the prediction models

## Results
- Current MVP prediction accuracy: [X]%
- Current DPOY prediction accuracy: [Y]%
