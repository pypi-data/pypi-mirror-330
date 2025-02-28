from abc import ABC, abstractmethod


class BaseAdvice(ABC):
    """
    AOP Advice Interface
    """

    @abstractmethod
    def before(self, func, *args, **kwargs):
        pass

    @abstractmethod
    def after(self, func, result, *args, **kwargs):
        pass

    @abstractmethod
    def around(self, func, *args, **kwargs):
        pass

    @abstractmethod
    def on_exception(self, func, exception, *args, **kwargs):
        pass