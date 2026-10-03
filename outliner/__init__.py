# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""JA Tree for IngeTrazo 0.5.7, extension API 2."""
from .i18n import tr

__version__ = "0.1.0"


def setup(app):
    if getattr(app, "api_version", 0) < 2:
        raise RuntimeError(tr("JA Tree requiere la API de extensiones 2 de IngeTrazo."))
    controllers = getattr(app.window, "_outliner_controllers", None)
    if controllers is None:
        controllers = app.window._outliner_controllers = {}
    if app.key not in controllers:
        from .controller import Controller
        controller = Controller(app)
        controller.install()
        controllers[app.key] = controller
    return controllers[app.key]
