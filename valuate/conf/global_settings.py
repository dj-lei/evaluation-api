from valuate.conf import *
ENCODING = 'utf-8'

##########################
# 生产,测试,本地库配置
##########################

# 运行环境[PRODUCT,PRODUCT_OUTTER,TEST,LOCAL]
RUNTIME_ENVIRONMENT = os.environ.get('VALUATE_RUNTIME_ENVIRONMENT', 'PRODUCT')

if RUNTIME_ENVIRONMENT == 'LOCAL':
    # 生产库外网
    PRODUCE_DB_ADDR_OUTTER = '101.201.143.74'
    PRODUCE_DB_USER = 'leidengjun'
    PRODUCE_DB_PASSWD = 'ldj_DEV_~!'
    PRODUCE_PINGJIA_ENGINE = 'mysql+pymysql://'+PRODUCE_DB_USER+':'+PRODUCE_DB_PASSWD+'@'+PRODUCE_DB_ADDR_OUTTER+'/pingjia?charset=utf8'
    PRODUCE_DATASOURCE_ENGINE = 'mysql+pymysql://'+PRODUCE_DB_USER+':'+PRODUCE_DB_PASSWD+'@'+PRODUCE_DB_ADDR_OUTTER+'/datasource?charset=utf8'

    # 测试库
    TEST_DB_ADDR = '101.200.229.249'
    TEST_DB_USER = 'pingjia'
    TEST_DB_PASSWD = 'De32wsxC'
    TEST_PINGJIA_ENGINE = 'mysql+pymysql://'+TEST_DB_USER+':'+TEST_DB_PASSWD+'@'+TEST_DB_ADDR+'/pingjia?charset=utf8'

    # 历史库
    HISTORY_DB_ADDR = '101.201.148.49:3306'
    HISTORY_DB_USER = 'leidengjun'
    HISTORY_DB_PASSWD = 'ldj_DEV_~!'
    HISTORY_PINGJIA_ENGINE = 'mysql+pymysql://'+HISTORY_DB_USER+':'+HISTORY_DB_PASSWD+'@'+HISTORY_DB_ADDR+'/databak?charset=utf8'
elif RUNTIME_ENVIRONMENT == 'TEST':
    # 生产库外网
    PRODUCE_DB_ADDR_OUTTER = '10.45.138.200'
    PRODUCE_DB_USER = 'leidengjun'
    PRODUCE_DB_PASSWD = 'ldj_DEV_~!'
    PRODUCE_PINGJIA_ENGINE = 'mysql+pymysql://' + PRODUCE_DB_USER + ':' + PRODUCE_DB_PASSWD + '@' + PRODUCE_DB_ADDR_OUTTER + '/pingjia?charset=utf8'
    PRODUCE_DATASOURCE_ENGINE = 'mysql+pymysql://' + PRODUCE_DB_USER + ':' + PRODUCE_DB_PASSWD + '@' + PRODUCE_DB_ADDR_OUTTER + '/datasource?charset=utf8'

    # 测试库
    TEST_DB_ADDR = '10.44.206.161'
    TEST_DB_USER = 'pingjia'
    TEST_DB_PASSWD = 'De32wsxC'
    TEST_PINGJIA_ENGINE = 'mysql+pymysql://' + TEST_DB_USER + ':' + TEST_DB_PASSWD + '@' + TEST_DB_ADDR + '/pingjia?charset=utf8'

    # 历史库
    HISTORY_DB_ADDR = '10.45.144.69:3306'
    HISTORY_DB_USER = 'leidengjun'
    HISTORY_DB_PASSWD = 'ldj_DEV_~!'
    HISTORY_PINGJIA_ENGINE = 'mysql+pymysql://' + HISTORY_DB_USER + ':' + HISTORY_DB_PASSWD + '@' + HISTORY_DB_ADDR + '/databak?charset=utf8'
elif RUNTIME_ENVIRONMENT == 'PRODUCT':
    # 生产库内网
    PRODUCE_DB_ADDR_OUTTER = '10.45.138.200'
    PRODUCE_DB_USER = 'leidengjun'
    PRODUCE_DB_PASSWD = 'ldj_DEV_~!'
    PRODUCE_PINGJIA_ENGINE = 'mysql+pymysql://' + PRODUCE_DB_USER + ':' + PRODUCE_DB_PASSWD + '@' + PRODUCE_DB_ADDR_OUTTER + '/pingjia?charset=utf8'
    PRODUCE_DATASOURCE_ENGINE = 'mysql+pymysql://' + PRODUCE_DB_USER + ':' + PRODUCE_DB_PASSWD + '@' + PRODUCE_DB_ADDR_OUTTER + '/datasource?charset=utf8'

    # 生产库
    TEST_DB_ADDR = '100.114.30.239:18056'
    TEST_DB_USER = 'pingjia'
    TEST_DB_PASSWD = 'De32wsxC'
    TEST_PINGJIA_ENGINE = 'mysql+mysqlconnector://' + TEST_DB_USER + ':' + TEST_DB_PASSWD + '@' + TEST_DB_ADDR + '/valuate?charset=utf8'

    # 历史库
    HISTORY_DB_ADDR = '10.45.144.69:3306'
    HISTORY_DB_USER = 'leidengjun'
    HISTORY_DB_PASSWD = 'ldj_DEV_~!'
    HISTORY_PINGJIA_ENGINE = 'mysql+pymysql://' + HISTORY_DB_USER + ':' + HISTORY_DB_PASSWD + '@' + HISTORY_DB_ADDR + '/databak?charset=utf8'
elif RUNTIME_ENVIRONMENT == 'PRODUCT_OUTTER':
    # 生产库外网
    PRODUCE_DB_ADDR_OUTTER = '101.201.143.74'
    PRODUCE_DB_USER = 'leidengjun'
    PRODUCE_DB_PASSWD = 'ldj_DEV_~!'
    PRODUCE_PINGJIA_ENGINE = 'mysql+pymysql://'+PRODUCE_DB_USER+':'+PRODUCE_DB_PASSWD+'@'+PRODUCE_DB_ADDR_OUTTER+'/pingjia?charset=utf8'
    PRODUCE_DATASOURCE_ENGINE = 'mysql+pymysql://'+PRODUCE_DB_USER+':'+PRODUCE_DB_PASSWD+'@'+PRODUCE_DB_ADDR_OUTTER+'/datasource?charset=utf8'

    # 生产库
    TEST_DB_ADDR = '101.201.199.62'
    TEST_DB_USER = 'leidengjun'
    TEST_DB_PASSWD = 'ldj_DEV_~!'
    TEST_PINGJIA_ENGINE = 'mysql+pymysql://' + TEST_DB_USER + ':' + TEST_DB_PASSWD + '@' + TEST_DB_ADDR + '/valuate?charset=utf8'

    # 历史库
    HISTORY_DB_ADDR = '101.201.148.49:3306'
    HISTORY_DB_USER = 'leidengjun'
    HISTORY_DB_PASSWD = 'ldj_DEV_~!'
    HISTORY_PINGJIA_ENGINE = 'mysql+pymysql://'+HISTORY_DB_USER+':'+HISTORY_DB_PASSWD+'@'+HISTORY_DB_ADDR+'/databak?charset=utf8'

###########################
# 模型预测配置
###########################
# 公里数阈值和范围
# 正常行驶的车辆以一年2.5万公里为正常基数，低于2.5万公里的价格的浮动在+3.5%以内
# 大于2.5万公里的若每年的平均行驶里程大于2.5万公里小于5万公里价格浮动在-3.5-7.5%
# 若年平均形式里程大于5万公里及以上影响价格在-7.5-12.5%之间
MILE_THRESHOLD_2_5 = 2.5
MILE_THRESHOLD_5 = 5
MILE_THRESHOLD_10 = 10

# # 畅销程度系数
# PROFITS = {'A': (0.06, 0.11, 0.027, 0.02, 0.12, 0.08, 0.09, 0.006, -0.01),
#            'B': (0.05, 0.13, 0.031, 0.025, 0.14, 0.10, 0.10, 0.007, -0.01),
#            'C': (0.05, 0.15, 0.02, 0.03, 0.16, 0.12, 0.11, 0.003, -0.01)}

PROFITS = {'A': (0.05, 0.094, 0.027, 0.02, 0.12, 0.08, 0.09, 0.006, -0.01),
           'B': (0.05, 0.114, 0.031, 0.025, 0.14, 0.10, 0.10, 0.007, -0.01),
           'C': (0.05, 0.134, 0.02, 0.03, 0.16, 0.12, 0.11, 0.003, -0.01)}

# 各车况因素的系数
CAR_CONDITION_COEFFICIENT = {'excellent': 1.04, 'good': 1, 'fair': 0.95, 'bad': 0.89}
CAR_CONDITION_COEFFICIENT_VALUES = [1.04, 1, 0.95, 0.89]

# 交易方式
INTENT_TYPE = ['sell', 'buy', 'release', 'private', 'lowest', 'cpo', 'replace', 'auction', 'avg-buy', 'avg-sell']
INTENT_TYPE_CAN = ['release', 'release', 'release', 'release', 'release', 'release', 'release', 'release', 'release', 'release']

# 返回类型
RETURN_RECORDS = 'records'
RETURN_NORMAL = 'normal'

###########################
# 异常类型
###########################
ERROR_PARAMS = 'PARAMS'
ERROR_SQL = 'SQL'


