"""
Create by yy on 2019-07-25
"""
from .helper_config import HelperConfig


class Helper(HelperConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_config(self, config=None):
        self.config.from_object(config)
