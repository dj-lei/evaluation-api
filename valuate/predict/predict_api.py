from valuate.predict import *


def get_profit_rate(intent, popularity):
    """
    获取畅销系数
    """
    # 按畅销程度分级,各交易方式相比于标价的固定比例
    profits = gl.PROFITS
    profit = profits[popularity]
    # 计算各交易方式的价格相比于标价的固定比例
    if intent == 'sell':
        # 商家收购价相比加权平均价的比例
        profit_rate = 1 - profit[0] - profit[1]
    elif intent == 'buy':
        # 商家真实售价相比加权平均价的比例
        profit_rate = 1 - profit[0]
    elif intent == 'release':
        # 建议标价相比加权平均价的比例
        profit_rate = 1
    elif intent == 'private':
        # C2C价格相比加权平均价的比例
        profit_rate = 1 - profit[0] - profit[2]
    elif intent == 'lowest':
        # 最低成交价相比加权平均价的比例
        profit_rate = 1 - profit[0] - profit[1] - profit[3]
    elif intent == 'cpo':
        # 认证二手车价相比加权平均价的差异比例
        profit_rate = 1 - profit[0] - profit[8]
    elif intent == 'replace':
        # 4S店置换价相比加权平均价的比例
        profit_rate = 1 - profit[0] - profit[4]
    elif intent == 'auction':
        # 拍卖价相比加权平均价的差异比例
        profit_rate = 1 - profit[0] - profit[5]
    elif intent == 'avg-buy':
        # 平均买车价相比加权平均价的差异比例
        profit_rate = 1 - profit[0] - profit[7]
    elif intent == 'avg-sell':
        # 平均卖车价价相比加权平均价的差异比例
        profit_rate = 1 - profit[0] - profit[6]
    return profit_rate


def cal_intent_condition(prices, condition):
    """
    计算所有交易方式的4个级别车况价
    """
    if condition == 'excellent':
        df2 = pd.DataFrame([[1, 0.961, 0.913, 0.855]])
    elif condition == 'good':
        df2 = pd.DataFrame([gl.CAR_CONDITION_COEFFICIENT_VALUES])
    elif condition == 'fair':
        df2 = pd.DataFrame([[1.094, 1.052, 1, 0.936]])
    else:
        df2 = pd.DataFrame([[1.168, 1.123, 1.067, 1]])
    df1 = pd.DataFrame(prices)
    all_map = df1.dot(df2)
    all_map.columns = ['excellent', 'good', 'fair', 'bad']
    all_map['intent'] = pd.Series(gl.INTENT_TYPE).values
    all_map = all_map.loc[:, ['intent', 'excellent', 'good', 'fair', 'bad']]
    all_map[['excellent', 'good', 'fair', 'bad']] = all_map[['excellent', 'good', 'fair', 'bad']].astype(int)
    all_map['condition'] = condition
    return all_map


def process_profit_rate(df):
    """
    畅销系数处理
    """
    return get_profit_rate(df['intent'], df['popularity'])


def process_buy_profit_rate(df):
    """
    畅销系数处理
    """
    return get_profit_rate(df['intent_source'], df['popularity'])


def process_unreasonable_history_price(data, nums):
    """
    处理不合理历史价格趋势
    """
    if nums == 0:
        return data

    temp = data[1:]
    temp.sort()
    for i, value in enumerate(temp):
        data[i+1] = temp[i]

    for i in range(0, nums):
        rate = (data[i + 1] - data[i]) / data[i + 1]
        if (data[i] >= data[i + 1]) | (0.003 > rate) | (0.0157 < rate):
            data[i + 1] = int(data[i] * 1.004)

    return data


def predict_from_db_history(data, hedge, month, times):
    """
    从生产库查询预测
    """
    # 月份与预测价格比率
    month_rate_normal = {'1': 0.036, '2': 0.028, '3': 0.02, '4': 0.012, '5': 0.004, '6': -0.004,
                  '7': -0.004, '8': -0.007, '9': -0.015, '10': -0.021, '11': -0.029, '12': -0.037}
    month_rate = pd.DataFrame(pd.Series([1.036, 1.028, 1.02, 1.012, 1.004, 0.996, 0.996, 0.993, 0.985, 0.979, 0.971, 0.963]), columns=['rate'])
    month_rate['rate'] = month_rate['rate'] - month_rate_normal[str(month)]
    # 组合结果
    used_years = data.loc[0, 'used_years']
    condition = data.loc[0, 'condition']
    buy_price = data.loc[1, condition]
    priviate_price = data.loc[3, condition]
    sell_price = data.loc[0, condition]

    # 查找对应值
    if used_years <= 1:
        if times < month:
            dealer_price = [int(rate * buy_price) for rate in month_rate.rate.values]
            dealer_price = dealer_price[month-times:month]
            dealer_price.reverse()
            cpersonal_price = [int(rate * priviate_price) for rate in month_rate.rate.values]
            cpersonal_price = cpersonal_price[month-times:month]
            cpersonal_price.reverse()
            sell_price = [int(rate * sell_price) for rate in month_rate.rate.values]
            sell_price = sell_price[month-times:month]
            sell_price.reverse()
        else:
            dealer_price = [int(rate * buy_price) for rate in month_rate.rate.values]
            dealer_price = dealer_price[0:month]
            dealer_price.reverse()
            cpersonal_price = [int(rate * priviate_price) for rate in month_rate.rate.values]
            cpersonal_price = cpersonal_price[0:month]
            cpersonal_price.reverse()
            sell_price = [int(rate * sell_price) for rate in month_rate.rate.values]
            sell_price = sell_price[0:month]
            sell_price.reverse()
            for i in range(0, times-month):
                dealer_price.append(dealer_price[month-1])
                cpersonal_price.append(cpersonal_price[month-1])
                sell_price.append(sell_price[month-1])
    else:
        cur_dealer_price = [int(rate * buy_price) for rate in month_rate.rate.values]
        prev_dealer_price = [int(rate * (buy_price/hedge[used_years-1]*hedge[used_years-2])) for rate in month_rate.rate.values]
        prev_dealer_price.extend(cur_dealer_price)
        dealer_price = prev_dealer_price[month + 12 - times:month + 12]
        dealer_price.reverse()

        cur_cpersonal_price = [int(rate * priviate_price) for rate in month_rate.rate.values]
        prev_cpersonal_price = [int(rate * (priviate_price/hedge[used_years-1]*hedge[used_years-2])) for rate in month_rate.rate.values]
        prev_cpersonal_price.extend(cur_cpersonal_price)
        cpersonal_price = prev_cpersonal_price[month + 12 - times:month + 12]
        cpersonal_price.reverse()

        cur_sell_price = [int(rate * sell_price) for rate in month_rate.rate.values]
        prev_sell_price = [int(rate * (sell_price/hedge[used_years-1]*hedge[used_years-2])) for rate in month_rate.rate.values]
        prev_sell_price.extend(cur_sell_price)
        sell_price = prev_sell_price[month + 12 - times:month + 12]
        sell_price.reverse()
    return dealer_price, cpersonal_price, sell_price


def check_params_value(reg_year, reg_month, deal_year, deal_month, mile):
    """
    校验参数
    """
    # 校验mile
    if not ((isinstance(mile, int)) | (isinstance(mile, float))):
        raise ApiParamsTypeError('mile', mile, 'Mile must be int or float!')
    elif mile < 0:
        raise ApiParamsValueError('mile', mile, 'Mile must be greater than zero!')
    # 校验month
    if (not isinstance(reg_month, int)) or (not (1 <= reg_month <= 12)):
        raise ApiParamsTypeError('reg_month', reg_month, 'reg_month must be int and in [1,12]!')
    if (not isinstance(deal_month, int)) or (not (1 <= deal_month <= 12)):
        raise ApiParamsTypeError('deal_month', deal_month, 'deal_month must be int and in [1,12]!')
    # 校验year
    if not isinstance(reg_year, int):
        raise ApiParamsTypeError('reg_year', reg_year, 'reg_year must be int!')
    if not isinstance(deal_year, int):
        raise ApiParamsTypeError('deal_year', deal_year, 'deal_year must be int!')
    if (deal_year - reg_year) > 20:
        raise ApiParamsValueError('deal_year - reg_year', deal_year - reg_year, 'The years of Forecast must be in 20 years!')
    # 校验时间差至少使用1个月
    if (deal_year < reg_year) | ((deal_year == reg_year) & (deal_month < reg_month)):
        raise ApiParamsTypeError('deal_year,deal_month and reg_year,reg_month', 0, 'Use at least 1 month!')


def df_process_mile(price, used_years, mile):
    """
    mile处理
    """
    # 正常行驶的车辆以一年2.5万公里为正常基数，低于2.5万公里的价格的浮动在+3.5%以内
    # 大于2.5万公里的若每年的平均行驶里程大于2.5万公里小于5万公里价格浮动在-3.5-7.5%
    # 若年平均形式里程大于5万公里及以上影响价格在-7.5-12.5%之间
    mile_per_year = mile / used_years
    if mile_per_year <= gl.MILE_THRESHOLD_2_5:
        return price + 0.0061 * (1 - mile_per_year/gl.MILE_THRESHOLD_2_5) * price
    elif gl.MILE_THRESHOLD_2_5 < mile_per_year <= gl.MILE_THRESHOLD_5:
        return price - (0.04 * (mile_per_year/gl.MILE_THRESHOLD_5)+0.035) * price
    elif gl.MILE_THRESHOLD_5 < mile_per_year <= gl.MILE_THRESHOLD_10:
        return price - (0.05 * (mile_per_year/gl.MILE_THRESHOLD_5)+0.075) * price
    else:
        return price - 0.125 * price


def df_process_reasonable_hedge(df):
    """
    人工处理非合理保值率
    """
    # 查找标价的异常节点
    result = ast.literal_eval(df['predict_hedge'])
    normal_used_years = 1 if (datetime.datetime.now().year - df['year']) == 0 else (datetime.datetime.now().year - df['year'])
    # 原则上每年的贬值率在4%-10%之间
    for i in range(normal_used_years-1, 0, -1):
        if (result[i - 1] - result[i]) > 0.1:
            result[i - 1] = result[i] + 0.07
        elif (result[i - 1] - result[i]) < 0.025:
            result[i - 1] = result[i] + 0.04
        else:
            result[i - 1] = result[i - 1]

    for i in range(normal_used_years-1, 19):
        if (result[i] - result[i+1]) > 0.1:
            result[i + 1] = result[i] - 0.07
        elif (result[i] - result[i+1]) < 0.025:
            result[i + 1] = result[i] - 0.04
        else:
            result[i + 1] = result[i + 1]
    result = [0.01 if j < 0.02 else j for j in result]
    return result


def df_process_hedge(df):
    """
    查找保值率
    """
    # 保值率处理
    result = df_process_reasonable_hedge(df)
    # 上牌月份影响因子
    if df['year_flag'] != 0:
        reg_month_rate = [0.9924, 0.9942, 0.9952, 0.9972, 0.9984, 0.9992, 0.9995, 1.0006, 1.0007, 1.0017, 1.0022, 1.0043]
    else:
        reg_month_rate = [1.0049, 1.0055, 1.0061, 1.0067, 1.0073, 1.0079, 1.0085, 1.0091, 1.0097, 1.0103, 1.0109, 1.0115]

    price = int(result[df['used_years']-1] * df['price_bn'])
    price = price * reg_month_rate[df['reg_month'] - 1]
    return pd.Series([df_process_mile(price, df['used_years'], df['mile']), str(result)])


def cal_residuals(price, next_year):
    """
    计算12个月内残值
    """
    month_rate = [0, 0.08, 0.165, 0.245, 0.33, 0.415, 0.5, 0.585, 0.67, 0.755, 0.835, 0.92, 1]
    diff = price - next_year
    residuals = [int(price - month_rate[i]*diff) for i in range(0, 13)]
    return residuals


def cal_score(df):
    """
    计算车况评级每一项得分
    """
    if df['number'] == 0:
        return df['number_0']
    if df['number'] == 1:
        return df['number_1']
    if df['number'] == 2:
        return df['number_2']
    if df['number'] == 3:
        return df['number_3']


def cal_final_score_and_condition(data, cur_condition, mile_per_year):
    """
    计算最终得分和车况
    """
    score = 0
    inner = data.loc[(data['position'] == '内饰'), 'score'].values[0]
    outter = data.loc[(data['position'] == '外观'), 'score'].values[0]
    structure = data.loc[(data['position'] == '机械结构'), 'score'].values[0]
    reinforce = data.loc[(data['position'] == '车辆加强件'), 'score'].values[0]
    skeleton = data.loc[(data['position'] == '车辆骨架或事故'), 'score'].values[0]
    if skeleton > 35:
        score = score + 35
    score = score + skeleton
    if outter > 20:
        score = score + 20
    score = score + outter
    if inner > 15:
        score = score + 15
    score = score + inner
    if reinforce > 10:
        score = score + 10
    score = score + reinforce
    if structure > 20:
        score = score + 20
    score = score + structure

    if mile_per_year > 3:
        score = score + 5

    final_score = 100 - score
    if 92 <= final_score <= 100:
        evalute_condition = 0
    elif 78 <= final_score <= 91:
        evalute_condition = 1
    elif 65 <= final_score <= 77:
        evalute_condition = 2
    elif final_score < 65:
        evalute_condition = 3

    if evalute_condition > cur_condition:
        return gl.CAR_CONDITION[evalute_condition]
    return gl.CAR_CONDITION[cur_condition]


class Predict(object):

    def __init__(self):
        """
        加载各类匹配表和模型
        """
        self.result = []
        self.valuate_model = []

    def add_process_intent(self, data):
        """
        根据交易方式修正预测值
        """
        # 组合结果
        data = data.to_dict('records')
        self.result = result_map.copy()
        self.result.loc[(self.result['intent'] == 'release'), 'predict_price'] = data[0]['price']
        self.result['predict_price'] = self.result['predict_price'].fillna(data[0]['price'])

        self.result['popularity'] = data[0]['popularity']
        self.result['profit_rate'] = self.result.apply(process_profit_rate, axis=1)
        self.result['buy_profit_rate'] = self.result.apply(process_buy_profit_rate, axis=1)
        self.result['predict_price'] = self.result['predict_price'] / self.result['buy_profit_rate']
        self.result['predict_price'] = self.result['profit_rate'] * self.result['predict_price']

        # 车况判断两年以内优秀,8-3年良好,9-11年一般,12年以上较差
        if data[0]['used_years'] <= 2:
            condition = 'excellent'
        elif 2 < data[0]['used_years'] <= 8:
            condition = 'good'
        elif 8 < data[0]['used_years'] <= 11:
            condition = 'fair'
        elif 12 < data[0]['used_years']:
            condition = 'bad'
        # 计算所有交易类型
        self.result = cal_intent_condition(self.result.predict_price.values, condition)

    def generate_residuals(self, data, hedge):
        """
        生成残值
        """
        # 组合结果
        # 组合结果
        used_years = data.loc[0, 'used_years']
        buy_price = data.loc[1, 'good']
        priviate_price = data.loc[3, 'good']
        sell_price = data.loc[0, 'good']
        hedge.extend([0.008, 0.006, 0.002])

        df2 = pd.DataFrame(gl.CAR_CONDITION_COEFFICIENT_VALUES)
        df1 = pd.DataFrame([cal_residuals(buy_price, int(buy_price/hedge[used_years-1]*hedge[used_years]))])
        buy_residuals = df2.dot(df1)
        buy_residuals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        buy_residuals['intent'] = 'buy'
        buy_residuals['condition'] = pd.Series(['excellent', 'good', 'fair', 'bad'])

        df1 = pd.DataFrame([cal_residuals(priviate_price, int(priviate_price/hedge[used_years-1]*hedge[used_years]))])
        cpersonal_residuals = df2.dot(df1)
        cpersonal_residuals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        cpersonal_residuals['intent'] = 'private'
        cpersonal_residuals['condition'] = pd.Series(['excellent', 'good', 'fair', 'bad'])

        df1 = pd.DataFrame([cal_residuals(sell_price, int(sell_price/hedge[used_years-1]*hedge[used_years]))])
        sell_residuals = df2.dot(df1)
        sell_residuals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        sell_residuals['intent'] = 'sell'
        sell_residuals['condition'] = pd.Series(['excellent', 'good', 'fair', 'bad'])

        self.result = pd.DataFrame()
        self.result = self.result.append(buy_residuals)
        self.result = self.result.append(cpersonal_residuals)
        self.result = self.result.append(sell_residuals)
        self.result[['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']] = self.result[['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']].astype(int)
        self.result.reset_index(inplace=True, drop=True)

    def generate_residuals_future(self, data, hedge):
        """
        生成残值
        """
        # 组合结果
        used_years = data.loc[0, 'used_years']
        condition = data.loc[0, 'condition']
        buy_price = data.loc[1, condition]
        priviate_price = data.loc[3, condition]
        sell_price = data.loc[0, condition]
        hedge.extend([0.008, 0.006, 0.002])

        df1 = pd.DataFrame([[buy_price, int(buy_price/hedge[used_years-1]*hedge[used_years]),int(buy_price/hedge[used_years-1]*hedge[used_years+1]),int(buy_price/hedge[used_years-1]*hedge[used_years+2])]])
        df1.columns = ['0', '12', '24', '36']
        df1['type'] = 'buy'

        df2 = pd.DataFrame([[priviate_price, int(priviate_price/hedge[used_years-1]*hedge[used_years]),int(priviate_price/hedge[used_years-1]*hedge[used_years+1]),int(priviate_price/hedge[used_years-1]*hedge[used_years+2])]])
        df2.columns = ['0', '12', '24', '36']
        df2['type'] = 'private'

        df3 = pd.DataFrame([[sell_price, int(sell_price/hedge[used_years-1]*hedge[used_years]),int(sell_price/hedge[used_years-1]*hedge[used_years+1]),int(sell_price/hedge[used_years-1]*hedge[used_years+2])]])
        df3.columns = ['0', '12', '24', '36']
        df3['type'] = 'sell'

        self.result = df1.append(df2)
        self.result = self.result.append(df3)

    def predict(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        预测返回
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)

        # 转换编码
        used_years = 1 if (deal_year - reg_year) == 0 else deal_year - reg_year

        # 查询对应条件预测
        self.result = db_operate.query_valuate(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        self.result['reg_month'] = reg_month
        self.result['used_years'] = used_years
        self.result['year_flag'] = deal_year - reg_year
        self.result['mile'] = mile

        if self.result.loc[0, 'year'] > datetime.datetime.now().year:
            self.result['year'] = datetime.datetime.now().year

        # 预测返回保值率
        self.result[['price', 'hedge']] = self.result.apply(df_process_hedge, axis=1)

        # 根据交易方式修正预测值
        self.add_process_intent(self.result)

        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def predict_with_condition(self, condition_desc=None, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        预测估值和车况定级
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)

        # 转换编码
        used_years = 1 if (deal_year - reg_year) == 0 else deal_year - reg_year

        # 查询对应条件预测
        self.result = db_operate.query_valuate(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        self.result['reg_month'] = reg_month
        self.result['used_years'] = used_years
        self.result['year_flag'] = deal_year - reg_year
        self.result['mile'] = mile

        if self.result.loc[0, 'year'] > datetime.datetime.now().year:
            self.result['year'] = datetime.datetime.now().year

        # 预测返回保值率
        self.result[['price', 'hedge']] = self.result.apply(df_process_hedge, axis=1)

        # 根据交易方式修正预测值
        self.add_process_intent(self.result)

        # 车况评级
        condition_valuate = pd.read_json(condition_desc, orient='records')
        condition_valuate = condition_evaluate_map.merge(condition_valuate, how='left', on=['item'])
        condition_valuate['score'] = condition_valuate.apply(cal_score, axis=1)
        condition_valuate = condition_valuate.groupby(['position'])['score'].sum().reset_index()
        condition = cal_final_score_and_condition(condition_valuate, gl.CAR_CONDITION.index(self.result.loc[0, 'condition']), mile/used_years)
        self.result['condition'] = condition

        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def residuals(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        残值返回
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)

        # 转换编码
        used_years = 1 if (deal_year - reg_year) == 0 else deal_year - reg_year

        # 查询对应条件预测
        self.result = db_operate.query_valuate(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        self.result['reg_month'] = reg_month
        self.result['used_years'] = used_years
        self.result['year_flag'] = deal_year - reg_year
        self.result['mile'] = mile

        # 预测返回保值率
        self.result[['price', 'hedge']] = self.result.apply(df_process_hedge, axis=1)
        hedge = ast.literal_eval(self.result.loc[0, 'hedge'])
        # 根据交易方式修正预测值
        self.add_process_intent(self.result)
        self.result['used_years'] = used_years
        # 根据交易生成残值
        self.generate_residuals(self.result, hedge)

        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def history_price_trend(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        计算历史价格趋势
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)
        used_months = (deal_year - reg_year)*12 + deal_month - reg_month
        used_months = 1 if used_months <= 0 else used_months
        # 计算时间
        times_str = ['0', '-1', '-2', '-3', '-4', '-5', '-6']
        nums = 6
        if used_months <= 6:
            times_str = []
            nums = used_months-1
            for i in range(0, nums+1):
                times_str.append(str(-i))
        # 转换编码
        used_years = 1 if (deal_year - reg_year) == 0 else deal_year - reg_year

        # 查询对应条件预测
        self.result = db_operate.query_valuate(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        self.result['reg_month'] = reg_month
        self.result['used_years'] = used_years
        self.result['year_flag'] = deal_year - reg_year
        self.result['mile'] = mile

        # 预测返回保值率
        self.result[['price', 'hedge']] = self.result.apply(df_process_hedge, axis=1)
        hedge = ast.literal_eval(self.result.loc[0, 'hedge'])
        # 根据交易方式修正预测值
        self.add_process_intent(self.result)
        condition = self.result.loc[0, 'condition']
        self.result['used_years'] = used_years

        # 预测返回保值率 data, hedge, month, times
        data_buy, data_private, data_sell = predict_from_db_history(self.result, hedge, deal_month, len(times_str))
        # 处理异常值
        data_buy = process_unreasonable_history_price(data_buy, nums)
        data_sell = process_unreasonable_history_price(data_sell, nums)
        data_private = process_unreasonable_history_price(data_private, nums)
        if data_private[0] > data_buy[0]:
            data_private = data_buy
        result_b_2_c = pd.DataFrame([data_buy], columns=times_str)
        result_b_2_c['type'] = 'buy'
        result_c_2_b = pd.DataFrame([data_sell], columns=times_str)
        result_c_2_b['type'] = 'sell'
        result_c_2_c = pd.DataFrame([data_private], columns=times_str)
        result_c_2_c['type'] = 'private'

        self.result = result_b_2_c.append(result_c_2_b, ignore_index=True)
        self.result = self.result.append(result_c_2_c, ignore_index=True)
        self.result['condition'] = condition
        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def future_price_trend(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        计算未来价格趋势
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)

        # 转换编码
        used_years = 1 if (deal_year - reg_year) == 0 else deal_year - reg_year

        # 查询对应条件预测
        self.result = db_operate.query_valuate(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        self.result['reg_month'] = reg_month
        self.result['used_years'] = used_years
        self.result['year_flag'] = deal_year - reg_year
        self.result['mile'] = mile

        # 预测返回保值率
        self.result[['price', 'hedge']] = self.result.apply(df_process_hedge, axis=1)
        hedge = ast.literal_eval(self.result.loc[0, 'hedge'])
        # 根据交易方式修正预测值
        self.add_process_intent(self.result)
        condition = self.result.loc[0, 'condition']
        self.result['used_years'] = used_years
        # 根据交易生成残值
        self.generate_residuals_future(self.result, hedge)
        self.result['condition'] = condition
        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def load_valuated_cities(self):
        """
        可预测城市
        """
        return db_operate.query_valuated_cities()

    def load_valuated_models(self):
        """
        可预测车型
        """
        return db_operate.query_valuated_models()

    def load_valuated_model_details(self):
        """
        可预测款型
        """
        return db_operate.query_valuated_model_details()

