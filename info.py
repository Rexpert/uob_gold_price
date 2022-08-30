import pandas as pd

price = (
    pd
    .read_csv(r'.\data\basic_price.csv')
    .assign(
        TIME=lambda x: pd.to_datetime(x.TIME),
        scrape=lambda x: pd.to_datetime(x.scrape)
    )
)


(
    price
    .TIME
    .value_counts(sort=False)
    .reset_index(name='count')['index']
    .dt
    .date
    .value_counts(sort=False)
    .reset_index(name='count')
    .assign(
        index=lambda x: pd.to_datetime(x['index']),
        day=lambda x: x['index'].dt.day_name()
    )
)

#        index  count        day
# 0 2022-08-20      1   Saturday
# 1 2022-08-21      1     Sunday
# 2 2022-08-22      4     Monday
# 3 2022-08-23      2    Tuesday
# 4 2022-08-24      1  Wednesday
# 5 2022-08-25      1   Thursday
# 6 2022-08-26      3     Friday
# 7 2022-08-27      1   Saturday
# 8 2022-08-28      1     Sunday
# 9 2022-08-29      3     Monday

(
    price
    .TIME
    .value_counts(sort=False)
    .reset_index(name='count')
    .assign(
        hour=lambda x: x['index'].dt.ceil('h')
    )['hour']
    .dt
    .hour
    .value_counts()
    .sort_index()
)

# 8     4
# 10    6
# 11    1
# 12    1
# 13    2
# 14    1
# 15    1
# 16    2

# Scraping strategy #1:
# every weekday: every hour 0710-1810 UTC+8
# every weekend: 1159,2359 UTC+8

# -> Scraping strategy #2:
# every weekday: every hour 1000-1600 UTC+8
# every weekend: 0800 UTC+8
