import glob
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

directory_of_this_file = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(directory_of_this_file, "../results")

# Initialize a DataFrame to store combined data
data = []

# Process each CSV file
for filepath in glob.glob(os.path.join(results_dir, "expval_*.csv")):
    # Extract the date from the filename
    filename = os.path.basename(filepath)
    date_str = filename.split("_")[1]
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # Read the CSV file and add the date
    df = pd.read_csv(filepath, comment="#")
    df["date"] = date
    data.append(df)

# Combine all data into a single DataFrame
data = pd.concat(data)

# Filter for the latest date
latest_date = data["date"].max()
data_latest = data[data["date"] == latest_date]

# Create a color map for compilers
unique_compilers = sorted(data_latest["compiler"].unique())
colormap = plt.get_cmap("tab10", len(unique_compilers))
color_map = {
    compiler: colormap(i) for i, compiler in enumerate(unique_compilers)
}

# Plot the data using violin plots
fig = plt.figure(figsize=(12, 8))
sns.violinplot(
    data=data_latest,
    x="compiler",
    y="absolute_error",
    palette=color_map,
    density_norm="width",
)

# Customize the plot
plt.title(
    f"Distribution of Absolute Error by Compiler on {latest_date.strftime('%Y-%m-%d')}"
)
plt.xlabel("Compiler")
plt.ylabel("Absolute Error")
plt.grid(True, axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Save the plot
directory_of_this_file = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(
    directory_of_this_file, "../latest_expval_benchmark_by_compiler.png"
)
print(f"\n Saving plot to {filename}")
fig.savefig(filename)
