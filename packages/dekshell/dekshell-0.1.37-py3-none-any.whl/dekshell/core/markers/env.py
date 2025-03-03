import os
from .base import MarkerBase


class MarkerEnvBase(MarkerBase):

    def exec(self, env, command, marker_node, marker_set):
        argv = self.split(command, True)
        args, _ = self.cmd2ak(argv[1:3])
        args, _ = self.var_map_batch(env, *args)
        environ = self.get_environ(env)
        if len(args) == 1:
            environ.pop(args[0], None)
        elif len(args) == 2:
            environ[args[0]] = args[1]
        else:
            environ.clear()

    def get_environ(self, env):
        raise NotImplementedError


class EnvMarker(MarkerEnvBase):
    tag_head = "@env"

    def get_environ(self, env):
        return os.environ


class EnvShellMarker(MarkerEnvBase):
    tag_head = "@envs"

    def get_environ(self, env):
        return env.environ_pointer
