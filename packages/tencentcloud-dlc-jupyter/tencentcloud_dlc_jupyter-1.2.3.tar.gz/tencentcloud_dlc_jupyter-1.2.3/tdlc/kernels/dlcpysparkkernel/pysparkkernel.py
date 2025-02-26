from tdlc.utils import constants
from tdlc.utils import log
from tdlc.kernels import kernelbase

import tdlc


class PySparkKernel(kernelbase.Kernelbase):

    implementation = "PySpark"
    implementation_version = tdlc.VERSION
    language = constants.LANGUAGE_PYTHON
    language_info = {
        'name': 'pyspark',
        'mimetype': 'text/x-python',
        "codemirror_mode": {"name": "python", "version": 3},
        "file_extension": ".py",
        "pygments_lexer": "python3",
    }

    banner = 'DLC PySpark Kernel'

    def __init__(self, **kwargs):
         super().__init__(**kwargs)



if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PySparkKernel)