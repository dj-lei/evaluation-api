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

###########################
# 模型预测配置
###########################
# # 畅销程度系数
# PROFITS = {'A': (0.06, 0.11, 0.027, 0.02, 0.12, 0.08, 0.09, 0.006, -0.01),
#            'B': (0.05, 0.13, 0.031, 0.025, 0.14, 0.10, 0.10, 0.007, -0.01),
#            'C': (0.05, 0.15, 0.02, 0.03, 0.16, 0.12, 0.11, 0.003, -0.01)}

PROFITS = {'A': (0.05, 0.095, 0.027, 0.02, 0.12, 0.08, 0.09, 0.006, -0.01),
           'B': (0.05, 0.114, 0.031, 0.025, 0.14, 0.10, 0.10, 0.007, -0.01),
           'C': (0.05, 0.134, 0.02, 0.03, 0.16, 0.12, 0.11, 0.003, -0.01)}

# 各车况因素的系数
CAR_CONDITION = ['excellent', 'good', 'fair', 'bad']
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

CONDITION_JSON = '[{"item":"左前纵梁","number":0},{"item":"右前纵梁","number":0},{"item":"左前减震器座","number":0},{"item":"右前减震器座","number":0},{"item":"防火墙","number":0},{"item":"左A柱","number":0},{"item":"左B柱","number":0},{"item":"左C柱","number":0},{"item":"右B柱","number":0},{"item":"右C柱","number":0},{"item":"右A柱","number":0},{"item":"左后纵梁","number":0},{"item":"右后纵梁","number":0},{"item":"右后减震器座","number":0},{"item":"左后减震器座","number":0},{"item":"火烧情况","number":0},{"item":"泡水情况","number":0},{"item":"前保险杠","number":0},{"item":"机盖","number":0},{"item":"左前叶子板","number":0},{"item":"左前轮胎","number":0},{"item":"左前轮毂","number":0},{"item":"前挡风玻璃","number":0},{"item":"左前门","number":0},{"item":"左后门","number":0},{"item":"左后叶子板","number":0},{"item":"左后轮胎","number":0},{"item":"左后轮毂","number":0},{"item":"左后大灯","number":0},{"item":"右后大灯","number":0},{"item":"后保险杠","number":0},{"item":"右后轮胎","number":0},{"item":"右后轮毂","number":0},{"item":"右后叶子板","number":0},{"item":"右后门","number":0},{"item":"右前门","number":0},{"item":"右前叶子板","number":0},{"item":"右前轮胎","number":0},{"item":"右前轮毂","number":0},{"item":"左侧下边梁","number":0},{"item":"右侧下边梁","number":0},{"item":"车顶","number":0},{"item":"右前大灯","number":0},{"item":"左前大灯","number":0},{"item":"中控台","number":0},{"item":"仪表盘","number":0},{"item":"主驾驶座椅","number":0},{"item":"副驾驶座椅","number":0},{"item":"后排座椅","number":0},{"item":"车辆顶棚","number":0},{"item":"换挡杆区域","number":0},{"item":"车辆娱乐设备","number":0},{"item":"方向盘","number":0},{"item":"空调","number":0},{"item":"右前翼子板内衬","number":0},{"item":"左前翼子板内衬","number":0},{"item":"右后翼子板内衬","number":0},{"item":"左后翼子板内衬","number":0},{"item":"前防撞梁","number":0},{"item":"后防撞梁","number":0},{"item":"备胎槽","number":0},{"item":"水箱框架","number":0},{"item":"发动机","number":0},{"item":"发动机状况","number":0},{"item":"变速箱","number":0},{"item":"变速箱状况","number":0},{"item":"转向系统","number":0},{"item":"离合器系统","number":0},{"item":"刹车系统","number":0},{"item":"发动机是否烧机油","number":0}]'


