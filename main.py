import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("videos.csv")

print("\n--- All Videos ---")
print(df)

print("\n--- Views Column ---")
print(df["views"])

average_views = df["views"].mean()
print("\nAverage views:", average_views)

max_views = df["views"].max()
print("Max views:", max_views)

most_viewed = df.loc[df["views"].idxmax()]
print("\n--- Most Viewed Video ---")
print(most_viewed)

print("\nThe length of the table is", len(df))
print(f"Total videos: {len(df)}")

rounded_average = round(average_views, 2)
print(f"Average views rounded: {rounded_average}")

most_liked = df.loc[df["likes"].idxmax()]
print("\n--- Most Liked Video ---")
print(most_liked)

df["engagement_rate"] = ((df["likes"] + df["comments"]) / df["views"]) * 100
df["engagement_rate"] = df["engagement_rate"].round(2)

print("\n--- Table After Adding Engagement Rate ---")
print(df)

best_engagement = df.loc[df["engagement_rate"].idxmax()]
print("\n--- Best Engagement Video ---")
print(best_engagement)

df.to_csv("analysis_results.csv", index=False)
print("\nResults saved to analysis_results.csv")

plt.figure(figsize=(10, 6))
plt.bar(df["title"], df["views"])

plt.title("Views per YouTube Video")
plt.xlabel("Video Title")
plt.ylabel("Views")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig("views_chart.png")
print("Chart saved to views_chart.png")

plt.show()