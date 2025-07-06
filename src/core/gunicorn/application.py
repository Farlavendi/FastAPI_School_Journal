from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(
        self,
        application: FastAPI,
        options: dict | None = None,
    ):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self):
        return self.application

    @property
    def config_options(self) -> dict:
        return {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }

    def load_config(self) -> None:
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
