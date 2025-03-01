import os
import sys
from importlib.metadata import version

from cement import Controller
from yaml import safe_load

from hmd_cli_tools import get_version
from hmd_cli_tools.hmd_cli_tools import convert_args_to_command_line

VERSION_BANNER = """
hmd version: {}
"""


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "Support tools for the hmd data platform."

        # controller level arguments. ex: 'hmd --version'
        arguments = [
            (
                ["-v", "--version"],
                {
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd-cli-app")),
                },
            ),
            (
                ["-rn", "--repo-name"],
                {
                    "action": "store",
                    "dest": "repo_name",
                    "required": False,
                    "default": os.environ.get("HMD_REPO_NAME"),
                },
            ),
            (
                ["-rv", "--repo-version"],
                {
                    "action": "store",
                    "dest": "repo_version",
                    "required": False,
                    "default": os.environ.get("HMD_REPO_VERSION"),
                },
            ),
            (
                ["-hr", "--hmd-region"],
                {
                    "action": "store",
                    "dest": "hmd_region",
                    "required": False,
                    "default": os.environ.get("HMD_REGION", "reg1"),
                },
            ),
            (
                ["-cc", "--customer-code"],
                {
                    "action": "store",
                    "dest": "customer_code",
                    "required": False,
                    "default": os.environ.get("HMD_CUSTOMER_CODE"),
                },
            ),
            (
                ["-p", "--profile"],
                {"action": "store", "dest": "profile", "required": False},
            ),
        ]

        epilog = "hmd <technology> <lifecycle-phase>"

    def _post_argument_parsing(self):
        if not self.app.pargs.repo_name:
            self.app.pargs.repo_name = os.path.basename(os.getcwd())

        if not self.app.pargs.repo_version:
            try:
                self.app.pargs.repo_version = get_version()
            except Exception as e:
                pass

        if hasattr(self.app.pargs, "config_file") and self.app.pargs.config_file:
            config_file = self.app.pargs.config_file
            if config_file == "STDIN":
                self.app.pargs.config_values = safe_load(sys.stdin)
            else:
                with open(config_file, "r") as fl:
                    self.app.pargs.config_values = safe_load(fl)
        else:
            self.app.pargs.config_values = {}

        sub_commands = getattr(self.app.pargs, "__dispatch__", "").split(".")
        sub_commands = [sc.replace("_", "-") for sc in sub_commands]
        command_line = ["hmd"] + convert_args_to_command_line(
            self.app.args, self.app.pargs, sub_commands
        )
        if self.app.debug:
            print(" ".join(command_line))

    def _default(self):
        self.app.args.print_help()
