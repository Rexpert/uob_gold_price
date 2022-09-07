# UOB Gold Price
This repo logs the gold price offered by UOB © [United Overseas Bank (Malaysia) Bhd](https://www.uob.com.my/). 

## Info
- There are 2 types of Gold Investment Account (GIA):
  - Gold Savings Account (GSA):
    - opening purchase: 20gm
    - minimum purchase: 5gm per transaction
  - Premier Gold Account (PGA):
    - opening purchase: 1kg 
    - minimum purchase: 1kg per transaction
  - More Info: [UOB Official GIA Product Page](https://www.uob.com.my/corporate/gmim/gmim-pga.page)
- The price is scrapped from [GIA Pricing Page](https://www.uob.com.my/online-rates/gold-prices.page).
- The scrapper are schedule as follows:
  - every weekday: every hour 1000-1600 UTC+8
  - every weekend: 0900 UTC+8
- Due to unstable schedule experienced with Github Action Scheduler, this scraping job are schedule through [cron-job.org](https://cron-job.org).

## Usage
- The pricing data is located in [`basic_price.csv`](data/basic_price.csv) and [`premium_price.csv`](data/premium_price.csv)
- Data description:
  | Column  | Description                                            |
  | :------ | :----------------------------------------------------- |
  | TIME    | The timestamp when UOB offer the gold at a given price |
  | SELLING | The Bank Selling Price (How much you buy the gold at)  |
  | BUYING  | The Bank Buying Price (How much you sell the gold at)  |
  | scrape  | The last timestamp before scrapper detect data changes |
- Example Usage: 
  ```Python
  import pandas as pd

  gsa_url = r'https://raw.githubusercontent.com/Rexpert/uob_gold_price/main/data/basic_price.csv'

  # Data Loading
  gsa_history = (
      pd
      .read_csv(gsa_url)
      # Parsing dates column
      .assign(
          TIME=lambda x: pd.to_datetime(x.TIME),
          scrape=lambda x: pd.to_datetime(x.scrape)
      )
  )

  # Data Exploration
  (
      gsa_history
      # Drop unused column
      .drop('scrape', axis=1)
      .set_index('TIME')
      # Change to daily frequency
      .resample('D')
      .last()
      # Fill missing value
      .interpolate(method='pad')
      # Finding the best day to buy gold 
      # i.e.: What time the gold price is selling at its minimum?
      .query('SELLING == SELLING.min()')
  )

  # >               SELLING  BUYING
  # > TIME
  # > 2022-09-02    248.1   244.0
  # > 2022-09-03    248.1   244.0
  # > 2022-09-04    248.1   244.0
  ```

## Visualization
- Click [here](https://rexpert.github.io/uob_gold_price/visualization.html) to visualize the GIA prices. 

## Disclaimer
- I do not own/create the data in UOB website.
- I do not represent UOB and not responsible for the accuracy of the pricing data in this repo. 
- Everyone are welcome to use the logged data in this repo, but the responsibility for the usage of data shall bound to themself, including any trading gain/loss in GIA. 

MIT &copy; [Rexpert](https://github.com/Rexpert) 2022
