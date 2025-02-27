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
        return self._apply_async(func) if asyncio.iscoroutinefunction(func) else self._apply_sync(func)

    def execute_advice(self, func, args, kwargs, is_async=False):
        """
        Execute the before/after/on_exception advices while handling sync & async functions.
        """
        if self.advice:
            self.advice.before(func, *args, **kwargs)

        result = None
        try:
            if self.advice and hasattr(self.advice, "around"):
                if is_async:
                    result = asyncio.ensure_future(self.advice.around(func, *args, **kwargs))
                else:
                    result = self.advice.around(func, *args, **kwargs)

            if result is None:
                result = func(*args, **kwargs) if not is_async else asyncio.ensure_future(func(*args, **kwargs))

            if self.advice:
                self.advice.after(func, result, *args, **kwargs)

        except Exception as e:
            if self.advice:
                self.advice.on_exception(func, e, *args, **kwargs)
            return None  # Stop re-raising the exception

        return result

    def _apply_sync(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.execute_advice(func, args, kwargs, is_async=False)

        return wrapper

    def _apply_async(self, func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await self.execute_advice(func, args, kwargs, is_async=True)

        return async_wrapper