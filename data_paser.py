#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd


# Filter A method 1
def filter_a_1(df):
    filter_a = df[
        (df['主要用途'] == '住家用') &
        (df['建物型態'].str.contains('住宅大樓')) &
        (df['總樓層數'].str.len() > 2) &
        (~df['總樓層數'].isin(['十一層', '十二層']))
    ]
    return filter_a


# Filter A method 2 (Not Good)
def filter_a_2(df):
    filter_a = df[(df['主要用途'] == '住家用') & (df['建物型態'].str.contains('住宅大樓'))]
    filter_a = filter_a[~filter_a['總樓層數'].isin(['十一層', '十二層'])]
    return filter_a


def main():
    # Load
    csv_list = ['a_lvr_land_a', 'b_lvr_land_a', 'e_lvr_land_a', 'f_lvr_land_a', 'h_lvr_land_a']
    df_list = [pd.read_csv(f'source/{i}.csv', skiprows=[1]) for i in csv_list]
    df_all = pd.concat(df_list)

    # Filter A
    # filter_a = filter_a_1(df_all)
    # filter_a = filter_a_2(df_all)
    # filter_a.to_csv('filter_a.csv', index=False)

    # Filter B
    data = {
        '總件數': [df_all.shape[0]],
        '總車位數': [df_all['交易筆棟數'].apply(lambda x: x.split('車位').pop()).astype(int).sum()],
        '平均總價元': [df_all['總價元'].mean()],
        '平均車位總價元': [df_all['車位總價元'].mean()]
    }
    filter_b = pd.DataFrame(data)
    filter_b.to_csv('filter_b.csv', index=False)
    return


if __name__ == '__main__':
    main()
