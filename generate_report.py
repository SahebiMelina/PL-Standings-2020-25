
from pathlib import Path
import pandas as pd

# 1. Locate the Excel file
BASE_DIR = Path(__file__).resolve().parent

file_path = BASE_DIR / "NFL Stats 2022 Update.xlsx"

# 2. Load the Excel dataset
df = pd.read_excel(file_path, header=1)

# 3. Clean the dataset
df.columns = df.columns.str.strip()

# Remove empty columns
df = df.dropna(axis=1, how="all")

# Remove unnecessary unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# 4. Display basic information
print("\n--- DATASET OVERVIEW ---")
print(df.head())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN INFORMATION ---")
print(df.info())

# 5. Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 6. Descriptive statistics
print("\n--- DESCRIPTIVE STATISTICS ---")
print(df.describe())

# 7. Correlation analysis
print("\n--- CORRELATION WITH RECEIVING YARDS ---")

correlations = df.corr(numeric_only=True)[
    "Total Receiving Yards*"
].sort_values(ascending=False)

print(correlations)

# 8. Save the results
output_dir = BASE_DIR / "analysis_results"
output_dir.mkdir(exist_ok=True)

df.describe().to_csv(output_dir / "descriptive_statistics.csv")

correlations.to_csv(output_dir / "receiving_yards_correlations.csv")

print("\nAnalysis completed successfully!")
