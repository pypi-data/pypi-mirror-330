﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .command_failed_exception import CommandFailedException


class RemoteModeException(CommandFailedException):
    """
    Thrown when a command is rejected because the device is in EtherCAT Control (remote) mode.
    """
