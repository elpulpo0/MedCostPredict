### MED COST PREDICT

## Installation

**Clone this repository**

`git clone https://github.com/elpulpo0/MedCostPredict`

**Create a virtual environnement**

`python -m venv .venv`

**Connect to the virtual environnement**

- mac/linux

    `source .venv/bin/activate.fish`

- windows

    `.venv/Scripts/activate` or `.venv/Scripts/activate.ps1`
    
- bash(windows)

    `source .venv/Scripts/activate`

**Upgrade pip and install librairies**

`python.exe -m pip install --upgrade pip`

`pip install -r requirements.txt`

**Download dataset "insurance.csv" into a folder /data**

https://www.kaggle.com/datasets/mirichoi0218/insurance

## Execution

**Run the app**

`uvicorn backend/main:app --reload`