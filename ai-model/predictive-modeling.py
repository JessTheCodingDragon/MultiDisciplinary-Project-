import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'earthquake_alert_balanced_dataset.csv')
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dataset not found at: {csv_path}")
df = pd.read_csv(csv_path)

# Check for missing values
print(df.isnull().sum())

# Base style
sns.set_style("whitegrid")
plt.rcParams.update({
    'axes.titlesize': 20,
    'axes.titleweight': 'bold',
    'axes.labelsize': 18,
    'axes.labelweight': 'bold',
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 16,
    'legend.title_fontsize': 16
})

def style_axes(ax):
    """Apply spine and tick styling"""
    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax.tick_params(axis='both', colors='black', width=2, length=8)

# Ensure plots directory exists and provide helper to save plots there
PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plots'))
os.makedirs(PLOTS_DIR, exist_ok=True)

def save_plot(filename, **kwargs):
    """Save current matplotlib figure into the repository `plots` folder."""
    path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(path, **kwargs)
    print(f"Saved plot: {path}")

# Plot 1: Histogram of Magnitude
fig, ax = plt.subplots(figsize=(8,6))
ax.hist(df['magnitude'], bins=30, color='skyblue', edgecolor='black', linewidth=1.5)
ax.set_title('Distribution of Earthquake Magnitudes')
ax.set_xlabel('Magnitude')
ax.set_ylabel('Frequency')
style_axes(ax)
save_plot('plot1_magnitude_hist.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 2: Histogram of Depth
fig, ax = plt.subplots(figsize=(8,6))
sns.histplot(df['depth'], bins=30, kde=False, color=plt.cm.viridis(0.6), ax=ax)
ax.set_title('Distribution of Earthquake Depths')
ax.set_xlabel('Depth (km)')
ax.set_ylabel('Frequency')
style_axes(ax)
save_plot('plot2_depth_hist.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 3: Magnitude vs Depth colored by CDI
fig, ax = plt.subplots(figsize=(8,6))
sc = ax.scatter(df['magnitude'], df['depth'], c=df['cdi'], cmap='plasma', s=50, edgecolors='black', linewidth=1.5)
ax.set_title('Magnitude vs Depth Colored by CDI')
ax.set_xlabel('Magnitude')
ax.set_ylabel('Depth (km)')
style_axes(ax)
cbar = fig.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label('CDI', fontsize=16, fontweight='bold', color='black')
save_plot('plot3_mag_depth_cdi.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 4: Magnitude vs MMI colored by MMI
fig, ax = plt.subplots(figsize=(8,6))
sc2 = ax.scatter(df['magnitude'], df['mmi'], c=df['mmi'], cmap='inferno', s=50, edgecolors='black', linewidth=1.5)
ax.set_title('Magnitude vs MMI Colored by MMI')
ax.set_xlabel('Magnitude')
ax.set_ylabel('MMI')
style_axes(ax)
cbar2 = fig.colorbar(sc2, ax=ax, pad=0.02)
cbar2.set_label('MMI', fontsize=16, fontweight='bold', color='black')
save_plot('plot4_mag_mmi_inferno.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 5: Count of Alerts by Type
alert_counts = df['alert'].value_counts()
fig, ax = plt.subplots(figsize=(8,6))
bars = ax.bar(alert_counts.index, alert_counts.values, color=plt.cm.magma(np.linspace(0.2,0.8,len(alert_counts))))
ax.set_title('Count of Earthquake Alerts by Type')
ax.set_xlabel('Alert Level')
ax.set_ylabel('Count')
style_axes(ax)
legend_labels = [f'{lvl}: {cnt}' for lvl,cnt in zip(alert_counts.index, alert_counts.values)]
legend = ax.legend(bars, legend_labels, title='Alerts', loc='center left', bbox_to_anchor=(1,0.5), frameon=True)
legend.get_frame().set_edgecolor('black')
legend.get_title().set_fontweight('bold')
save_plot('plot5_alert_counts.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 6: Boxplot of Magnitude by Alert
fig, ax = plt.subplots(figsize=(8,6))
sns.boxplot(x='alert', y='magnitude', data=df, palette='cividis', ax=ax)
ax.set_title('Magnitude Distribution by Alert Level')
ax.set_xlabel('Alert Level')
ax.set_ylabel('Magnitude')
style_axes(ax)
save_plot('plot6_boxplot_mag_alert.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 8: Line Plot of Average SIG by Magnitude Bin
bins = np.arange(df['magnitude'].min(), df['magnitude'].max()+0.5, 0.5)
df['mag_bin'] = pd.cut(df['magnitude'], bins)
avg_sig = df.groupby('mag_bin')['sig'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(avg_sig['mag_bin'].astype(str), avg_sig['sig'], color=plt.cm.cubehelix(0.7), linewidth=2, marker='o', markersize=8, markeredgewidth=1.5)
ax.set_title('Average SIG by Magnitude Bin')
ax.set_xlabel('Magnitude Bin')
ax.set_ylabel('Average SIG')
style_axes(ax)
leg = fig.legend(['Avg SIG'], loc='center left', bbox_to_anchor=(1,0.5), frameon=True)
leg.get_frame().set_edgecolor('black')
leg.get_texts()[0].set_fontweight('bold')
plt.xticks(rotation=45)
save_plot('plot8_line_avg_sig.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# Plot 9: Bar Plot of Average SIG by Alert
avg_sig_alert = df.groupby('alert')['sig'].mean().sort_index()
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(x=avg_sig_alert.index, y=avg_sig_alert.values, palette='magma', edgecolor='black', ax=ax)
ax.set_title('Average SIG by Alert Level')
ax.set_xlabel('Alert Level')
ax.set_ylabel('Average SIG')
style_axes(ax)
bars2 = ax.patches
labels2 = [f'{lvl}: {val:.2f}' for lvl,val in zip(avg_sig_alert.index, avg_sig_alert.values)]
leg2 = ax.legend(bars2, labels2, title='Avg SIG', loc='center left', bbox_to_anchor=(1,0.5), frameon=True)
leg2.get_frame().set_edgecolor('black')
leg2.get_title().set_fontweight('bold')
save_plot('plot10_bar_avg_sig_alert.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

#  Split Data into Training and Testing Sets
X = df[['magnitude', 'depth', 'cdi', 'mmi', 'sig']]  # Features
y = df['alert']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make Predictions on the Test Set
y_pred = model.predict(X_test)

# Evaluate the Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")
print(classification_report(y_test, y_pred))