估值模块使用说明
====

一.安装说明
-------
        第一次安装:pip3 install valuate-3.0.1.tar.gz<br>
        更新:pip3 install valuate-3.0.1.tar.gz -U<br>

二.接口功能
-------
### 1.预测接口
>功能：

        提供10类交易方式的价格估值，并分4种车况

>入参及条件：

        1.city(城市范围):生产表open_city内城市
        2.model_detail_slug(款型范围):生产表open_detail_model内price_bn非0&status为Y或A的款型
        3.reg_year(上牌年份):deal_year -  reg_year差值不能超过20年
        4.reg_month(上牌月份):1-12
        5.deal_year(交易年份):deal_year -  reg_year差值不能超过20年
        6.deal_month(交易月份):1-12
        7.mile(公里数):大于0(单位:万公里)

>用例：

        from valuate.predict.predict_api import Predict as api
        predict = api()
        result = predict.predict(city='绍兴', model_detail_slug='110071_autotis', reg_year=2017, reg_month=5, deal_year=2018, deal_month=2, mile=0.62)

>返回:

        [{'bad': 138140, 'excellent': 173518, 'intent': 'sell', 'fair': 149933, 'good': 168464}]

### 2.历史价格走势接口
>功能：

        提供当前车型参数前半年的价格预测走势

>入参及条件：

        1.city(城市范围):生产表open_city内城市
        2.model_detail_slug(款型范围):生产表open_detail_model内price_bn非0&status为Y或A的款型
        3.reg_year(上牌年份):deal_year -  reg_year差值不能超过20年
        4.reg_month(上牌月份):1-12
        5.deal_year(交易年份):deal_year -  reg_year差值不能超过20年
        6.deal_month(交易月份):1-12
        7.mile(公里数):大于0(单位:万公里)

>用例：

        from valuate.predict.predict_api import Predict as api
        predict = api()
        result = predict.history_price_trend(city='绍兴', model_detail_slug='110071_autotis', reg_year=2017, reg_month=5, deal_year=2018, deal_month=2, mile=0.62)

>返回:

        [{'-4': 191483, 'type': 'buy', '-3': 189907, '-1': 186794, '-2': 188344, '-5': 193072, '0': 185257, '-6': 194674}]

### 3.个人交易未来价格趋势接口
>功能：

        提供当前车型参数未来3年的价格预测

>入参及条件：

        1.city(城市范围):生产表open_city内城市
        2.model_detail_slug(款型范围):生产表open_detail_model内price_bn非0&status为Y或A的款型
        3.reg_year(上牌年份):deal_year -  reg_year差值不能超过20年
        4.reg_month(上牌月份):1-12
        5.deal_year(交易年份):deal_year -  reg_year差值不能超过20年
        6.deal_month(交易月份):1-12
        7.mile(公里数):大于0(单位:万公里)

>用例：

        from valuate.predict.predict_api import Predict as api
        predict = api()
        result = predict.future_price_trend(city='绍兴', model_detail_slug='110071_autotis', reg_year=2017, reg_month=5, deal_year=2018, deal_month=2, mile=0.62)

>返回:

        [{'12': 172108, '24': 146515, '0': 185257, 'type': 'buy', '36': 126087}]

### 4.异常处理
>异常类:

        ApiParamsValueError: 调用参数值异常
        ApiParamsTypeError: 调用参数类型异常

>用例:

        from valuate.exception.api_error import ApiParamsValueError
        from valuate.exception.api_error import ApiParamsTypeError
        from valuate.predict.predict_api import Predict as api

        try:
            predict = api()
            result = predict.predict_to_dict(city='123', model_detail_slug='123', reg_year=2018, reg_month=5, deal_year=2018, deal_month=2, mile=0.62)
        exceptApiParamsValueError as apve:
            print(apve.name, apve.value, apve.message)
        except ApiParamsTypeError as apte:
            print(apte.name, apte.value, apte.message)

>返回错说说明:

        1.未知城市错误:valuate.exception.api_error.ApiParamsValueError: ('city', '123', 'Unknown city!')
        2.未知款型错误:valuate.exception.api_error.ApiParamsValueError: ('model_detail_slug', '123', 'Unknown model!')
        3.使用时间至少1个月:valuate.exception.api_error.ApiParamsTypeError: ('deal_year,deal_month and reg_year,reg_month', 0, 'Use at least 1 month!')
        4.使用年限小于等于20年:valuate.exception.api_error.ApiParamsValueError: ('deal_year - reg_year', 21, 'The years of Forecast must be in 20 years!')

### 5.特征范围接口
>功能:

        提供可预测的城市,车型,款型

>用例:

        from valuate.predict.predict_api import Predict as api
        predict = api()
        result = predict.load_valuated_cities() #可预测城市
        result = predict.load_valuated_models() #可预测车型
        result = predict.load_valuated_model_details() #可预测款型

>返回:

        ['长春', '威海', '深圳', '怒江', '博尔塔拉', '昆明', '重庆']

### 6.未来12个月残值价格接口
>功能：

		提供当前车型参数未来12个月的残值预测

>入参及条件：

		1.city(城市范围):生产表open_city内城市
		2.model_detail_slug(款型范围):生产表open_detail_model内price_bn非0&status为Y或A的款型
		3.reg_year(上牌年份):deal_year -  reg_year差值不能超过20年
		4.reg_month(上牌月份):1-12
		5.deal_year(交易年份):deal_year -  reg_year差值不能超过20年
		6.deal_month(交易月份):1-12
		7.mile(公里数):大于0(单位:万公里)

>用例：

	    from valuate.predict.predict_api import Predict as api

	    predict = api()
	    result = predict.residuals(city='绍兴', model_detail_slug='110071_autotis', reg_year=2017, reg_month=5, deal_year=2018, deal_month=2, mile=0.62)

>返回:

        [{'4': 17842, '0': 22304, '9': 13498, 'intent': 'buy', 'condition': 'excellent', '2': 19949, '7': 15092, '3': 18866, '10': 12766, '11': 12073, '5': 16874, '1': 21094, '12': 11418, '8': 14273, '6': 15958}]