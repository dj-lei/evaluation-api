from valuate.db import *


###############################
# 生产库相关操作
###############################
# def query_valuate(model_detail_slug, city):
#     """
#     查询估值
#     """
#     query_sql = 'select vpd.*,vccd.diff,vclsd.a,vclsd.b from valuate.valuate_predict_data as vpd \
#         left join pingjia.open_model_detail as omd on vpd.model_detail_slug_id = omd.id \
#         left join pingjia.open_city as oc on vpd.city_id = oc.id and oc.parent != 0 \
#         left join valuate.valuate_c2b_calculate_data as vccd on vpd.model_slug_id = vccd.model_slug_id and vpd.province_id = vccd.province_id \
#         left join valuate.valuate_c2b_least_squares_data as vclsd on vpd.popularity = vclsd.popularity \
#         where omd.detail_model_slug = \''+model_detail_slug+'\' and oc.name = \''+city+'\' '
#
#     return pd.read_sql_query(query_sql, ENGINE)

def query_valuate(model_detail_slug, city):
    """
    查询估值
    """
    query_sql = 'select vpd.*,omd.year from valuate.valuate_predict_data_alter as vpd \
        left join pingjia.open_model_detail as omd on vpd.model_detail_slug_id = omd.id \
        left join pingjia.open_city as oc on vpd.province_id = oc.parent and oc.parent != 0 \
        where omd.detail_model_slug = \''+model_detail_slug+'\' and oc.name = \''+city+'\' '

    return pd.read_sql_query(query_sql, ENGINE)


def query_residuals(model_detail_slug, city):
    """
    查询残值
    """
    query_sql = 'select vpd.*,vccd.diff,vclsd.a,vclsd.b,vrd.k_param from valuate.valuate_predict_data as vpd \
        left join pingjia.open_model_detail as omd on vpd.model_detail_slug_id = omd.id \
        left join pingjia.open_city as oc on vpd.city_id = oc.id and oc.parent != 0 \
        left join valuate.valuate_c2b_calculate_data as vccd on vpd.model_slug_id = vccd.model_slug_id and vpd.province_id = vccd.province_id \
        left join valuate.valuate_c2b_least_squares_data as vclsd on vpd.popularity = vclsd.popularity \
        left join valuate.valuate_residuals_data as vrd on vpd.model_slug_id = vrd.model_slug_id and vpd.province_id = vrd.province_id \
        where omd.detail_model_slug = \''+model_detail_slug+'\' and oc.name = \''+city+'\' '

    return pd.read_sql_query(query_sql, ENGINE)


def query_residuals_median(popularity):
    """
    查询残值
    """
    query_sql = 'SELECT \
                  @k_param \
                FROM \
                  (SELECT \
                    k_param, \
                    @rum := @rum + 1, \
                    IF( \
                      @rum = \
                      (SELECT \
                        FLOOR(COUNT(*) / 2) \
                      FROM \
                        valuate.valuate_residuals_data \
                      WHERE popularity = \''+popularity+'\'), \
                      @k_param := k_param, \
                      0 \
                    ), \
                    @k_param \
                  FROM \
                    valuate.valuate_residuals_data, \
                    (SELECT \
                      @rum := 0) t \
                  WHERE popularity = \''+popularity+'\' \
                  ORDER BY k_param) t \
                LIMIT 1 '
    return pd.read_sql_query(query_sql, ENGINE)


def query_valuated_models():
    """
    查询可预测车型
    """
    query_sql = 'select distinct model_slug from valuate_model_detail_map'
    result = pd.read_sql_query(query_sql, ENGINE)
    return list(set(result.model_slug.values))


def query_valuated_model_details():
    """
    查询可预测车型
    """
    query_sql = 'select distinct model_detail_slug from valuate_model_detail_map'
    result = pd.read_sql_query(query_sql, ENGINE)
    return list(set(result.model_detail_slug.values))


def query_valuated_cities():
    """
    查询可预测城市
    """
    query_sql = 'select distinct name from pingjia.open_city where parent != 0'
    result = pd.read_sql_query(query_sql, ENGINE)
    return list(set(result.name.values))

