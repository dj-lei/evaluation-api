from valuate.predict import *


class Predict(object):

    def __init__(self):
        """
        加载各类匹配表和模型
        """
        self.result = []
        self.model_k_param = pd.read_csv(path + '../tmp/model_k_param.csv')
        self.div_price_bn_k_param = pd.read_csv(path + '../tmp/div_price_bn_k_param.csv')
        self.div_province_k_param = pd.read_csv(path + '../tmp/div_province_k_param.csv')
        self.div_warehouse_k_param = pd.read_csv(path + '../tmp/div_warehouse_k_param.csv')
        self.div_mile_k_param = pd.read_csv(path + '../tmp/div_mile_k_param.csv')
        self.global_model_mean = pd.read_csv(path + '../tmp/global_model_mean.csv')
        self.province_city_map = pd.read_csv(path + '../tmp/province_city_map.csv')

    def predict(self, city='深圳', detail_slug='model_25023_cs', reg_year=2015, reg_month=3, deal_year=datetime.datetime.now().year, deal_month=datetime.datetime.now().month, mile=2):
        """
        预测返回
        """
        # 全国均值
        online_year, median_price = self.global_model_mean.loc[(self.global_model_mean['detail_slug'] == detail_slug), ['online_year', 'predict_price']].values[0]

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
        # print('median_price', int(median_price))
        # print('province_price', int(province_price))
        # print('warehouse_price', int(warehouse_price))
        # print('mile_price', int(mile_price))
        # print('final_price', int(final_price))

        return int(final_price)


