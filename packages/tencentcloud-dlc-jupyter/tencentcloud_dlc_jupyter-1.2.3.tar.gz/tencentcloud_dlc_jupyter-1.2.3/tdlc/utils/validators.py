

from tdlc import exceptions
from tdlc.utils import constants, log

LOG = log.getLogger("Validator")


def required(arg, message_if_error):
    if not arg:
        raise exceptions.ValidationException(message=message_if_error)
    return True


def range(arg, ranges, message_if_error):
    if arg not in ranges:
        raise exceptions.ValidationException(message=message_if_error)
    return True


def checkQcloudArgs(args):
    required(args["region"], "Region is required")
    required(args["secretId"], "SercretId is required")
    required(args["secretKey"], "SecretKey is required")
    return True

def checkPropertyArgs(args):

    required(args["roleArn"], "RoleArn is required, please provide with '--role-arn {role-arn}'")

    range(args["driverSize"], constants.CU_SIZE_SUPPORTED, f"DriverSize is invalid, available options are {constants.CU_SIZE_SUPPORTED}")
    range(args["executorSize"], constants.CU_SIZE_SUPPORTED, f"ExecutorSize is invalid, available options are {constants.CU_SIZE_SUPPORTED}")

    return True


