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
    try:
        new = (
            pd
            .read_csv(StringIO(txt))
        )
    except pd.errors.ParserError as e:
        raise ValueError(txt)
    new = (
        new
        .query('ITEM == @item')
        .loc[:, ['TIME', 'SELLING', 'BUYING']]
        .assign(TIME=lambda x: pd.to_datetime(x.TIME, format=r"%d/%m/%Y %H:%M"), scrape=now)
    )
    # Clean df
    new = (
        pd
        .concat([old, new], ignore_index=True)
        .assign(TIME=lambda x: pd.to_datetime(x.TIME))
        .groupby('TIME', as_index=False)
        .last()
    )
    return new


def compare(crit, timeframe, basic_price_now, premium_price_now, basic_price_crit):
    message = ''
    if (crit == 'min') and (basic_price_now < basic_price_crit):
        message = f'Bank Selling Price is now minimum in {timeframe}: GSA-RM{basic_price_now:.2f}/gm, PGA-RM{premium_price_now:.0f}/kg'
    elif (crit == 'max') and (basic_price_now > basic_price_crit):
        message = f'Bank Buying Price is now maximum in {timeframe}: GSA-RM{basic_price_now:.2f}/gm, PGA-RM{premium_price_now:.0f}/kg'
    return message


def alert(basic, basic_new, premium_new):
    basic = basic.assign(TIME=lambda x: pd.to_datetime(x.TIME))
    if basic.TIME.iloc[-1] != basic_new.TIME.iloc[-1]:
        basic_price_now = basic_new.SELLING.iloc[-1]
        premium_price_now = premium_new.SELLING.iloc[-1]
        min_messages = []
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=1)
        min_messages.append(compare('min', '1-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').SELLING.min()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
        min_messages.append(compare('min', '3-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').SELLING.min()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=6)
        min_messages.append(compare('min', '6-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').SELLING.min()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(years=1)
        min_messages.append(compare('min', '1-year ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').SELLING.min()))
        min_messages.append(compare('min', 'all-time ever', basic_price_now, premium_price_now, basic.SELLING.min()))

        basic_price_now = basic_new.BUYING.iloc[-1]
        premium_price_now = premium_new.BUYING.iloc[-1]
        max_messages = []
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=1)
        max_messages.append(compare('max', '1-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').BUYING.max()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
        max_messages.append(compare('max', '3-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').BUYING.max()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(months=6)
        max_messages.append(compare('max', '6-month ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').BUYING.max()))
        time_ago = pd.Timestamp.now() - pd.DateOffset(years=1)
        max_messages.append(compare('max', '1-year ago', basic_price_now, premium_price_now, basic.query('TIME >= @time_ago').BUYING.max()))
        max_messages.append(compare('max', 'all-time ever', basic_price_now, premium_price_now, basic.BUYING.max()))
        
        min_message_id = min_messages.index('') - 1 if '' in min_messages else 0
        max_message_id = max_messages.index('') - 1 if '' in max_messages else 0
        message = ''
        if min_message_id >= 0:
            message = min_messages[min_message_id-1]
        elif max_message_id >= 0:
            message = max_messages[max_message_id-1]
        if message != '':
            env_file = os.getenv('GITHUB_ENV')
            with open(env_file, 'a') as f:
                f.write(f'MESSAGE={message}')


if __name__ == '__main__':
    premium, basic = read_data()
    res = requests.get(r'https://www.uob.com.my/wsm/stayinformed.do?path=gia')
    basic_new = make_df(res.text, 'GOLD SAVINGS ACCOUNT', basic)
    basic_new.to_csv(basic_url, index=False)
    premium_new = make_df(res.text, 'PREMIER GOLD ACCOUNT', premium)
    premium_new.to_csv(premium_url, index=False)
    alert(basic, basic_new, premium_new)
