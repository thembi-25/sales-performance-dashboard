import pandas as pd
import numpy as np

df = pd.read_csv("/home/claude/project1/data/raw_sales_data.csv")

print("=== BEFORE CLEANING ===")
print(f"Total rows: {len(df)}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Null values:\n{df.isnull().sum()}")
print(f"\nUnique regions: {df['region'].dropna().unique()}")
print(f"Unique categories: {df['category'].unique()}")

# 1. Remove exact duplicates
df = df.drop_duplicates()

# 2. Standardise date formats -> YYYY-MM-DD
def parse_date(d):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(d, format=fmt)
        except ValueError:
            continue
    return pd.NaT

df["order_date"] = df["order_date"].apply(parse_date)

# 3. Standardise category casing -> Title Case
df["category"] = df["category"].str.title()
df["category"] = df["category"].replace({
    "Home & Kitchen": "Home & Kitchen",
    "Beauty & Personal Care": "Beauty & Personal Care",
    "Sports & Outdoors": "Sports & Outdoors",
})

# 4. Standardise region naming
region_map = {
    "APAC": "Asia Pacific",
    "N. America": "North America",
}
df["region"] = df["region"].replace(region_map)

# 5. Handle nulls in region -> "Unknown"
df["region"] = df["region"].fillna("Unknown")

# 6. Handle nulls in unit_price -> impute with category median
df["unit_price"] = df.groupby("category")["unit_price"].transform(
    lambda x: x.fillna(x.median())
)

# 7. Fix outliers: cap unit_price values that are >2x the category's 99th percentile
caps = df.groupby("category")["unit_price"].quantile(0.99) * 2
df["unit_price"] = df.apply(
    lambda row: min(row["unit_price"], caps[row["category"]]) if row["unit_price"] > caps[row["category"]] else row["unit_price"],
    axis=1
)

# 8. Add calculated columns
df["revenue"] = (df["unit_price"] * df["quantity"]).round(2)
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df["order_year"] = df["order_date"].dt.year
df["order_quarter"] = df["order_date"].dt.to_period("Q").astype(str)

df = df.sort_values("order_date").reset_index(drop=True)

print("\n=== AFTER CLEANING ===")
print(f"Total rows: {len(df)}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Null values:\n{df.isnull().sum()}")
print(f"Unique regions: {sorted(df['region'].unique())}")
print(f"Unique categories: {sorted(df['category'].unique())}")
print(f"\nDate range: {df['order_date'].min()} to {df['order_date'].max()}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")

df.to_csv("/home/claude/project1/data/cleaned_sales_data.csv", index=False)
print("\nSaved cleaned_sales_data.csv")
