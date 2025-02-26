from tdlc.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tdlc.tencentcloud.dlc.v20210125 import dlc_client
from tdlc.utils import log

import tdlc
import json


LOG = log.getLogger("QClient")


class QClient(dlc_client.DlcClient):

    RETRY_TIMES = 3

    def __init__(self, credential, region, profile=None):
        super().__init__(credential, region, profile)


    def call(self, action, params, options=None, headers=None):

        retry = 0

        if headers is None:
            headers = {}

        headers.setdefault('_v_', f'nb-{tdlc.VERSION}')

        err = None

        # 网络异常
        while retry < self.RETRY_TIMES:
            LOG.debug(f"Calling (retry={retry}) {action} with  args: {params}")
            retry += 1
            try:
                body = super().call(action, params, options, headers)
                LOG.debug(f"Calling {action} with response: {body}")

                # hack error message
                r = json.loads(body)
                if 'Error' in r['Response'] and 'Detail' in r['Response']['Error']:

                    try:
                        o = json.loads(r['Response']['Error']['Detail'])
                        r['Response']['Error']['Message'] = o['errMsg']
                        return json.dumps(r)
                    except Exception as e:
                        LOG.warning(e)
                    
                return body
            except Exception as e:
                err = e

        if err is not None:
            raise err

        return body
            