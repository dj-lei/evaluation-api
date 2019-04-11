from valuate.db import *


def query(model_detail_slug, city):
    """
    查询估值
    """
    sql = 'select vgmm.*, vpc.* from (select online_year, median_price, control from china_used_car_estimate.valuate_global_model_mean where detail_model_slug = \''+model_detail_slug+'\') as vgmm , \
                        (select k,b from china_used_car_estimate.valuate_province_city where city = \''+city+'\') as vpc'
    return pd.read_sql_query(sql, ENGINE)




