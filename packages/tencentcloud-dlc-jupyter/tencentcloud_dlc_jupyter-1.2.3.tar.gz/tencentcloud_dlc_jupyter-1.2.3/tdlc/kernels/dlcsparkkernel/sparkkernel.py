from tdlc.utils import log, constants
from tdlc.kernels import kernelbase

import tdlc


class SparkKernel(kernelbase.Kernelbase):

    implementation = "Spark"
    implementation_version = tdlc.VERSION
    language = constants.LANGUAGE_SCALA
    language_version = "0.1"
    language_info = {
        "name": "scala",
        "mimetype": "text/x-scala",
        "codemirror_mode": "text/x-scala",
        "file_extension": ".sc",
        "pygments_lexer": "scala",
    }


    banner = 'DLC Spark Kernel'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SparkKernel)

