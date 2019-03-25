import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import os
import datetime
os.environ['VALUATE_RUNTIME_ENVIRONMENT'] = 'LOCAL'

from valuate.predict.predict_api import Predict
from valuate.conf import global_settings as gl


if __name__ == "__main__":
    # verify = pd.read_csv('./wait_predict.csv')
    # verify['new_sell'] = np.NaN
    # verify['new_buy'] = np.NaN
    #
    # content = input("是否重新开始验证(y/n):")
    # if content == 'y':
    #     data = pd.DataFrame([], columns=verify.columns)
    #     data.to_csv('./predict_result.csv', index=False)
    # else:
    #     predict_result = pd.read_csv('./wait_predict.csv')
    #     verify = verify.loc[~(verify['detail_model_slug'].isin(list(predict_result.detail_model_slug.values))),
    #              :].reset_index(drop=True)
    #
    # predict = Predict()
    # for i in range(0, len(verify)):
    #     data = pd.DataFrame([], columns=verify.columns)
    #     data.loc[0, :] = verify.loc[i, :].copy()
    #     city = verify.loc[i, 'city']
    #     model_detail_slug = verify.loc[i, 'detail_model_slug']
    #     reg_year = int(verify.loc[i, 'year'])
    #     reg_month = int(verify.loc[i, 'month'])
    #     deal_year = datetime.datetime.now().year
    #     deal_month = datetime.datetime.now().month
    #     mile = float(verify.loc[i, 'mile'])
    #
    #     print(i, model_detail_slug, city, reg_year, deal_year, mile)
    #     result = predict.predict(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month,
    #                              deal_year=deal_year, deal_month=deal_month, mile=mile, ret_type='normal')
    #     condition = result.loc[0, 'condition']
    #     data['new_sell'] = result.loc[(result['intent'] == 'sell'), condition].values[0]
    #     data['new_buy'] = result.loc[(result['intent'] == 'buy'), condition].values[0]
    #     data.to_csv('./predict_result.csv', header=False, mode='a', index=False)


    predict = Predict()
    result = predict.predict(city='成都', model_detail_slug='13746_ah', reg_year=2013, reg_month=2, deal_year=2019, deal_month=3, mile=4, ret_type='normal')
    print(result)
    # result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city='苏州',model_detail_slug='m14877_ba', reg_year=2018, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.history_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.future_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.residuals(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)