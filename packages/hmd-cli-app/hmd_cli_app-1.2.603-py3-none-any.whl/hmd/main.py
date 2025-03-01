from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import HmdAppError
from .controllers.base import Base

import pkgutil
import importlib

# configuration defaults
CONFIG = init_defaults("hmd", "github", "docker")


class HmdApp(App):
    """hmd Command-line Interface primary application."""

    class Meta:
        label = "hmd"

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = ["yaml", "colorlog", "jinja2"]

        # configuration handler
        config_handler = "yaml"

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "jinja2"

        # handlers are registered in main()


class HmdAppTest(TestApp, HmdApp):
    """A sub-class of HmdApp that is better suited for testing."""

    class Meta:
        label = "hmd"
        handlers = [Base]


def main():
    handlers = [Base]
    # add all controller objects from hmd_cli packages
    for _, name, _ in pkgutil.iter_modules():
        if name.startswith("hmd_cli"):
            try:
                module = importlib.import_module(f"{name}.controller")
                module_controllers = filter(
                    lambda x: x != "Controller" and x.endswith("Controller"),
                    dir(module),
                )
                for module_controller in module_controllers:
                    handlers.append(getattr(module, module_controller))
            except ModuleNotFoundError:
                pass
        pass

    with HmdApp(**{"handlers": handlers}) as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except HmdAppError as e:
            print("HmdAppError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0

        except Exception as e:
            print(f"Error: {e.args[0]}")
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()


if __name__ == "__main__":
    main()
