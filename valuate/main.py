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
    result = predict.predict(city='成都', model_detail_slug='2468_ah', reg_year=2006, reg_month=2, deal_year=2018, deal_month=12, mile=24, ret_type='normal')
    print(result)
    # result = predict.predict_with_condition(condition_desc=gl.CONDITION_JSON, city='苏州',model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.history_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.future_price_trend(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2, deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)
    # result = predict.residuals(city='苏州', model_detail_slug='m14877_ba', reg_year=2012, reg_month=2,deal_year=2018, deal_month=12, mile=12, ret_type='normal')
    # print(result)