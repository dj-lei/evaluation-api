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


class Predict(object):

    def __init__(self):
        """
        加载各类匹配表和模型
        """
        self.result = []
        self.combine_detail = pd.read_csv(path + '../tmp/combine_detail.csv')
        self.div_price_bn_k_param = pd.read_csv(path + '../tmp/div_price_bn_k_param.csv')
        self.div_province_k_param = pd.read_csv(path + '../tmp/div_province_k_param.csv')
        self.div_warehouse_k_param = pd.read_csv(path + '../tmp/div_warehouse_k_param.csv')
        self.div_mile_k_param = pd.read_csv(path + '../tmp/div_mile_k_param.csv')
        self.global_model_mean = pd.read_csv(path + '../tmp/global_model_mean.csv')
        self.province_city_map = pd.read_csv(path + '../tmp/province_city_map.csv')

    def add_process_intent(self, final_price, used_years):
        """
        根据交易方式修正预测值
        """
        # 组合结果
        self.result = result_map.copy()
        self.result.loc[(self.result['intent'] == 'release'), 'predict_price'] = final_price
        self.result['predict_price'] = self.result['predict_price'].fillna(final_price)

        self.result['popularity'] = 'A'
        self.result['profit_rate'] = self.result.apply(process_profit_rate, axis=1)
        self.result['buy_profit_rate'] = self.result.apply(process_buy_profit_rate, axis=1)
        self.result['predict_price'] = self.result['predict_price'] / self.result['buy_profit_rate']
        self.result['predict_price'] = self.result['profit_rate'] * self.result['predict_price']

        # 车况判断两年以内优秀,8-3年良好,9-11年一般,12年以上较差
        if used_years <= 2:
            condition = 'excellent'
        elif 2 < used_years <= 8:
            condition = 'good'
        elif 8 < used_years <= 11:
            condition = 'fair'
        elif 12 < used_years:
            condition = 'bad'
        # 计算所有交易类型
        self.result = cal_intent_condition(self.result.predict_price.values, condition)

    def predict(self, city='深圳', model_detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2, ret_type=gl.RETURN_RECORDS):
        """
        预测返回
        """
        detail_slug = self.combine_detail.loc[(self.combine_detail['detail_model_slug'] == model_detail_slug), 'car_autohome_detail_id'].values[0]

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
        used_years = deal_year - reg_year
        if used_months <= 0:
            used_months = 1
        k, b = self.div_mile_k_param.loc[0, ['k', 'b']].values
        mile_price = (k * (mile/used_months) + b) * median_price

        final_price = median_price + province_price + warehouse_price + mile_price
        print(final_price)
        # print('median_price', int(median_price))
        # print('province_price', int(province_price))
        # print('warehouse_price', int(warehouse_price))
        # print('mile_price', int(mile_price))
        # print('final_price', int(final_price))

        # 根据交易方式修正预测值
        self.add_process_intent(final_price, used_years)

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


