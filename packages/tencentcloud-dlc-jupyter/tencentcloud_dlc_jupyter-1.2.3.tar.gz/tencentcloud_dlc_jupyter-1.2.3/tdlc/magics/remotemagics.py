import json
from IPython.core.magic import Magics, magics_class, line_magic, line_cell_magic, cell_magic, needs_local_scope
from IPython.core import magic_arguments
from tdlc.magics import basemagics
from tdlc.utils import log, render, constants, configurations, validators
from tdlc.widgets import configuiwidget
from tdlc import exceptions


LOG = log.getLogger("Magic")


@magics_class
class RemoteMagics(basemagics.BaseMagics):

    def __init__(self, mode, shell=None, **kwargs):
        super().__init__(mode, shell, **kwargs)

        self._config_ui_widget = configuiwidget.ConfigUiWidget(self.controller)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument("command", type=str, nargs="*", default=[], help="Command to execute.")
    @magic_arguments.argument(
        "-n",
        "--name",
        type=str,
        help="Session name, should be unique in local."
    )
    @magic_arguments.argument(
        "--session-id",
        type=str,
        default=None,
        help="Session id, unique globally."
    )
    @magic_arguments.argument(
        "--region",
        type=str,
        default=None,
        help="Region where DLC was used.",
    )
    @magic_arguments.argument(
        "--secret-id",
        type=str,
        default=None,
        help="SecretId of TencentCloud account, should have access to DLC at least."
    )
    @magic_arguments.argument(
        "--secret-key",
        type=str,
        default=None,
        help="SecretKey of TencentCloud account, should have access to DLC at least."
    )
    @magic_arguments.argument(
        "--token",
        type=str,
        default=None,
        help="Token of TencentCloud account, should have access to DLC at least."
    )
    @magic_arguments.argument(
        "--endpoint",
        type=str,
        default=None,
        help="Endpoint of TencentCloud DLC serivce."
    )
    @magic_arguments.argument(
        "--driver-size",
        type=str,
        default=None,
        help="Driver size for the session, options are " + ','.join(constants.CU_SIZE_SUPPORTED)
    )
    @magic_arguments.argument(
        "--executor-size",
        type=str,
        default=None,
        help="Executor size for the session, options are " + ','.join(constants.CU_SIZE_SUPPORTED)
    )
    @magic_arguments.argument(
        "--executor-num",
        type=str,
        default=None,
        help="Executor numbers for the session, should be more or equal than 1."
    )
    @magic_arguments.argument(
        "--jars",
        type=str,
        nargs="*",
        default=[],
        help="Dependency jars for the session."
    )
    @magic_arguments.argument(
        "--py-files",
        type=str,
        nargs="*",
        default=[],
        help="Dependency python files added to PYTHONPATH."
    )
    @magic_arguments.argument(
        "--files",
        type=str,
        nargs="*",
        default=[],
        help="Dependency files."
    )
    @magic_arguments.argument(
        "--archives",
        type=str,
        nargs="*",
        default=[],
        help="Archives added to working directory."
    )
    @magic_arguments.argument(
        "--engine",
        type=str,
        help="(DLC)Engine name for the session."
    )
    @magic_arguments.argument(
        "--role-arn",
        type=str,
        default=None,
        help="TencentCloud roleArn name for the session."
    )
    @magic_arguments.argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help="Language for the session; one of {}".format(', '.join(constants.LANGUAGES_SUPPORTED))
    )
    @magic_arguments.argument(
        "-t",
        "--timeout",
        type=int,
        default=None,
        help="Timeout(seconds) for the session; if timeout, the session will be killed;"
    )
    @magic_arguments.argument(
        "--conf",
        type=str,
        default=[],
        nargs="*",
        help="Engine configurations assigned to the session, seperated by blank; example '--conf spark.files.overwrite=true spark.eventLog.enabled=true'"
    )
    @magic_arguments.argument(
        "--remote",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="Query remote sessions in DLC engines."
    )
    @magic_arguments.argument(
        "--reverse",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="The logs will be rendered in time-reversed order."
    )
    @magic_arguments.argument(
        "--save",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="The configurations will be saved and taking effects in new kernels if set True",
    )
    @magic_arguments.argument(
        "--var-output",
        type=str,
        default=None,
        help="The ouput variable name. ",
    )
    @magic_arguments.argument(
        "--sample-method",
        type=str,
        default=None,
        help="The sample method.",
    )
    @magic_arguments.argument(
        "--sample-fraction",
        type=str,
        default=None,
        help="The sample fraction for sample method.",
    )
    @magic_arguments.argument(
        "--max-rows",
        type=int,
        default=None,
        help="The max rows pull back.",
    )
    @magic_arguments.argument(
        "--coerce",
        type=str,
        default=None,
        help="",
    )
    @magic_arguments.argument(
        "--quiet",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="Do not display result when using SQL.",
    )
    @magic_arguments.argument(
        "--var-input",
        type=str,
        default=None,
        help="The variable name being sended to engine.",
    )
    @magic_arguments.argument(
        "--var-type",
        type=str,
        default=None,
        help="The variable type being sended to engine. ",
    )
    @magic_arguments.argument(
        "--var-name",
        type=str,
        default=None,
        help="The variable name to store the data being sended. ",
    )
    @magic_arguments.argument(
        "--image",
        type=str,
        default=None,
        help="The spark image to be used. ",
    )
    @needs_local_scope
    @line_cell_magic
    @exceptions.wrap_magic_exceptions
    def spark(self, line, cell=None, local_ns=None):
        '''Magic to communicate with DLC spark cluster.

        The maigc is used to communicate a DLC spark cluster remotely. 
        Each session can be shared with multi users

        Subcommand
        ----------
        ui
            Create session using GUI.
        config
            Config current kernel or globally if --save is provided.
            e.g. `%%spark config --save
                {
                    region: <REGION>,
                    secret-id: <SECRETID>,
                    secret-key: <SECRETKEY>
                }`
        start
            Create a new session.
            e.g. `%spark start --name session1 --engine notebook --secret-id <SECRETID> --secret-key <SECRETKEY>` the secret-id/secret-key will be overwrite with line args. 
        session
            List current available sessions.
            e.g. `%spark session --remote` to list local or remote sessions if --remote is provided.
        attach
            Attach to a remote session.
            e.g. `%spark attach --name session1 --sesion-id <SESSIONID>`
        detach
            Detach from a local session.
            e.g. `%spark detach --name session1` will detach from the session 'session1'
        stop
            Stop a session.
            e.g. `%spark stop --name session1` will stop the session 'session1'
        log
            Get logs for a given session.
            e.g. `%spark logs --name session1 --reverse` will return logs in time-reversed order.
        exec
            Execute spark code for a given session.
            e.g. `%%spark --name session1` will execute code with 'session1'
            e.g. `%%spark --language scala` will execute code in scalca
            e.g. `%%spark --var-output var1 --max-rows 1000` will execute code and store the 1000 rows result typed pandas dataframe in 'var1'
        sql
            Execute SQL for a given session
            e.g. `%%spark sql --quiet` will execute SQL with no result.
            e.g. `%%spark sql --sample-method sample --sample-fraction 0.1 --max-rows 1000`
        send
            Sending local data to cluster.
            e.g. `%spark send --var-intput localVar --var-type str --var-output remoteVar`
        '''
        args = magic_arguments.parse_argstring(self.spark, line)
        qclouds_args = {
            'region': args.region or configurations.REGION.get(),
            'secretId': args.secret_id or configurations.SECRET_ID.get(),
            'secretKey': args.secret_key or configurations.SECRET_KEY.get(),
            'token': args.token or configurations.TOKEN.get(),
            'endpoint': args.endpoint or configurations.ENDPOINT.get()
        }

        properties_args = {
            'timeout': args.timeout or configurations.SESSION_TIMEOUT.get(),
            'roleArn': args.role_arn or configurations.ROLE_ARN.get(),
            'driverSize': args.driver_size or configurations.DRIVER_SIZE.get(),
            'executorSize': args.executor_size or configurations.EXECUTOR_SIZE.get(),
            'executorNum': args.executor_num or configurations.EXECUTOR_NUM.get(),
            'jars': ','.join(args.jars) or configurations.JARS.get(),
            'pyfiles': ','.join(args.py_files) or configurations.PYFILES.get(),
            'archives': ','.join(args.archives) or configurations.ARCHIVES.get(),
            'files': ','.join(args.files) or configurations.FILES.get(),
            'image': args.image or configurations.IMAGE.get(),
        }

        if properties_args['image']:
            properties_args['image'] = properties_args['image'].strip("'").strip('"')

        if properties_args['jars']:
            properties_args['jars'] = properties_args['jars'].split(',')
        else:
            properties_args['jars'] = []

        if properties_args['pyfiles']:
            properties_args['pyfiles'] = properties_args['pyfiles'].split(',')
        else:
            properties_args['pyfiles'] = []

        if properties_args['archives']:
            properties_args['archives'] = properties_args['archives'].split(',')
        else:
            properties_args['archives'] = []

        if properties_args['files']:
            properties_args['files'] = properties_args['files'].split(',')
        else:
            properties_args['files'] = []

        engine = args.engine or configurations.ENGINE.get()
        if args.language is not None:
            validators.range(args.language, constants.LANGUAGES_SUPPORTED, f"The language is not supported, should be one of {', '.join(constants.LANGUAGES_SUPPORTED)}")
        
        sparkConf = configurations.SPARK_CONF.get()
        if args.conf:
            for eConf in args.conf:
                parts = eConf.split('=')
                if len(parts) != 2:
                    raise exceptions.IllegalInputException(post=f"The '{eConf}' is invalid.")
                sparkConf[parts[0]] = parts[1]
        
        subcommand = "exec"
        if len(args.command) > 0:
            subcommand = args.command[0].lower()

        if subcommand == 'ui':
            return self._config_ui_widget

        elif subcommand == 'config':
            try:
                configurations.setAll(json.loads(cell), args.save)
            except Exception as e:
                LOG.error(e)
                raise exceptions.IllegalInputException(post="The JSON is invalid.")
            
            extra = 'in current kernel'
            if args.save:
                extra = 'globally'

            render.toStdout(f"The configutations have been set {extra}.")

        elif subcommand == 'start':

            self.controller.start_session(
                engine=engine, 
                name=args.name,
                language=args.language or configurations.LANGUAGE.get(), 
                qclouds=qclouds_args,
                properties=properties_args,
                conf=sparkConf,
            )

        elif subcommand == 'stop':
            self.controller.stop_session(name=args.name)
        elif subcommand == 'cleanup':
            pass

        elif subcommand == 'attach':
            self.controller.attach_session(engine, args.name, args.language or configurations.LANGUAGE.get(), args.session_id, qclouds_args)

        elif subcommand == 'detach':
            self.controller.detach_session(args.name)

        elif subcommand == 'session':
            self.controller.render_sessions(args.remote, engine, qclouds=qclouds_args)

        elif subcommand == 'logs':
            self.controller.render_logs(args.name, args.reverse)

        elif subcommand == 'sql':
            return self.execute_sqlquery(args.name, cell, args.var_output, args.sample_method, args.sample_fraction, args.max_rows, args.coerce, args.quiet)
        
        elif subcommand == "send":
            return self.var_to_spark(args.name, args.var_input, args.var_type, args.var_output, args.max_rows)

        elif subcommand == "exec":
            return self.execute_spark(args.name, cell, args.var_output, args.sample_method, args.sample_fraction, args.max_rows, args.coerce, args.language)
        else:
            raise exceptions.CommandNotFoundException


def load_ipython_extension(ip):
    ip.register_magics(RemoteMagics(constants.KERNEL_MODE_IPYTHON, ip))