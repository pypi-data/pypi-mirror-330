from tdlc.engines import cloudapi, commands
from tdlc.utils import constants, render, configurations, log, common
from tdlc import exceptions

import time
import random


LOG = log.getLogger("Session")

''' 处理已知业务问题 '''
def _handle_known_errors(e, *args):

    if 'message' not in e.__dict__:
        raise e

    ''' 引擎不存在问题 '''
    if common.contains_all_keywords(e.message, ['Find no house', 'fail']):
        raise exceptions.EngineNotExistException(*args)
    
    ''' RoleArn 不存在问题 '''
    if common.contains_all_keywords(e.message, ['Get role', 'fail']):
        raise exceptions.RoleArnNotFoundException(*args)

    ''' 远程 Session 不存在问题 '''
    if common.contains_all_keywords(e.message, ["Get session", "fail"]):
        raise exceptions.SessionNotFoundException(*args)
    
    ''' 集群 不在运行状态 '''
    if common.contains_all_keywords(e.message, ["Cluster is not ready"]) or common.contains_all_keywords(e.message, ["not running"]):
        raise exceptions.EngineNotReadyException
    
    ''' 集群资源不足 '''
    if common.contains_all_keywords(e.message, ["Cluster resources insufficient"]):
        raise exceptions.EngineInsufficientException
    
    ''' 镜像不存在 '''
    if common.contains_all_keywords(e.message, ["Spark images nonuniquen"]):
        raise exceptions.ImageNotExistsException

    raise e

class Session(object):

    def __init__(self, gateway, 
                       engine, 
                       name, 
                       kind,
                       roleArn=None,
                       timeout=None, 
                       driverSize=None, 
                       executorSize=None, 
                       executorNum=None, 
                       image=None,
                       jars=[], 
                       pyfiles=[], 
                       archives=[], 
                       files=[],
                       conf={}) -> None:

        self._gateway :cloudapi.QCloudInteractiveApi= gateway
        self.status = None

        self.engine = engine
        self._jars = jars
        self._pyfiles = pyfiles
        self._archives = archives
        self._files = files

        self._role_arn = roleArn
        self._conf = conf
        self._mode = constants.SESSION_MODE_NATIVE

        self.id = None
        self.spark_app_id = None
        self.spark_ui_url = ''
        self.name = name
        self.remote_name = self._build_session_name()
        self.kind = kind
        self.timeout = timeout or configurations.SESSION_TIMEOUT.get()
        self.driver_size = driverSize or configurations.DRIVER_SIZE.get()
        self.executor_size = executorSize or configurations.EXECUTOR_SIZE.get()
        self.executor_num = executorNum or configurations.EXECUTOR_NUM.get()
        self.image = image

        self.spark_or_sql_context_var_name = None
    
    def _build_session_name(self):
        r = random.randint(0, 1000)
        return f'session-{int(time.time())}'

    def start(self):

        LOG.info(f"Starting {self}, kind={self.kind}, dirverSize={self.driver_size}, executor=<{self.executor_num},{self.executor_size}>")
        try:

            render.toStdout(f"Starting {self} from engine '{self.engine}', please wait a while...\n")
            arguments = {
                'dlc.role.arn': self._role_arn
            }

            arguments.update(self._conf)

            r = self._gateway.create_session(
                self.engine, 
                self.remote_name, 
                self.kind, 
                driver_size=self.driver_size,
                executor_size=self.executor_size,
                executor_num=self.executor_num,
                files=self._files,
                jars=self._jars,
                pyfiles=self._pyfiles,
                archives=self._archives,
                timeout=self.timeout,
                arguments=arguments,
                image=self.image)

            self.id = r['sessionId']
            self.spark_app_id = r['sparkAppId']
            self.status = r['status']
            # self.spark_ui_url = r['appInfo']['sparkUiUrl']

        except Exception as e:
            _handle_known_errors(e)

        try:
            r = self.wait_for_idle()
        except exceptions.SessionTimeoutException as e:
            raise exceptions.SessionTimeoutException(post=f"{self} did not start up in {configurations.WAIT_IDLE_TIMEOUT.get()}s.")
        except KeyboardInterrupt:
            # 不判断那状态 直接 kill
            # if self.status != constants.SESSION_STATUS_NOT_STARTED:
            # 处理 EOS 超时问题
            try:
                self.stop()
            except Exception as e:
                LOG.error(e)
            raise exceptions.InterruptException
        except exceptions.tdlcException as e:
            _handle_known_errors(e)
        
        self.render_as_table(True)
     
    def stop(self):

        render.toStdout(f"Closing the {self}...\n")

        try:
            self._gateway.delete_session(self.id)
        except Exception as e:
            LOG.error(e)

        starts = time.time()

        while time.time() - starts <= 60:
            self.refresh_status()
            if self.status in constants.SESSION_FINAL_STATUS:
                render.toStdout(f"Successfully close the {self}.\n")
                return
            self.sleep(2)


    
    def refresh_status(self):

        ''' 更新当前 session 状态'''
        # TODO logs

        try:
            r = self._gateway.get_session(self.id)
        except Exception as e:
            _handle_known_errors(e)

        self.spark_ui_url = r['appInfo']['sparkUiUrl']

        status = r['status']
        if status not in constants.SESSION_STATUS_SUPPORTED:
            raise exceptions.UnknownStatusException(f"{self} status '{status}' is unknown.")
        self.status = status

        return r

    
    def check_spark_or_sql_context(self):

        command = commands.Command("spark;sc=spark.sparkContext")

        (success, out, mimetype) = command.execute(self)
        if success:
            render.toStdout("SparkSesson available as 'spark'.\n")
            render.toStdout("SparkContext available as 'sc'.\n")
            self.spark_or_sql_context_var_name = 'spark'
        else:
            command = commands.Command("sqlContext")
            (success, out, mimetype) = command.execute(self)
            if success:
                if 'hive' in out.lower():
                    render.toStdout("HiveContext available as 'sqlContext'.\n")
                else:
                    render.toStdout("SqlContext available as 'sqlContext'.\n")
                self.spark_or_sql_context_var_name = 'sqlContext'
            else:
                raise exceptions.SessionContextException

    def wait_for_idle(self, seconds_to_wait=None):

        if seconds_to_wait is None:
            seconds_to_wait = configurations.WAIT_IDLE_TIMEOUT.get()
        
        starts = time.time()

        while True:

            if time.time() - starts >= seconds_to_wait:
                raise exceptions.SessionTimeoutException(post=f"Waiting '{self}' idle timeout.")

            self.refresh_status()

            if self.status == constants.SESSION_STATUS_IDLE:
                return
            
            if self.status in constants.SESSION_FINAL_STATUS:
                raise exceptions.SessionTerminated(f"The status of {self} is {self.status}")
            

            LOG.debug(f"Waitting for {self} idle, sleep for 2 seconds.")
            self.sleep(2)
            

    def submit_statement(self, code, kind=None):
        return self._gateway.submit_statement(self.id, kind or self.kind, code)
    
    def get_statement(self, statement_id):
        return self._gateway.get_statement(self.id, statement_id)
    
    def cancel_statement(self, statement_id):
        return self._gateway.cancel_statement(self.id, statement_id)

    def get_logs(self, reverse):
        _logs = self._gateway.get_logs(session_id=self.id)
        # 服务端按照 时间倒序返回日志， 这里取反
        if not reverse:
            _logs.reverse()
        return '\n'.join(_logs)

    def sleep(self, seconds):
        time.sleep(seconds)

    def attach(self, session_id):

        self.id = session_id

        render.toStdout(f"Attachting to {self}...")
        r = self.refresh_status()

        ''' 更新 session 信息 '''
        self.remote_name = r['name']
        self.spark_ui_url = r['appInfo']['sparkUiUrl']

        if self.kind != r['kind']:
            render.toStderr(f'[Warning]The requested session kind "{self.kind}" is different from the server side "{r["kind"]}", change to "{r["kind"]}".')
        self.kind = r['kind']

        if self.status in constants.SESSION_FINAL_STATUS:
            raise exceptions.SessionTerminated(f"The status of {self} is {self.status}")
        
        self.render_as_table(True)
        

    def to_columns(self, current=False):

        spark_ui_link = f"<a target='_blank' href='{self.spark_ui_url}'>SparkUI</a>"
        _current = ''
        if current:
            _current = 'Y'
            
        return [self.id, self.name, self.remote_name, self.engine,  spark_ui_link, self.kind, self.status, '', _current]

    def render_as_table(self, current=False):
        render.asHTMLTable(constants.SESSION_COLUMNS, [self.to_columns(current)])

    
    def __str__(self) -> str:
        return f'Session<{self.name}, {self.id}>'
    
