"""
author songjie
"""
from .config import Config
from .helper_context import HelperContext
from .db import DBConfig


class HelperConfig(HelperContext):
    config_class = Config
    DEFAULT_CONFIG = {
        "MYSQL_DATABASE": "mysql",
        "MYSQL_USERNAME": "root",
        "MYSQL_PASSWORD": "root",
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_TABLE_PREFIX": ""
    }

    def __init__(self, **kwargs):
        super().__init__()
        self._root_path = None
        self.config = self.make_config()
        self._db = DBConfig()

    def __del__(self):
        with self.auto_handle_exception():
            self._db.close()

    @property
    def db(self):
        return self._db

    def init_db(self, config=None):
        """
        初始化数据库设置
        init db config
        :param config:
        :return:
        """
        if not config:
            config = "MYSQL_CONFIG"
        self._db = DBConfig(
            username=self.config[config].setdefault("MYSQL_USERNAME", HelperConfig.DEFAULT_CONFIG["MYSQL_USERNAME"]),
            password=self.config[config].setdefault("MYSQL_PASSWORD",
                                                    HelperConfig.DEFAULT_CONFIG["MYSQL_PASSWORD"]),
            database=self.config[config].setdefault("MYSQL_DATABASE",
                                                    HelperConfig.DEFAULT_CONFIG["MYSQL_DATABASE"]),
            host=self.config[config].setdefault("MYSQL_HOST", HelperConfig.DEFAULT_CONFIG["MYSQL_HOST"]),
            port=self.config[config].setdefault("MYSQL_PORT", HelperConfig.DEFAULT_CONFIG["MYSQL_PORT"]),
            table_prefix=self.config[config].setdefault("MYSQL_TABLE_PREFIX",
                                                        HelperConfig.DEFAULT_CONFIG["MYSQL_TABLE_PREFIX"])
        )
        return self._db

    def make_config(self):
        """
        构造配置项
        :return:
        """
        root_path = self._root_path
        return self.config_class(root_path=root_path, defaults=HelperConfig.DEFAULT_CONFIG)
