import os
from io import StringIO

import pandas as pd
import requests

premium_url = r'./data/premium_price.csv'
basic_url = r'./data/basic_price.csv'


def read_data():
    try:
        if os.path.getsize(premium_url) > 0:
            premium = pd.read_csv(premium_url)
            basic = pd.read_csv(basic_url)
            return premium, basic
    except FileNotFoundError:
        pass
    premium = pd.DataFrame(columns=['TIME', 'SELLING', 'BUYING', 'scrape'])
    basic = premium.copy()
    return premium, basic


def make_df(txt, item, old):
    now = pd.Timestamp.now(tz='Asia/Kuala_Lumpur')
    # Create new data
    new = (
        pd
        .read_csv(StringIO(txt))
        .query('ITEM == @item')
        .loc[:, ['TIME', 'SELLING', 'BUYING']]
        .assign(TIME=lambda x: pd.to_datetime(x.TIME, format=r"%d/%m/%Y %H:%M"), scrape=now)
    )
    # Clean df
    new = (
        pd
        .concat([old, new], ignore_index=True)
        .assign(TIME=lambda x: pd.to_datetime(x.TIME))
        .groupby('TIME')
        .last()
    )
    return new


if __name__ == '__main__':
    premium, basic = read_data()
    res = requests.get(r'https://www.uob.com.my/wsm/stayinformed.do?path=gia')
    basic_new = make_df(res.text, 'GOLD SAVINGS ACCOUNT', basic)
    basic_new.to_csv(basic_url)
    premium_new = make_df(res.text, 'PREMIER GOLD ACCOUNT', premium)
    premium_new.to_csv(premium_url)
