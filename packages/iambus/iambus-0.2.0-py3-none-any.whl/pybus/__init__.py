import importlib
import sys
import types
import warnings


class PybusRedirector(types.ModuleType):
    """Module interceptor."""

    def __init__(self):
        super().__init__("pybus")
        self._iambus = importlib.import_module("iambus")

    def __getattr__(self, name):
        warnings.warn(
            "The 'pybus' package name is deprecated and will be removed in a future release. Use 'iambus' instead.",
            FutureWarning,
            stacklevel=2
        )

        try:
            return getattr(self._iambus, name)
        except AttributeError:
            return importlib.import_module(f"iambus.{name}")

    def __dir__(self):
        return dir(self._iambus)


sys.modules["pybus"] = PybusRedirector()
