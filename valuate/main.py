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
    # test = pd.read_csv('../tmp/wait_predict.csv')
    # test['buy_price'] = np.NaN
    # for i in range(0, len(test)):
    #     try:
    #         city = test.loc[i, 'city']
    #         detail_slug = int(test.loc[i, 'detail_slug'])
    #         reg_year = int(test.loc[i, 'year'])
    #         reg_month = int(test.loc[i, 'month'])
    #         deal_year = 2018
    #         deal_month = 12
    #         mile = test.loc[i, 'mile']
    #         print(i, detail_slug, city, deal_year, reg_year, mile)
    #         result = predict.verify(city=city, detail_slug=detail_slug, reg_year=reg_year, reg_month=reg_month,deal_year=deal_year, deal_month=deal_month, mile=mile)
    #         test.loc[i, 'buy_price'] = result
    #     except Exception:
    #         print(i)
    # test = test.sort_values(by=['brand_slug', 'model_slug', 'online_year', 'price_bn'])
    # test.to_csv('../tmp/predict_result.csv', index=False)

    predict = Predict()
    result = predict.predict(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    print(result)
    result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city='苏州',model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    print(result)
    result = predict.history_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    print(result)
    result = predict.future_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    print(result)
    result = predict.residuals(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    print(result)