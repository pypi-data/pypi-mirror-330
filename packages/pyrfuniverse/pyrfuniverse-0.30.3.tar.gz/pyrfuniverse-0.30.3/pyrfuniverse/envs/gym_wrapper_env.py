from typing import Any, SupportsFloat
import pyrfuniverse.attributes as attr
from pyrfuniverse.envs.base_env import RFUniverseBaseEnv

try:
    import gymnasium as gym
except ImportError:
    print("This feature requires gymnasium, please install with `pip install gymnasium`")
    raise


class RFUniverseGymWrapper(RFUniverseBaseEnv, gym.Env):
    """
    RFUniverse base environment with Gym class.

    Args:
        executable_file: Str, the absolute path of Unity executable file. None for last used executable file; "@editor" for using Unity Editor.
        scene_file: Str, the absolute path of Unity scene JSON file. All JSON files locate at `StraemingAssets/SceneData` by default.
        assets: List, the list of pre-load assets. All assets in the list will be pre-loaded in Unity when the environment is initialized, which will save time during instanciating.
        graphics: Bool, True for showing GUI and False for headless mode.
        port: Int, the port for communication.
        proc_id: Int, the process id for the Unity environment. 0 for the first process, 1 for the second process, and so on.
        log_level: Int, the log level for Unity environment. 0 for no log, 1 for errors logs, 2 for warnings and errors, 3 for all only.
        ext_attr: List, the list of extended attributes. All extended attributes will be added to the environment.
        check_version: Bool, True for checking the version of the Unity environment and the pyrfuniverse library. False for not checking the version.
    """

    def __init__(
            self,
            executable_file: str = None,
            scene_file: str = None,
            assets: list = [],
            graphics: bool = True,
            port: int = 5004,
            proc_id=0,
            log_level=1,
            ext_attr: list[type(attr.BaseAttr)] = [],
            check_version: bool = True,
            communication_backend: str = "tcp",
    ):
        RFUniverseBaseEnv.__init__(
            self,
            executable_file=executable_file,
            scene_file=scene_file,
            assets=assets,
            graphics=graphics,
            port=port,
            proc_id=proc_id,
            log_level=log_level,
            ext_attr=ext_attr,
            check_version=check_version,
            communication_backend=communication_backend,
        )

    def env_step(self, count: int = 1, simulate: bool = True, collect: bool = True):
        """
        Send the messages of called functions to Unity and simulate for a step, then accept the data from Unity.

        Args:
            count: The number of steps for executing Unity simulation.
            simulate: Simulate Physics
            collect: Collect Data
        """
        RFUniverseBaseEnv.step(self, count)

    def step(self, action: gym.core.ActType) -> tuple[gym.core.ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """
        Gym step.

        Args:
            action: gym action.
        """
        return gym.Env.step(self, action)

    def env_close(self):
        """
        Close the environment
        """
        RFUniverseBaseEnv.close(self)

    def close(self):
        """
        Close gym
        """
        gym.Env.close(self)
