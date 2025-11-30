import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
df = pd.read_csv("/kaggle/input/earthquake-alert-prediction-dataset/earthquake_alert_balanced_dataset.csv")


# Check for missing values
print(df.isnull().sum())