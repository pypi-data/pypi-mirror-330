from .base import MarkerBase


class DefaultMarker(MarkerBase):
    tag_head = "@default"

    def exec(self, env, command, marker_node, marker_set):
        args = self.split_raw(command, 2)
        var_name = self.get_item(args, 1)
        if var_name not in env.context:
            self.set_var(env, args, 1, self.eval(env, args[2]))
