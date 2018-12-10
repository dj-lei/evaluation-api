import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import os
os.environ['VALUATE_RUNTIME_ENVIRONMENT'] = 'LOCAL'

from valuate.predict.predict_api import Predict
from valuate.conf import global_settings as gl


if __name__ == "__main__":
    # predict = Predict()
    # test = pd.read_csv('/home/ml/PycharmProjects/evaluation-predict/api_valuate/explore/evaluation.csv')
    # # test = test.head(10)
    # test['buy'] = np.NaN
    # test['sell'] = np.NaN
    # for i in range(0, len(test)):
    #     try:
    #         city = test.loc[i, 'city']
    #         model_detail_slug = test.loc[i, 'model_detail_slug']
    #         reg_year = int(test.loc[i, 'year'])
    #         reg_month = int(test.loc[i, 'month'])
    #         deal_year = 2018
    #         deal_month = 8
    #         mile = test.loc[i, 'mile']
    #         print(i, model_detail_slug, city, deal_year, reg_year, mile)
    #         result = predict.predict(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month,
    #                                  deal_year=deal_year, deal_month=deal_month, mile=mile, ret_type='normal')
    #         test.loc[i, 'buy'] = float('%.2f' % (result.loc[(result['intent'] == 'buy'), 'excellent'].values[0] / 10000))
    #         test.loc[i, 'sell'] = float('%.2f' % (result.loc[(result['intent'] == 'sell'), 'excellent'].values[0] / 10000))
    #     except Exception:
    #         print(i)
    # test.to_csv('/home/ml/PycharmProjects/evaluation-predict/api_valuate/explore/man.csv', index=False)

    predict = Predict()
    # result = predict.predict(city='成都', model_detail_slug='8eb2866c5b_autotis', reg_year=2018, reg_month=3, deal_year=2018, deal_month=10, mile=0.5, ret_type='normal')
    # print(result)
    result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city='上海', model_detail_slug='96725_autotis', reg_year=2015, reg_month=6, deal_year=2018, deal_month=8, mile=4.5, ret_type='normal')
    print(result)
    # result = predict.residuals(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=8, mile=12, ret_type='normal')
    # print(result)
    # result = predict.history_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=8, mile=12, ret_type='normal')
    # print(result)
    # result = predict.future_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=8, mile=12, ret_type='normal')
    # print(result)
    # result = predict.load_valuated_cities()
    # print(result)
    # result = predict.load_valuated_models()
    # print(result)
    # result = predict.load_valuated_model_details()
    # print(result)上海
    # http://127.0.0.1:8001/api/evalapi/v1/evaluation?city=上海&model_detail_slug=105432_autotis&mile=3&online_year=2016&online_month=6
