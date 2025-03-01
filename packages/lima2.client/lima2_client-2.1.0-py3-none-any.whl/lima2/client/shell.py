#!/usr/bin/env python
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT license. See LICENSE for more info.


"""Lima2 client interactive shell

Given a Tango server at $TANGO_HOST and the l2c_config.yaml file, launch an ipython interactive
shell with a Client object initialized and some example control/acquisition/processing parameters.
"""

# Apply gevent monkeypatch before any other imports
# This enables async actions to run in the background (e.g. state machine)
import gevent.monkey

gevent.monkey.patch_all(thread=False)

from typing import Literal
from beartype import beartype
from functools import partial
from uuid import uuid1
from lima2.client.client import Client
import tango


@beartype
def get_proc_params(pipeline: Literal["Legacy", "Smx", "Xpcs"]) -> dict:
    """Get the default processing params for a pipeline"""
    from lima2.client import pipelines

    proc_class = pipelines.get_class(f"LimaProcessing{pipeline}")
    proc_params: dict = proc_class.params_default

    return proc_params


def run_acquisition(
    c: Client,
    ctl_params: dict,
    rcv_params: dict,
    proc_params: dict,
    nb_frames: int,
    expo_time: float,
    latency_time: float,
    trigger_mode: str = "internal",
):
    ctl_params["acq"]["trigger_mode"] = trigger_mode
    ctl_params["acq"]["nb_frames"] = nb_frames
    rcv_params["acq"]["nb_frames"] = nb_frames
    ctl_params["acq"]["expo_time"] = int(expo_time * 1e6)
    rcv_params["acq"]["expo_time"] = int(expo_time * 1e6)
    ctl_params["acq"]["latency_time"] = int(latency_time * 1e6)
    rcv_params["acq"]["latency_time"] = int(latency_time * 1e6)
    proc_params["saving"]["nb_frames_per_file"] = 10
    proc_params["saving"]["file_exists_policy"] = "overwrite"

    c.prepare_acq(uuid1(), ctl_params, rcv_params, proc_params)
    c.start_acq()


def main():
    import copy
    import logging
    import os

    import tango as tg

    try:
        from IPython import start_ipython
    except ImportError as e:
        raise ImportError(
            f"Dependency '{e.name}' not found. To fix:\n"
            "$ pip install lima2-client[shell]"
        ) from e

    from traitlets.config import Config

    import lima2.client as l2c

    if not os.getenv("TANGO_HOST"):
        raise ValueError("TANGO_HOST must be exported")

    logging.basicConfig(level=logging.INFO)

    #############
    # Populate user namespace

    config_filename = "l2c_config.yaml"
    try:
        c = Client.from_yaml(config_filename=config_filename)
    except tango.ConnectionFailed as e:
        raise RuntimeError(
            f"Could not establish a connection to the Tango server at {os.getenv('TANGO_HOST')}."
        ) from e
    except tango.DevFailed as e:
        raise RuntimeError(
            f"Device connection failed. Please check your configuration in '{config_filename}'.\n"
            "See error above for details."
        ) from e

    # Some sensible default parameters
    proc_params = get_proc_params("Legacy")
    proc_params["saving"]["file_exists_policy"] = "overwrite"

    ctl_params = c.params_default[c.control.name()]["acq_params"]

    rcv_params = copy.deepcopy(ctl_params)

    user_namespace = {
        "tg": tg,
        "l2c": l2c,
        "c": c,
        "get_proc_params": get_proc_params,
        "uuid1": uuid1,
        "ctl_params": ctl_params,
        "rcv_params": rcv_params,
        "proc_params": proc_params,
        "run_acquisition": partial(
            run_acquisition, c, ctl_params, rcv_params, proc_params
        ),
    }

    #############
    # IPython config
    config = Config()

    # Show defined symbols on ipython banner
    config.TerminalInteractiveShell.banner2 = (
        "\n"
        "===============\n"
        "| Lima2 shell |\n"
        "===============\n\n"
        f"Defined symbols: {[key for key in user_namespace]}\n"
        "Run an acquisition as follows:\n"
        " c.detector.prepare_acq(uuid1(), ctl_params, rcv_params, proc_params)\n"
        " c.detector.start_acq()\n"
    )

    # Enable autoreload
    config.InteractiveShellApp.extensions = ["autoreload"]
    config.InteractiveShellApp.exec_lines = [r"%autoreload all"]

    start_ipython(argv=[], user_ns=user_namespace, config=config)


if __name__ == "__main__":
    import sys

    sys.exit(main())
