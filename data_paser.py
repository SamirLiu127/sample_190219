#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd


def main():
    csv_list = ['a_lvr_land_a', 'b_lvr_land_a', 'e_lvr_land_a', 'f_lvr_land_a', 'h_lvr_land_a']
    df_list = [pd.read_csv(f'source/{i}.csv', skiprows=[1]) for i in csv_list]
    df_all = pd.concat(df_list)

    filter_a = df_all[
        (df_all['主要用途'] == '住家用') &
        # (df_all['建築型態'] == '') &
        (len(df_all['總樓層數']) > 2) &
        (df_all['總樓層數'] not in ['十一層', '十二層'])
    ]
    return


if __name__ == '__main__':
    main()
