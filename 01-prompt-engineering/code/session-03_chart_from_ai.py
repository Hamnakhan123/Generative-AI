"""Use case: an assistant was asked 'Turn this sales data into a chart'.
This is the kind of code it returns. We draw a text bar chart so it runs anywhere,
and also save a PNG with matplotlib."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sales = {"Jan": 120, "Feb": 95, "Mar": 160, "Apr": 140, "May": 210, "Jun": 185}
peak = max(sales, key=sales.get)
for month, v in sales.items():
    print(f"{month} | {'#' * (v // 10):<21} {v}{'  <- peak' if month == peak else ''}")
growth = (sales["Jun"] - sales["Jan"]) / sales["Jan"] * 100
print(f"\nGrowth Jan->Jun: {growth:.1f}%   Average: {sum(sales.values())/len(sales):.1f}")

plt.bar(sales.keys(), sales.values(), color="#FF6B1A")
plt.title("Monthly sales (units)")
plt.savefig("session-03_sales_chart.png", dpi=80)
print("Saved chart -> session-03_sales_chart.png")
