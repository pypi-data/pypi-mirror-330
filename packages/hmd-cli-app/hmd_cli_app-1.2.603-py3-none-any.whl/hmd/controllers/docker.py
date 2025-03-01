import os

from cement import Controller, ex
from importlib.metadata import version
from ..core.exc import HmdAppError
from hmd_cli_tools import get_version

VERSION_BANNER = """
hmd docker versionx: {}
"""


class DockerController(Controller):
    class Meta:
        label = "docker"

        stacked_type = "nested"
        stacked_on = "base"

        # text displayed at the top of --help output
        description = "Build and deploy docker imagesx"

        arguments = (
            (
                ["-v", "--version"],
                {
                    "help": "Display the version of the docker commandx.",
                    "action": "version",
                    "version": VERSION_BANNER.format(version("hmd_cli_docker")),
                },
            ),
        )

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="build a docker image",
        arguments=[
            (["-n", "--name"], {"action": "store", "dest": "name", "required": False}),
            (
                ["--build-args"],
                {
                    "action": "store",
                    "dest": "build_args",
                    "required": False,
                    "nargs": "*",
                },
            ),
        ],
    )
    def build(self):
        args = {}
        name = self.app.pargs.name
        if not name:
            name = os.path.basename(os.getcwd())
        args.update({"name": name})

        build_args = self.app.pargs.build_args
        if build_args:
            args.update({"build_args": dict([v.split(":") for v in build_args])})

        version = get_version()
        args.update({"version": version})
        import hmd_cli_docker

        result = hmd_cli_docker.build(**args)
        for l in result:
            print(l)

    @ex(
        help="deploy a docker image",
        arguments=[
            (["-n", "--name"], {"action": "store", "dest": "name", "required": False})
        ],
    )
    def deploy(self):
        print("hmd docker deploy")
        args = {}
        name = self.app.pargs.name
        if not name:
            name = os.path.basename(os.getcwd())
        args.update({"name": name})

        docker_username = self.app.config.get("docker", "username")
        docker_password = self.app.config.get("docker", "password")
        version = get_version()

        if not docker_username or not docker_password:
            raise HmdAppError(
                'Application config properties "docker.username" and "docker.pat" must be set.'
            )
        args.update(
            {
                "docker_username": docker_username,
                "docker_password": docker_password,
                "version": version,
            }
        )

        import hmd_cli_docker

        hmd_cli_docker.deploy(**args)
