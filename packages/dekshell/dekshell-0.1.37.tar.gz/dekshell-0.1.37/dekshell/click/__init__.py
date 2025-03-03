import os
import shutil
import sys
import typer
from dektools.output import pprint
from dektools.str import str_escaped
from dektools.shell import shell_wrapper, associate_console_script, get_current_sys_exe
from dektools.typer import command_mixin, command_version
from dektools.plugin import iter_plugins
from ..core import shell_command_batch, shell_command_file, shell_command_file_cd
from ..core.markers.base import MarkerBase
from ..core.contexts import get_all_context
from ..core.markers import generate_markers
from ..core.redirect import redirect_shell_by_path_tree
from ..core.encode import decode_run_str

app = typer.Typer(add_completion=False)
command_version(app, __name__)


def get_argv(index=None):
    if index is not None:
        return sys.argv[index]
    else:
        return sys.argv


def get_kwargs(begin):
    args, kwargs = MarkerBase.cmd2ak(get_argv()[begin:])
    return {f'__arg{i}': arg for i, arg in enumerate(args, 1)} | kwargs


def try_redirect_shell(filepath=None):
    filepath = filepath or os.getcwd()
    path_shell = redirect_shell_by_path_tree(filepath)
    if path_shell:
        shell_wrapper(path_shell + ' ' + ' '.join(sys.argv[1:]))
        return True
    else:
        return False


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rs():
    line = get_argv(2)
    if not try_redirect_shell():
        line = decode_run_str(line)
        shell_command_batch(str_escaped(line), context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def raw_rs():
    line = get_argv(2)
    line = decode_run_str(line)
    shell_command_batch(str_escaped(line), context=get_kwargs(3))


@command_mixin(app)
def rrs(args):
    if not try_redirect_shell():
        shell_command_batch(str_escaped(args))


@command_mixin(app)
def raw_rrs(args):
    shell_command_batch(str_escaped(args))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rf():
    filepath = get_argv(2)
    if not try_redirect_shell(filepath):
        filepath = os.path.normpath(os.path.abspath(filepath))
        shell_command_file_cd(filepath, context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def raw_rf():
    filepath = get_argv(2)
    filepath = os.path.normpath(os.path.abspath(filepath))
    shell_command_file_cd(filepath, context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def rfc():
    filepath = get_argv(2)
    if not try_redirect_shell(filepath):
        shell_command_file(filepath, context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def raw_rfc():
    filepath = get_argv(2)
    shell_command_file(filepath, context=get_kwargs(3))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def r():
    s = get_argv(2)
    if os.path.isfile(s):
        rf()
    else:
        rs()


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def raw_r():
    s = get_argv(2)
    if os.path.isfile(s):
        raw_rf()
    else:
        raw_rs()


@app.command()
def self():
    if not try_redirect_shell():
        pprint(dict(
            context=get_all_context(),
            marker=generate_markers(),
            plugin=[str(x) for x in iter_plugins(__name__)]
        ))


@app.command()
def assoc():
    path_bin = get_current_sys_exe()
    associate_console_script(
        '.pysh', __name__, 'Pysh',
        f"""from dektools.shell import shell_command_nt_as_admin;shell_command_nt_as_admin(r'"{path_bin}" rf %1')""",
        True)
