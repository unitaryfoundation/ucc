import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from common import annotate_and_adjust, extract_compiler_versions

# Get the directory of the current script
directory_of_this_file = os.path.dirname(os.path.abspath(__file__))

# Construct the correct path to the results folder
results_folder = os.path.join(directory_of_this_file, "../results")

# Use glob to find all CSV files in the results folder
csv_files = glob.glob(os.path.join(results_folder, "expval_*.csv"))

# Iterate through all CSV files and load them into dataframes with date column
dfs = []  # List to store dataframes
for file in csv_files:
    # Extract the version from the file header
    with open(file, "r") as f:
        header_line = f.readline().strip()
        compiler_versions = extract_compiler_versions(header_line)
    # Extract the date from the filename (assuming the date is after 'expval_' and before '.csv')
    date_label = str(file).split("_")[1].split(".")[0]

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file, comment="#")

    # Add the extracted date as a new column in the dataframe
    df["date"] = date_label
    df["compiler_version"] = df["compiler"].map(compiler_versions)

    # Append the dataframe to the list
    dfs.append(df)

# Concatenate all dataframes into one large dataframe
df_all = pd.concat(dfs, ignore_index=True)

# Convert the 'date' column to datetime
df_all["date"] = pd.to_datetime(df_all["date"])

# Get the earliest date for each compiler version
new_version_dates = df_all.groupby(["compiler", "compiler_version"])[
    "date"
].min()

# Get all unique first occurrence dates
unique_dates = new_version_dates.unique()

# Filter on first occurrence of each compiler version based on the date
df_all = df_all[df_all["date"].isin(unique_dates)]

# Group by date and compiler, and calculate the average absolute error
summary = (
    df_all.groupby(["date", "compiler", "compiler_version"])
    .agg(avg_absolute_error=("absolute_error", "mean"))
    .reset_index()
)

# Set up the figure
fig, ax = plt.subplots(figsize=(12, 6))

# Set color map for different compilers
unique_compilers = sorted(summary["compiler"].unique())
colormap = plt.get_cmap("tab10", len(unique_compilers))
color_map = {
    compiler: colormap(i) for i, compiler in enumerate(unique_compilers)
}


# Plot average absolute error over time
for compiler in unique_compilers:
    compiler_data = summary[summary["compiler"] == compiler]

    ax.plot(
        compiler_data["date"],
        compiler_data["avg_absolute_error"],
        label=compiler,
        color=color_map[compiler],
        marker="o",
    )

# Customize plot
last_version_seen = {compiler: None for compiler in unique_compilers}


previous_bboxes = []

for _, row in summary.iterrows():
    # Get the version for this date
    current_version = row["compiler_version"]
    compiler = row["compiler"]
    avg_absolute_error = row["avg_absolute_error"]

    if current_version != last_version_seen[compiler]:
        text = f"{current_version}"
        xy = (row["date"], avg_absolute_error)
        color = color_map[compiler]

        # Add the annotation and adjust for overlap
        annotate_and_adjust(
            ax=ax,
            text=text,
            xy=xy,
            color=color,
            previous_bboxes=previous_bboxes,
            offset=(0, 20),  # Initial offset
            increment=2,  # Vertical adjustment step
            max_attempts=15,
        )
        # plt.pause(0.1)
        # Update the last seen version for this compiler
        last_version_seen[compiler] = current_version


# Customize plot
ax.set_title("Average Absolute Error Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Absolute Error")
ax.grid(True)
ax.legend(title="Compiler")

# Adjust layout and save the figure
plt.tight_layout()
filename = os.path.join(
    directory_of_this_file, "../average_absolute_error_over_time.png"
)
print(f"\n Saving plot to {filename}")
fig.savefig(filename)
