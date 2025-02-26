from ipywidgets import widgets 
from tdlc.utils import render, configurations, log,constants
from tdlc.engines import controllers


LOG = log.getLogger('Widget')


class CreateSessionWidget(widgets.VBox):


    def __init__(self, controller: controllers.EngineSessionController, **kwargs):
        super().__init__(**kwargs)

        self.controller = controller

        self.children = []

        self._widget_session_name_text = widgets.Text(
            description="会话名称*",
            name='session_name',
            placeholder="请输入会话名称",
            value=self.controller.build_local_session_name(),
        )

        self._widget_region_text = widgets.Text(
            description="地域*", 
            name="region",
            placeholder="请输入地域",
            value=configurations.REGION.get(),
        )


        self._widget_secret_id_text = widgets.Text(
            description="Secret Id*",
            name='secret_id',
            placeholder="请输入腾讯云 Secret Id",
            value=configurations.SECRET_ID.get()
        )
        self._widget_secret_key_text = widgets.Text(
            description="Secret Key*",
            name='secret_key',
            placeholder="请输入腾讯云 Secret Key",
            value=configurations.SECRET_KEY.get(),
        )

        self._widget_engine_hbox = widgets.HBox([
            widgets.Text(
                description="Engine*",
                name='engine',
                placeholder="请输入批作业引擎名称",
                value=configurations.ENGINE.get()
            )
        , widgets.Label("引擎名称")])

        self._widget_role_arn_text = widgets.Text(
            description="RoleArn",
            name="role_arn",
            placeholder="请输入 roleArn",
            value=configurations.ROLE_ARN.get()
        )
        
        self._widget_py_files_hbox = widgets.HBox([widgets.Text(
            description="--py-files",
            name="py_files",
            placeholder="请填写 python 依赖包",
            value=configurations.PYFILES.get()
        ), widgets.Label("[可选] python依赖文件, 多个文件以\",\"分割, 只支持 cosn:// 路径")])

        self._widget_archives_hbox = widgets.HBox([widgets.Text(
            description="--archives",
            name="archives",
            placeholder="请填写 archives 包路径",
            value=configurations.PYFILES.get()
        ), widgets.Label("[可选] archives 包, 多个文件以\",\"分割, 只支持 cosn:// 路径")])

        self._widget_extraconf_hbox = widgets.HBox([
            widgets.Textarea(
                description="引擎配置",
                name="extraconf",
                placeholder="请输入引擎配置"
            )
        ])

        self._widget_submit_button = widgets.Button(
            description = "确定"
        )
        self._widget_save_button = widgets.Button(
            description = "保存"
        )

        self._widget_buttons = widgets.HBox([
            self._widget_submit_button,
            self._widget_save_button,

        ])

        self._widget_submit_button.on_click(lambda x: x.parent_widget.on_submit_click())
        self._widget_save_button.on_click(lambda x: x.parent_widget.on_save_click())

        self.children = [
                self._widget_session_name_text, 
                self._widget_region_text, 
                self._widget_secret_id_text, 
                self._widget_secret_key_text, 
                self._widget_engine_hbox, 
                self._widget_role_arn_text,
                self._widget_py_files_hbox,
                self._widget_archives_hbox,
                self._widget_extraconf_hbox,
                self._widget_buttons,
                ]

        for child in self.children:
            child.parent_widget = self
        
        self._widget_submit_button.parent_widget = self
        self._widget_save_button.parent_widget = self
    


    def on_submit_click(self):

        name = self._widget_session_name_text.value
        region =  self._widget_region_text.value
        secret_id = self._widget_secret_id_text.value
        secret_key = self._widget_secret_key_text.value
        engine = self._widget_engine_hbox.children[0].value
        role_arn = self._widget_role_arn_text.value

        qclouds_args = {
            'region': region,
            'secretId': secret_id,
            'secretKey': secret_key,
            'token': None,
            'endpoint': configurations.ENDPOINT.get(),
        }

        properties_args = {
            'timeout': configurations.SESSION_TIMEOUT.get(),
            'roleArn': role_arn,
            'driverSize': constants.CU_SIZE_SMALL,
            'executorSize': constants.CU_SIZE_SMALL,
            'executorNum': 0,
            'jars': None,
            'pyfiles': None,
            'archives':None,
        }

        self.controller.start_session(engine, name, constants.LANGUAGE_PYTHON, qclouds_args, properties_args, {})


    
    def on_save_click(self):

        configurations.REGION.set(self._widget_region_text.value, True)
        configurations.SECRET_ID.set(self._widget_secret_id_text.value, True)
        configurations.SECRET_KEY.set(self._widget_secret_key_text.value, True)
        configurations.ENGINE.set(self._widget_engine_hbox.children[0].value, True)
        configurations.ROLE_ARN.set(self._widget_role_arn_text.value, True)
        configurations.PYFILES.set(self._widget_py_files_hbox.children[0].value, True)
        configurations.ARCHIVES.set(self._widget_archives_hbox.children[0].value, True)
        configurations.EXTRACONF.set(self._widget_extraconf_hbox.children[0].value, True)

