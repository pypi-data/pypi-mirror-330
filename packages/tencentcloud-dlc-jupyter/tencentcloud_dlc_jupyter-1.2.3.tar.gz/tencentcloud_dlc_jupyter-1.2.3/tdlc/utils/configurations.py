from tdlc.utils import constants

import os
import configparser
import json


SECTION_TDLC = 'tdlc'
SECTION_SPLITER = '__'
SECTION_SPARK_CONF = 'spark.conf'


_CONFIG_PATH = os.path.join(constants.HOME_PATH, "tdlc.ini")
_PARSER: configparser.ConfigParser = None

'''
tdlc__wait_idle_timout
'''

def get(key, default, typed=None):
    value = default
    try:
        value = _get_config_from_env(key) or _get_config_from_ini(key) or default
        if value and typed:
            value = typed(value)
    except Exception as e:
        raise
    return value



def _load():

    if not os.path.exists(constants.HOME_PATH):
        os.makedirs(constants.HOME_PATH)

    if not os.path.exists(_CONFIG_PATH):
        open(_CONFIG_PATH, 'w').close()

    parser = configparser.ConfigParser()
    parser.read(_CONFIG_PATH, encoding='utf8')
    if not parser.has_section(SECTION_TDLC):
        parser.add_section(SECTION_TDLC)

    return parser

def _save(key, value):
    _value = value
    if isinstance(value, dict):
        _value = json.dumps(value)
    else:
        _value = str(value)

    _PARSER.set(SECTION_TDLC, key, _value)
    _PARSER.write(open(_CONFIG_PATH, 'w'))

def _get_config_from_ini(k):

    global _PARSER

    if not _PARSER:
        _PARSER = _load()

    section = SECTION_TDLC
    key = k
    if SECTION_SPLITER in k:
        parts = k.split(SECTION_SPLITER)
        section = parts[0]
        key = parts[1]
    
    return _PARSER.get(section, key, fallback=None)


def _get_config_from_env(key):
    return os.environ.get(key)


def _toJSON(value):
    o = {}
    try:
        o = json.loads(value)
    except:
        pass
    return o




class Configuration(object):

    def __init__(self, key, default='', typed=str):

        self._key = key
        
        self._default = default

        self._typed = typed

        self._value = get(key, default, typed)
    

    def default(self):
        return self._default
    
    def get(self):
        return self._value

    def set(self, value, save=False):

        if value is None:
            return

        self._value = value
        if save:
            _save(self._key, self._value)
    
    def __str__(self):
        return '{}: {}'.format(self._key, self._value)

    
CONF = Configuration


LOG_FILE = CONF("log.file", os.path.join(constants.HOME_PATH,f"tdlc.log"))
LOG_LEVEL = CONF("log.level", "DEBUG")

REGION = CONF('qcloud.region')
SECRET_ID = CONF('qcloud.secret_id')
SECRET_KEY = CONF('qcloud.secret_key')
TOKEN = CONF('qcloud.token')
EXPIRED_TIME = CONF('qcloud.expired_time')
ENDPOINT = CONF('qcloud.endpoint')
ROLE_ARN = CONF('qcloud.role_arn')
ENGINE = CONF('qcloud.dlc.engine')

LANGUAGE = CONF('session.notebook.language', constants.LANGUAGE_PYTHON)

JARS = CONF('session.jars')
PYFILES = CONF('session.pyfiles')
ARCHIVES = CONF('session.archives')
FILES = CONF('session.files')
IMAGE = CONF('session.image')

PROXY_USER = CONF('session.proxy_user', 'root')
EXTRACONF = CONF('session.conf')

SESSION_TIMEOUT = CONF("session.timeout", 3600, int)
WAIT_IDLE_TIMEOUT = CONF("session.wait.idle.timeout", 600, int)

SESSION_NUM_MAX = CONF('session.limit.max_num', 5, int)

DRIVER_SIZE = CONF('session.spark.driver.size', constants.CU_SIZE_SMALL)
EXECUTOR_SIZE = CONF('session.spark.executor.size', constants.CU_SIZE_SMALL)
EXECUTOR_NUM = CONF('session.spark.executor.num', 1, int)


RESULT_MAX_ROWS = CONF("result.max.rows", 2500, int)
RESULT_SAMPLE_METHOD = CONF("result.sample.method", "take")
RESULT_SAMPLE_FRACTION = CONF("result.sample.fraction", 0.1, float)

SPARK_CONF = CONF("spark.conf", {}, _toJSON)


CREDENTIAL_PROVIDER = CONF('qcloud.credential.provider', 'default', str)
CREDENTIAL_WEDATA_ENDPOINT = CONF('qcloud.wedata.endpoint' ,'https://wedata-api-fusion-dev.cloud.tencent.com', str)
CREDENTIAL_WEDATA_PATH = CONF('qcloud.wedata.path' ,'/cloud/dataexploration/v1/GetCloudServiceTempToken', str)
CREDENTIAL_WEDATA_SECRET = CONF('qcloud.wedata.secret', '', str)
CREDENTIAL_DURATION = CONF('qcloud.credential.duration', 30 * 60, int)


UIN = CONF('qcloud.uin', '', str)
SUBUIN = CONF('qcloud.subuin', '', str)
APPID = CONF('qcloud.appid', 0, int)



def setAll(JSON: dict, save):

    REGION.set(JSON.get("region", ""), save)
    SECRET_ID.set(JSON.get("secret-id") or JSON.get("secretId", ""), save)
    SECRET_KEY.set(JSON.get("secret-key") or JSON.get("secretKey", ""), save)
    TOKEN.set(JSON.get('token'), save)
    ENDPOINT.set(JSON.get("endpoint", ""), save)
    ROLE_ARN.set(JSON.get("role-arn") or JSON.get("roleArn", ""), save)
    ENGINE.set(JSON.get("engine", ""), save)

    LANGUAGE.set(JSON.get("language"), save)
    PYFILES.set(JSON.get("pyfiles"), save)
    FILES.set(JSON.get("files"), save)
    ARCHIVES.set(JSON.get("archives"), save)
    JARS.set(JSON.get('jars'), save)
    # PROXY_USER.set(JSON.get("proxy_user"), save)

    SESSION_TIMEOUT.set(JSON.get("timeout"), save)
    DRIVER_SIZE.set(JSON.get("driver-size") or JSON.get("driverSize"), save)
    EXECUTOR_SIZE.set(JSON.get("executor-size") or JSON.get("executorSize"), save)
    EXECUTOR_NUM.set(JSON.get("executor-num") or JSON.get("executorNum"), save)

    IMAGE.set(JSON.get('image'), save)

    SPARK_CONF.set(JSON.get("conf"), save)


    #  TODO
    #  EXTRACONF 
    