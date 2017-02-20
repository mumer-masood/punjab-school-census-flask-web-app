# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from schoolCensus.app import create_app
from schoolCensus.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag(default=False) else ProdConfig

app = create_app(CONFIG)

if __name__ == "__main__":
    app.run()