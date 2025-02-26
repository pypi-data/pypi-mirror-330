from tdlc import exceptions
from tdlc.engines import sessions, cloudapi, commands
from tdlc.utils import constants, render, configurations, log, validators
import six


LOG = log.getLogger('Controller')


class EngineSessionController:

	def __init__(self, mode) -> None:

		self._session_default_prefix = 'session'
		self._current_session = None
		self._sessions = {}

		self._kernel_mode = mode


		LOG.debug(f"Initialize Engine Controller with kernel '{mode}', allowed session num is {configurations.SESSION_NUM_MAX.get()}")


	def _is_single_session_mode(self):
		return self._kernel_mode == constants.KERNEL_MODE_SPARK
	
	def build_local_session_name(self):

		name = None
		for i in range(0, 1000):
			name = f'{self._session_default_prefix}-{i}'
			if not self._sessions.get(name):
				return name
		return name

	def buidl_api_gateway(self, region, secretId, secretKey, token=None, endpoint=None):
		LOG.debug(f'build gateway with region: {region}')
		return cloudapi.QCloudInteractiveApi(region=region, secret_id=secretId, secret_key=secretKey, token=token, endpoint=endpoint, provider=configurations.CREDENTIAL_PROVIDER.get())
	
	def start_session(self, engine, name, language, qclouds={}, properties={}, conf={}):

		validators.required(engine, "Engine is required, please provide with '--engine <ENGINE>'")
		provider = configurations.CREDENTIAL_PROVIDER.get()
		if provider != constants.CREDENTIAL_PROVIDER_WEDATA:
			validators.checkQcloudArgs(qclouds)
		validators.checkPropertyArgs(properties)
		
		if not name:
			name = self.build_local_session_name()
		else:
			if self._sessions.get(name):
				raise exceptions.SessionExistException()
		
		current_session_num = self._sessions.values().__len__()
		if self._is_single_session_mode() and current_session_num >= 1:
			raise exceptions.SessionIsLimitedException(post='Only one session is allowed.')
		
		gateway = self.buidl_api_gateway(**qclouds)

		session = sessions.Session(gateway=gateway, engine=engine, name=name, kind=constants.LANGUAGE_TO_KIND[language], **properties, conf=conf)
		session.start()
		self._sessions[name] = session
		self.reset_current_session(session)

		session.check_spark_or_sql_context()


	def attach_session(self, engine, name, language, session_id, qclouds={}):

		validators.required(engine, "Engine is required, please provide with '--engine <ENGINE>'")
		validators.required(session_id, "SessionId is required, please provide with '--session-id <SESSIONID>'")
		validators.checkQcloudArgs(qclouds)

		for session in self.get_sessions():
			if session.id == session_id:
				raise exceptions.SessionAttachedException(session.name)

		if not name:
			name = self.build_local_session_name()
		else:
			if self._sessions.get(name):
				raise exceptions.SessionExistException(name)
			
		gateway = self.buidl_api_gateway(**qclouds)

		kind = constants.LANGUAGE_TO_KIND[language]

		session = sessions.Session(gateway=gateway, engine=engine, name=name, kind=kind)
		session.attach(session_id)

		self._sessions[name] = session
		self.reset_current_session(session)
		session.check_spark_or_sql_context()


	def get_sessions(self):
		return self._sessions.values()
	
	def get_remote_sessions(self, engine, qclouds={}, states=[]):

		gateway = self.buidl_api_gateway(**qclouds)
		_sessions = []
		for dto in gateway.get_sessions(engine, states):
			s = sessions.Session(gateway, dto['engine'], '', dto['kind']) 
			s.id = dto['sessionId']
			s.remote_name = dto['name']
			s.status = dto['status']
			s.spark_ui_url = dto['appInfo']['sparkUiUrl']
			_sessions.append(s)

		return _sessions


	def detach_session(self, name):

		session = self.get_current_session(name)
		del self._sessions[session.name]
		self.reset_current_session()

		render.toStdout(f"Successfully detached from {session}.")

	def reset_current_session(self, session=None, randonm_if_none=True):
		self._current_session = session
		if self._current_session is None and randonm_if_none and self._sessions:
			self._current_session = six.next(six.itervalues(self._sessions))

	def get_current_session(self, name=None, throw=True) -> sessions.Session:
		session = self._current_session
		if name:
			session = self.get_session_by_name(name, throw=throw)

		if not session and throw:
			raise exceptions.SessionNotAvailableException

		return session
		
	def stop_session(self, name):

		session = self.get_current_session(name)
		session.stop()

		del self._sessions[session.name]
		self.reset_current_session()
	
	
	def get_session_by_name(self, name, throw=True):

		session = self._sessions.get(name, None)
		if throw and not session:
			raise exceptions.SessionNotFoundException()
		return session

	def render_sessions(self, remote=False, engine=None, qclouds=None):

		sessions = []

		if remote and engine:
			sessions = self.get_remote_sessions(engine, qclouds, constants.SESSION_ACTIVE_STATUS)
		else:
			sessions = self.get_sessions()

		rows = []
		for session in sessions:
			rows.append(session.to_columns(session == self._current_session))
		render.asHTMLTable(constants.SESSION_COLUMNS, rows)
	
	def render_logs(self, name, reverse=None):
		session = self.get_current_session(name)
		render.toStdout(session.get_logs(reverse))

	def run_command(self, command: commands.Command, name=None, kind=None):
		session = self.get_current_session(name)
		self.reset_current_session(session)
		return command.execute(session, kind)

	def execute_sql(self, sql: commands.SQLCommand, name=None, kind=None):
		session = self.get_current_session(name)
		self.reset_current_session(session)
		return sql.execute(session, kind)
	
