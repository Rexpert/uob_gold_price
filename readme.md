# UOB Gold Price
This repo logs the gold price offered by UOB © [United Overseas Bank (Malaysia) Bhd](https://www.uob.com.my/). 

## Info
- There are 2 types of Gold Investment Account (GIA):
  - Gold Savings Account:
    - opening purchase: 20gm
    - minimum purchase: 5gm per transaction
  - Premier Gold Account
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
- |Column |Description                                           |
  |:------|:-----------------------------------------------------|
  |TIME   |The timestamp when UOB offer the gold at a given price|
  |SELLING|The Bank Selling Price (How much you buy the gold at) |
  |BUYING |The Bank Buying Price (How much you sell the gold at) |
  |scrape |The last timestamp before scrapper detect data changes|

## Visualization
- Click [here](https://rexpert.github.io/uob_gold_price/visualization.html) to visualize the GIA prices. 

## Disclaimer
- I do not own/create the data in UOB website.
- I do not represent UOB and not responsible for the accuracy of the pricing data in this repo. 
- Everyone are welcome to use the logged data in this repo, but the responsibility for the usage of data shall bound to themself, including any trading gain/loss in GIA. 
