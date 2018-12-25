import sys
sys.path.append('../')
import pandas as pd
import numpy as np
import os
os.environ['VALUATE_RUNTIME_ENVIRONMENT'] = 'LOCAL'

from valuate.predict.predict_api import Predict
from valuate.conf import global_settings as gl


if __name__ == "__main__":
    predict = Predict()

    city = '苏州'
    model_detail_slug = 'kkk'
    reg_year = 2012
    reg_month = 2
    deal_year = 2018
    deal_month = 12
    mile = 12
    test = pd.DataFrame()
    print(model_detail_slug, city, deal_year, reg_year, mile)
    result = predict.predict(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
    test.loc[0, 'predict'] = str(result)
    result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
    test.loc[0, 'predict_with_condition'] = str(result)
    result = predict.history_price_trend(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
    test.loc[0, 'history_price_trend'] = str(result)
    result = predict.future_price_trend(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
    test.loc[0, 'future_price_trend'] = str(result)
    result = predict.residuals(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
    test.loc[0, 'residuals'] = str(result)

    test.to_csv('../tmp/predict_result.csv', index=False)

    # predict = Predict()
    # result = predict.predict(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city='苏州',model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.history_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.future_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.residuals(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)