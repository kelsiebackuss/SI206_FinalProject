import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the database
conn = sqlite3.connect("mental_health_weather.db")
df = pd.read_sql_query("SELECT * FROM JoinedData", conn)
conn.close()

# Format date and UV ranges
df["date"] = pd.to_datetime(df["date"])
df["uv_range"] = pd.cut(
    df["uv"], 
    bins=[-1, 2, 5, 7, 10], 
    labels=["Low", "Moderate", "High", "Very High"]
)

sns.set(style="whitegrid")

# 1. Bar chart: Average Reddit Score by UV Range
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="uv_range", y="score", errorbar=None)
plt.title("Average Reddit Score by UV Range")
plt.xlabel("UV Range")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("avg_score_uv.png")
plt.close()


# 2. Pie chart: Post Distribution by UV Range
uv_counts = df["uv_range"].value_counts().sort_index()
plt.figure(figsize=(7, 7))
colors = sns.color_palette("pastel")[0:4]
plt.pie(uv_counts, labels=uv_counts.index, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("Distribution of Reddit Posts by UV Range")
plt.savefig("uv_post_piechart.png")
plt.close()

# 3. Heatmap: Average Score by City and UV Range
heatmap_data = df.pivot_table(values="score", index="city", columns="uv_range", aggfunc="mean")

plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".1f", linewidths=.5)
plt.title("Average Reddit Score by City and UV Range")
plt.xlabel("UV Range")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("score_heatmap.png")
plt.close()

# 4. Line Chart: Post Count Over Time
post_volume = df.groupby("date")["id"].count()

plt.figure(figsize=(10, 6))
post_volume.plot(kind="line", marker="o")
plt.title("Reddit Post Volume Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Posts")
plt.tight_layout()
plt.savefig("post_volume_linechart.png")
plt.close()

print(" All 4 visualizations saved: avg_score_uv.png, uv_post_piechart.png, score_heatmap.png, post_volume_linechart.png")


