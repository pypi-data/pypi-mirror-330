import functools
import asyncio
from .baseAdvice import BaseAdvice

class Aspect:
    def __init__(self):
        self.advice = None

    def set_advice(self, advice: BaseAdvice):
        if not isinstance(advice, BaseAdvice):
            raise TypeError("advice must inherit from BaseAdvice.")
        self.advice = advice

    async def _call_advice_async(self, method, *args, **kwargs):
        if method is None:
            return None
        if asyncio.iscoroutinefunction(method):
            return await method(*args, **kwargs)
        else:
            result = method(*args, **kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result

    def _call_advice_sync(self, method, *args, **kwargs):
        if method is None:
            return None
        if asyncio.iscoroutinefunction(method):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(method(*args, **kwargs))
            else:
                return loop.run_until_complete(method(*args, **kwargs))
        else:
            result = method(*args, **kwargs)
            if asyncio.iscoroutine(result):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    return asyncio.run(result)
                else:
                    return loop.run_until_complete(result)
            return result

    async def execute_advice_async(self, func, args, kwargs):
        try:
            if self.advice:
                await self._call_advice_async(self.advice.before, func, *args, **kwargs)

            if self.advice and hasattr(self.advice, "around"):
                result = await self._call_advice_async(self.advice.around, func, *args, **kwargs)
            else:
                result = await func(*args, **kwargs)

            if self.advice:
                await self._call_advice_async(self.advice.after, func, result, *args, **kwargs)
            return result
        except Exception as e:
            if self.advice:
                await self._call_advice_async(self.advice.on_exception, func, e, *args, **kwargs)
            raise e  # 예외를 다시 발생시켜 메인 except로 전달

    def execute_advice_sync(self, func, args, kwargs):
        try:
            if self.advice:
                self._call_advice_sync(self.advice.before, func, *args, **kwargs)

            if self.advice and hasattr(self.advice, "around"):
                result = self._call_advice_sync(self.advice.around, func, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if self.advice:
                after_result = self._call_advice_sync(self.advice.after, func, result, *args, **kwargs)
                if asyncio.iscoroutine(after_result):
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        asyncio.run(after_result)
                    else:
                        loop.create_task(after_result)
            return result
        except Exception as e:
            if self.advice:
                self._call_advice_sync(self.advice.on_exception, func, e, *args, **kwargs)
            raise e  # 예외를 다시 발생시켜 메인 except로 전달

    def apply(self, func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self.execute_advice_async(func, args, kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.execute_advice_sync(func, args, kwargs)
            return wrapper