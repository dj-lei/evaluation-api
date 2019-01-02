from valuate.predict import *


def get_profit_rate(intent, popularity, price):
    """
    获取畅销系数
    """
    # 按畅销程度分级,各交易方式相比于标价的固定比例
    profits = gl.PROFITS
    profit = profits[popularity]
    rate = 0.48 * math.e ** (-0.304 * (price * (1 - profit[0]) / 10000)) + 0.08

    # 计算各交易方式的价格相比于标价的固定比例
    if intent == 'sell':
        # 商家收购价相比加权平均价的比例
        # profit_rate = 1 - profit[0] - profit[1]
        profit_rate = (1 - profit[0])*(1-rate)
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
        # profit_rate = 1 - profit[0] - profit[1] - profit[3]
        profit_rate = (1 - profit[0]) * (1 - rate) - profit[3]
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


def process_profit_rate(df, column_name, price):
    """
    畅销系数处理
    """
    return get_profit_rate(df[column_name], df['popularity'], price)


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


class Predict(object):

    def __init__(self):
        """
        加载各类匹配表和模型
        """
        self.result = []

    def add_process_intent(self, final_price, used_years):
        """
        根据交易方式修正预测值
        """
        # 组合结果
        self.result = result_map.copy()
        self.result.loc[(self.result['intent'] == 'release'), 'predict_price'] = final_price
        self.result['predict_price'] = self.result['predict_price'].fillna(final_price)

        self.result['popularity'] = 'A'
        self.result['profit_rate'] = self.result.apply(process_profit_rate, args=('intent', final_price), axis=1)
        self.result['buy_profit_rate'] = self.result.apply(process_profit_rate, args=('intent_source', final_price), axis=1)
        self.result['predict_price'] = self.result['predict_price'] / self.result['buy_profit_rate']
        self.result['predict_price'] = self.result['profit_rate'] * self.result['predict_price']

        # 车况判断两年以内优秀,8-3年良好,9-11年一般,12年以上较差
        if used_years <= 2:
            condition = 'excellent'
        elif 2 < used_years <= 8:
            condition = 'good'
        elif 8 < used_years <= 11:
            condition = 'fair'
        elif 11 < used_years:
            condition = 'bad'
        # 计算所有交易类型
        self.result = cal_intent_condition(self.result.predict_price.values, condition)

    def query(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2):
        """
        查询
        """
        # 校验参数
        check_params_value(reg_year, reg_month, deal_year, deal_month, mile)

        # 查询对应条件预测
        self.result = db_operate.query(model_detail_slug, city)
        if len(self.result) == 0:
            raise ApiParamsValueError('model_detail_slug or city', 0, 'Unknown model or city!')
        online_year, median_price, k, b = self.result.loc[0, :].values
        median_price = int(median_price * 10000)
        # 省份差异
        province_price = k * median_price + b

        # 注册年份差异
        if online_year >= datetime.datetime.now().year:
            warehouse_year = 0
        else:
            warehouse_year = reg_year - online_year
        k = 0.0758
        warehouse_price = (k * warehouse_year) * median_price

        # 公里数差异
        used_months = ((deal_year - reg_year) * 12 + deal_month - reg_month)
        used_years = deal_year - reg_year
        if used_months <= 6:
            used_months = 6
        k, b = -0.1931, 0.0263
        mile_price = (k * (mile / used_months) + b) * median_price

        final_price = median_price + province_price + warehouse_price + mile_price

        print('median_price', int(median_price))
        print('province_price', int(province_price))
        print('warehouse_price', int(warehouse_price))
        print('mile_price', int(mile_price))
        print('final_price', int(final_price))

        # 根据交易方式修正预测值
        self.add_process_intent(final_price, used_years)

    def predict(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        预测返回
        """
        self.query(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)

        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def predict_with_condition(self, condition_desc=None, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        预测估值和车况定级
        """
        self.query(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
        used_years = deal_year - reg_year
        # 车况评级
        condition_valuate = pd.read_json(condition_desc, orient='records')
        condition_valuate = condition_evaluate_map.merge(condition_valuate, how='left', on=['item'])
        condition_valuate['score'] = condition_valuate.apply(cal_score, axis=1)
        condition_valuate = condition_valuate.groupby(['position'])['score'].sum().reset_index()
        if used_years <= 0:
            used_years = 1
        condition = cal_final_score_and_condition(condition_valuate, gl.CAR_CONDITION.index(self.result.loc[0, 'condition']), mile/used_years)
        self.result['condition'] = condition

        if ret_type == gl.RETURN_RECORDS:
            return self.result.to_dict(gl.RETURN_RECORDS)
        else:
            return self.result

    def verify(self, city='深圳', detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2):
        """
        预测返回
        """
        # 全国均值
        online_year, median_price = self.global_model_mean.loc[(self.global_model_mean['detail_slug'] == int(detail_slug)), ['online_year', 'median_price']].values[0]
        median_price = int(median_price * 10000)
        # 省份差异
        province = self.province_city_map.loc[(self.province_city_map['city'] == city), 'province'].values[0]
        k, b = self.div_province_k_param.loc[(self.div_province_k_param['province'] == province), ['k', 'b']].values[0]
        province_price = k * median_price + b

        # 注册年份差异
        warehouse_year = reg_year - online_year
        k = self.div_warehouse_k_param.loc[0, 'k']
        warehouse_price = (k * warehouse_year) * median_price

        # 公里数差异
        used_months = ((deal_year - reg_year) * 12 + deal_month - reg_month)
        if used_months <= 0:
            used_months = 1
        k, b = self.div_mile_k_param.loc[0, ['k', 'b']].values
        mile_price = (k * (mile/used_months) + b) * median_price

        final_price = median_price + province_price + warehouse_price + mile_price

        return int(final_price)

    def history_price_trend(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        计算历史价格趋势
        """
        self.query(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)

        condition = self.result.loc[0, 'condition']
        result = pd.DataFrame([], columns=['0', '-1', '-2', '-3', '-4', '-5', '-6', 'type', 'condition'])
        result.loc[0, ['0', 'type']] = self.result.loc[1, condition], 'buy'
        result.loc[1, ['0', 'type']] = self.result.loc[0, condition], 'sell'
        result.loc[2, ['0', 'type']] = self.result.loc[3, condition], 'private'
        for i in range(1, 7):
            result[str(-i)] = result['0'] * (1 + i * 0.0042)
            result[str(-i)] = result[str(-i)].astype(int)

        result['condition'] = condition
        if ret_type == gl.RETURN_RECORDS:
            return result.to_dict(gl.RETURN_RECORDS)
        else:
            return result

    def future_price_trend(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        计算未来价格趋势
        """
        self.query(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)
        used_years = deal_year - reg_year
        condition = self.result.loc[0, 'condition']
        result = pd.DataFrame([], columns=['0', '12', '24', '36', 'type', 'condition'])
        result.loc[0, ['0', 'type']] = self.result.loc[1, condition], 'buy'
        result.loc[1, ['0', 'type']] = self.result.loc[0, condition], 'sell'
        result.loc[2, ['0', 'type']] = self.result.loc[3, condition], 'private'
        k, b = 0.008, 0.11
        for i in range(0, 3):
            result[str((i+1)*12)] = result[str(i*12)] * (1 - ((used_years+i)*k+b))
            result[str((i+1)*12)] = result[str((i+1)*12)].astype(int)

        result['condition'] = condition

        if ret_type == gl.RETURN_RECORDS:
            return result.to_dict(gl.RETURN_RECORDS)
        else:
            return result

    def residuals(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        残值返回
        """
        self.query(city=city, model_detail_slug=model_detail_slug, reg_year=reg_year, reg_month=reg_month, deal_year=deal_year, deal_month=deal_month, mile=mile)

        result = pd.DataFrame([], columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'intent', 'condition'])
        temp = pd.DataFrame(pd.Series(self.result.loc[1, ['excellent', 'good', 'fair', 'bad']].values), columns=['0'])
        temp['intent'], temp['condition'] = 'buy', pd.Series(['excellent', 'good', 'fair', 'bad'])
        result = result.append(temp, sort=False)
        temp = pd.DataFrame(pd.Series(self.result.loc[0, ['excellent', 'good', 'fair', 'bad']].values), columns=['0'])
        temp['intent'], temp['condition'] = 'sell', pd.Series(['excellent', 'good', 'fair', 'bad'])
        result = result.append(temp, sort=False)
        temp = pd.DataFrame(pd.Series(self.result.loc[3, ['excellent', 'good', 'fair', 'bad']].values), columns=['0'])
        temp['intent'], temp['condition'] = 'private', pd.Series(['excellent', 'good', 'fair', 'bad'])
        result = result.append(temp, sort=False)

        used_years = deal_year - reg_year

        k, b = 0.008, 0.11
        param = used_years * k + b

        for i in range(1, 13):
            result[str(i)] = result['0'] * (1 - i * (param / 12))
            result[str(i)] = result[str(i)].astype(int)

        if ret_type == gl.RETURN_RECORDS:
            return result.to_dict(gl.RETURN_RECORDS)
        else:
            return result