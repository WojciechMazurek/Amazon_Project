import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("mock_keepa_data_improved.csv", parse_dates=['date'])

# Function to plot selected item(s)
def plot_items(item_ids):
    plt.figure(figsize=(14, 7))

    for item_id in item_ids:
        item_data = df[df['item_id'] == item_id]
        plt.plot(item_data['date'], item_data['price'], label=item_id)

    plt.title("Price History of Selected Items")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example usage
items_to_plot = ["ITEM_000", "ITEM_010","ITEM_011","ITEM_012","ITEM_012", "ITEM_020"]  # Change these as needed
plot_items(items_to_plot)
