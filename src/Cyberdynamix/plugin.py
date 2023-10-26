import abc


class Plugin(metaclass=abc.ABCMeta):
    """
    插件抽象类
    """

    @abc.abstractmethod
    def run(self):
        """
        插件运行方法
        """
        pass


def create_plugin(plugin_cls, **kwargs):
    return plugin_cls(**kwargs)
