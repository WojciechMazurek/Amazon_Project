import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, date

# Parameters
num_items = 100
today = datetime.now()


# Generate fixed and calculated U.S. holidays
def generate_us_holidays(start_year, end_year):
    fixed_holidays = [(1, 1), (7, 4), (12, 25)]
    holidays = set()
    for year in range(start_year, end_year + 1):
        for month, day in fixed_holidays:
            holidays.add(date(year, month, day))
        # 4th Thursday of November
        nov_first = date(year, 11, 1)
        weekday = nov_first.weekday()
        days_to_thursday = (3 - weekday + 7) % 7
        thanksgiving = nov_first + timedelta(days=days_to_thursday + 21)
        holidays.add(thanksgiving)
    return holidays

us_holidays = generate_us_holidays(today.year - 8, today.year)

# Generate realistic price history per item
def generate_price_history(item_id):
    #randomly lets the item be 1-8 years old
    years_back = random.randint(1, 8)
    start_date = today - timedelta(days=years_back * 365 + random.randint(0, 364))
    num_days = (today - start_date).days
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    base_price = round(random.uniform(5, 500), 2)
    is_premium = base_price > 250
    current_price = base_price
    holiday_discount_active = False
    holiday_discount_end_date = None

    price_history = []

    for i, current_date in enumerate(dates):
        date_only = current_date.date()

        decay_factor = 1 - (i / len(dates)) * 0.25  # up to 25% total decay over the date range
        effective_base_price = base_price * decay_factor

        #if it is a holiday give a sale (10% chance for premium items, 80% for non premium)
        if date_only in us_holidays and ((not is_premium and random.random() < 0.8) or random.random() < 0.1):
            discount = random.uniform(0.1, 0.25)
            current_price = round(effective_base_price * (1 - discount), 2)
            holiday_discount_active = True
            holiday_discount_end_date = current_date + timedelta(days=random.randint(1, 14))

        #if the holiday period has ended return price to normal (10% chance to adjust base price by 5 %)
        elif holiday_discount_active and current_date >= holiday_discount_end_date:
            current_price = effective_base_price
            if random.random() < 0.1:
                discount = random.uniform(-0.05, 0.05)
                current_price = round(effective_base_price * (1 - discount), 2)
                #base_price =  current_price
            holiday_discount_active = False
            holiday_discount_end_date = None
        #potential random price changes from current price
        elif (random.random() < 0.01) and not is_premium:
            change = 1 + np.random.normal(-0.02, 0.01)
            current_price *= change
            current_price = round(min(max(current_price, 3.0), effective_base_price * 1.2), 2)
        # .1% chance to return to base price
        elif random.random() < 0.0001:
            current_price = effective_base_price

        price_history.append(current_price)


    return pd.DataFrame({
        'item_id': item_id,
        'date': dates,
        'price': price_history
    })

# Generate dataset and save
all_data = pd.concat([generate_price_history(f"ITEM_{i:03}") for i in range(num_items)], ignore_index=True)
all_data.to_csv("mock_keepa_data_improved.csv", index=False)
print("Saved to mock_keepa_data_improved.csv")
