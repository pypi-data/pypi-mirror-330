import jwt.algorithms
from tdlc.tencentcloud.common import credential, common_client, exception
from tdlc.tencentcloud.common.profile import http_profile, client_profile
from tdlc.tencentcloud.dlc.v20210125 import models
from tdlc.utils import log, configurations, constants
from tdlc import exceptions
from tdlc.engines import qclient
import os
import time
import base64
import datetime
import requests

LOG = log.getLogger('QCloud')


def toSession(dto: models.NotebookSessionInfo) -> dict:
    session = {
        'name': dto.Name,
        'engine': dto.DataEngineName,
        'sessionId': dto.SessionId,
        'sparkAppId':dto.SparkAppId,
        'kind': dto.Kind,
        'status': dto.State,
        'log': [],
        'appInfo': {
            'sparkUiUrl': dto.SparkUiUrl,
        }
    }
    return session


def toStatement(dto: models.NotebookSessionStatementInfo) -> dict:

    statement_id = 0
    try:
        statement_id = int(dto.StatementId)
    except Exception as e:
        LOG.error(e)

    statement = {
        'statementId': statement_id,
        'status': dto.State,
        'completed': dto.Completed,
        'progress': dto.Progress,
        'started': dto.Started,
        'output': {}
    }


    data = {}

    if dto.OutPut.Data:
        for pair in dto.OutPut.Data:
            data[pair.Key] = pair.Value
        
    error_message = ''
    if dto.OutPut.ErrorMessage:
        error_message = ''.join(dto.OutPut.ErrorMessage)

    statement['output'] = {
        'data': data,
        'executionCount':dto.OutPut.ExecutionCount,
        'status': dto.OutPut.Status,
        'error': {
            'name': dto.OutPut.ErrorName,
            'value': dto.OutPut.ErrorValue,
            'message': error_message,
        }
    }

    return statement


class QCloudInteractiveApi(object):

    def __init__(self, region=None, secret_id=None, secret_key=None, token=None, endpoint=None, provider='default') -> None:

        self._region = region
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._token = token
        self._endpoint = endpoint

        LOG.info(f"Using {provider} credential provider.")

        cred = None
        profile = None
        if provider == constants.CREDENTIAL_PROVIDER_WEDATA:
            cred = WedataTempCredential(secret_id=secret_id, secret_key=secret_key, token=token, expired_time=configurations.EXPIRED_TIME.get())
        else:
            cred = credential.Credential(secret_id, secret_key, token=token)
            profile = client_profile.ClientProfile()
            if endpoint:
                profile.httpProfile = http_profile.HttpProfile(endpoint=endpoint)
        
        self._client = qclient.QClient(cred, region, profile)


    def get_engines(self):
        pass
    
    def get_sessions(self, engine, states=[]) -> list:

        request = models.DescribeNotebookSessionsRequest()
        request.DataEngineName = engine
        if states:
            request.State = states
        response = self._client.DescribeNotebookSessions(request)
        sessions = []
        for each in response.Sessions:
            sessions.append(toSession(each))
        return sessions


    def get_session(self, session_id):

        request = models.DescribeNotebookSessionRequest()
        request.SessionId = session_id

        response = self._client.DescribeNotebookSession(request)

        return toSession(response.Session)

    def create_session(self, 
                    engine, 
                    name, 
                    kind, 
                    driver_size,
                    executor_size,
                    executor_num,
                    files=[],
                    jars=[],
                    pyfiles=[],
                    archives=[],
                    timeout=3600,
                    arguments={},
                    image=None):

        request = models.CreateNotebookSessionRequest()
        request.Name = name
        request.DataEngineName = engine
        request.Kind = kind
        request.DriverSize = driver_size
        request.ExecutorSize = executor_size
        request.ExecutorNumbers = executor_num
        request.ProgramDependentFiles = files
        request.ProgramDependentJars = jars
        request.ProgramDependentPython = pyfiles
        request.ProgramArchives = archives
        request.ProxyUser = configurations.PROXY_USER.get()
        request.TimeoutInSecond = timeout
        request.Arguments = []
        request.SparkImage = image

        for k, v in arguments.items():
            o = models.KVPair()
            o.Key, o.Value = k, str(v)
            request.Arguments.append(o)

        response = self._client.CreateNotebookSession(request)

        return {
            "sessionId": response.SessionId,
            "sparkAppId": response.SparkAppId,
            "status": response.State,
        }

    def delete_session(self, session_id):

        request = models.DeleteNotebookSessionRequest()
        request.SessionId = session_id

        _ = self._client.DeleteNotebookSession(request)
        return None


    def submit_statement(self, session_id, kind, statement):

        request = models.CreateNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.Kind = kind
        if not statement:
            statement = ""
        request.Code = base64.b64encode(statement.encode('utf8')).decode('utf8')

        response = self._client.CreateNotebookSessionStatement(request)

        return toStatement(response.NotebookSessionStatement)


    def get_statement(self, session_id, statement_id):

        request = models.DescribeNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.StatementId = str(statement_id)

        response = self._client.DescribeNotebookSessionStatement(request)

        return toStatement(response.NotebookSessionStatement)


    def cancel_statement(self, session_id, statement_id):

        request = models.CancelNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.StatementId = str(statement_id)

        _ = self._client.CancelNotebookSessionStatement(request)
        return None


    def get_logs(self,session_id):
        request = models.DescribeNotebookSessionLogRequest()
        request.SessionId = session_id
        response = self._client.DescribeNotebookSessionLog(request)
        return response.Logs



class WedataTempCredential(object):

    def __init__(self, secret_id, secret_key, token, expired_time):

        self._secret_id = None
        self._secret_key = None
        self._token = None
        self._expired_time = None

    @property
    def secretId(self):
        self._need_refresh()
        return self._secret_id

    @property
    def secretKey(self):
        self._need_refresh()
        return self._secret_key

    @property
    def secret_id(self):
        self._need_refresh()
        return self._secret_id

    @property
    def secret_key(self):
        self._need_refresh()
        return self._secret_key

    @property
    def token(self):
        self._need_refresh()
        return self._token

    def _need_refresh(self):
        if None in [self._token, self._secret_key, self._secret_id] or self._expired_time < int(time.time()):
            LOG.debug(f'AK: {self._secret_id}, SK: {self._secret_key}, TOKEN: {self._token}, ExpireTime: {self._expired_time}, Now: {time.time()}')
            self.get_wedata_tmp_token()

    def get_wedata_tmp_token(self):

        import urllib.parse
        import jwt
        import uuid

        LOG.debug("start getting wedata token...")

        url = urllib.parse.urljoin(configurations.CREDENTIAL_WEDATA_ENDPOINT.get(), configurations.CREDENTIAL_WEDATA_PATH.get())
        uin = os.environ.get('QCLOUD_UIN') or configurations.UIN.get()
        subuin = os.environ.get('QCLOUD_SUBUIN') or configurations.SUBUIN.get()
        appid = os.environ.get('QCLOUD_APPID') or configurations.APPID.get()
        expired_time = int(time.time()) + configurations.CREDENTIAL_DURATION.get()

        wedata_secret = os.environ.get('WEDATA_SECRET') or configurations.CREDENTIAL_WEDATA_SECRET.get()
        payload = {
            'user_id': subuin,
            'tenant_id': appid,
            'owner_user_id': uin,
            'exp': expired_time,
        }

        LOG.debug(f'[WEDATA]payload: {payload}')

        auth = f"Bearer {jwt.encode(payload, wedata_secret, algorithm='HS256')}"
        LOG.debug(f"[WEDATA]auth: {auth}")

        response = requests.post(url, headers={
            'Content-Type': 'application/json',
            'Authorization': auth,
            'x-wedata-trace-id': 'NOTEBOOK-' + str(uuid.uuid4())
        }, json={
            'CloudServiceName': 'dlc'
        })
        LOG.debug(f"[WEDATA]Response is: {response.text}")

        data = response.json()
        r = data['Response']
        if 'Error' in r:
            raise exception.TencentCloudSDKException(code=r['Error']['Code'], message=r['Error']['Message'], requestId=r['RequestId'])

        self._secret_id = r['Data']['SecretId']
        self._secret_key = r['Data']['SecretKey']
        self._token = r['Data']['Token']
        self._expired_time = expired_time