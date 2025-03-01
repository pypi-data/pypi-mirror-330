######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.1                                                                                 #
# Generated on 2025-02-28T22:52:51.064623                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

