import functools
import asyncio
from .baseAdvice import BaseAdvice

class Aspect:
    def __init__(self):
        self.advice = None

    def set_advice(self, advice: BaseAdvice):
        """
        BaseAdvice를 상속한 인스턴스만 허용합니다.
        """
        if not isinstance(advice, BaseAdvice):
            raise TypeError("advice must inherit from BaseAdvice.")
        self.advice = advice

    async def _call_advice_async(self, method, *args, **kwargs):
        """
        비동기 컨텍스트에서 advice 메소드를 호출합니다.
        메소드가 코루틴 함수이면 await, 아니면 일반 호출 후 반환값이 코루틴이면 await합니다.
        """
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
        """
        동기 컨텍스트에서 advice 메소드를 호출합니다.
        메소드가 코루틴 함수이면 이벤트 루프를 이용해 실행하고, 그렇지 않으면 바로 실행합니다.
        """
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
        """
        비동기 함수 실행 전/후 및 예외 처리 advice를 호출합니다.
        """
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
            return None  # 예외 발생 시 None 반환 또는 필요 시 재전파

    def execute_advice_sync(self, func, args, kwargs):
        """
        동기 함수 실행 전/후 및 예외 처리 advice를 호출합니다.
        """
        try:
            if self.advice:
                self._call_advice_sync(self.advice.before, func, *args, **kwargs)

            if self.advice and hasattr(self.advice, "around"):
                result = self._call_advice_sync(self.advice.around, func, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if self.advice:
                after_result = self._call_advice_sync(self.advice.after, func, result, *args, **kwargs)
                # after가 코루틴이면 백그라운드에서 실행 (이벤트 루프가 존재하는 경우)
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
            return None  # 예외 발생 시 None 반환 또는 필요 시 재전파

    def apply(self, func):
        """
        함수에 advice를 적용하는 데코레이터를 반환합니다.
        함수가 비동기이면 async wrapper, 동기이면 일반 wrapper를 사용합니다.
        """
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