import functools
import asyncio

from .baseAdvice import BaseAdvice


class Aspect:
    def __init__(self):
        self.advice = None

    def set_advice(self, advice: BaseAdvice):
        """
        Only allows advice that inherits from BaseAdvice.
        """
        if not isinstance(advice, BaseAdvice):
            raise TypeError("advice must inherit from BaseAdvice.")
        self.advice = advice

    def apply(self, func):
        if asyncio.iscoroutinefunction(func):
            return self._apply_async(func)
        else:
            return self._apply_sync(func)

    def _apply_sync(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.advice:
                self.advice.before(func, *args, **kwargs)

            result = None
            try:
                if self.advice:
                    result = self.advice.around(func, *args, **kwargs)
                    if result is None:
                        result = func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                if self.advice:
                    self.advice.after(func, result, *args, **kwargs)
            except Exception as e:
                if self.advice:
                    self.advice.on_exception(func, e, *args, **kwargs)
                raise e

            return result

        return wrapper

    def _apply_async(self, func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if self.advice:
                self.advice.before(func, *args, **kwargs)

            result = None
            try:
                if self.advice:
                    result = await self.advice.around(func, *args, **kwargs)
                    if result is None:
                        result = await func(*args, **kwargs)
                else:
                    result = await func(*args, **kwargs)

                if self.advice:
                    self.advice.after(func, result, *args, **kwargs)
            except Exception as e:
                if self.advice:
                    self.advice.on_exception(func, e, *args, **kwargs)
                raise e

            return result

        return async_wrapper
