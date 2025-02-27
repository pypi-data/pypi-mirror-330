# AOPHelper – Python을 위한 강력한 AOP 라이브러리  

**AOPHelper**는 Python에서 **Aspect-Oriented Programming(AOP, 관점 지향 프로그래밍)**을 쉽게 적용할 수 있도록 도와주는 라이브러리입니다.  
`@Aspect` 데코레이터를 사용하여 **로깅, 성능 측정, 예외 처리** 등을 간편하게 적용하세요!

---

## 🚀 **설치 방법**
```sh
pip install aophelper
```

🔥 빠른 시작

✅ 기본 AOP 적용 예제
```python
from aophelper import Aspect, BaseAdvice

class LoggingAdvice(BaseAdvice):
    def before(self, func, *args, **kwargs):
        print(f"🚀 {func.__name__} 실행 시작!")

    def after(self, func, result, *args, **kwargs):
        print(f"✅ {func.__name__} 실행 완료! 결과: {result}")

aspect = Aspect()
aspect.set_advice(LoggingAdvice())

@aspect.apply
def add(x, y):
    return x + y

print(add(10, 20))
```

출력 결과

🚀 add 실행 시작!
✅ add 실행 완료! 결과: 30


## 📌 주요 기능

기능	설명
- ✅ before()	함수 실행 전에 수행할 작업 추가
- ⚡ around()	함수 실행 시간 측정 및 실행 방식 제어 가능
- 🛑 on_exception()	예외 발생 시 자동 처리 및 로깅 가능
- 📢 after()	함수 실행 후 결과를 후처리 가능
- 🔄 비동기 지원	async def 함수에도 AOP 적용 가능

### 🛠 각 기능의 예제 코드

#### ✅ before() – 함수 실행 전에 동작 추가
```python
from aophelper import Aspect, BaseAdvice

class MyAdvice(BaseAdvice):
    def before(self, func, *args, **kwargs):
        print(f"{func.__name__} 실행 전! 매개변수: {args}, {kwargs}")

aspect = Aspect()
aspect.set_advice(MyAdvice())

@aspect.apply
def greet(name):
    print(f"안녕하세요, {name}님!")

greet("Alice")
```
**출력 결과**
```
greet 실행 전! 매개변수: ('Alice',), {}
안녕하세요, Alice님!
```
### ⚡ around() – 실행 시간 측정 및 동작 변경
```python
import time

class TimerAdvice(BaseAdvice):
    def around(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 실행 시간: {end - start:.4f}초")
        return result

aspect.set_advice(TimerAdvice())

@aspect.apply
def slow_function():
    time.sleep(2)
    print("작업 완료!")

slow_function()
```
**출력 결과**

```
작업 완료!
slow_function 실행 시간: 2.0050초
```

### 🛑 on_exception() – 예외 발생 시 자동 처리

```python
class ErrorHandlerAdvice(BaseAdvice):
    def on_exception(self, func, exception, *args, **kwargs):
        print(f"{func.__name__}에서 오류 발생: {exception}")

aspect.set_advice(ErrorHandlerAdvice())

@aspect.apply
def error_function():
    raise ValueError("잘못된 값!")

error_function()
```

**출력 결과**
```
error_function에서 오류 발생: 잘못된 값!
```

### 📢 after() – 실행 후 후처리
```python
class PostProcessingAdvice(BaseAdvice):
    def after(self, func, result, *args, **kwargs):
        print(f"{func.__name__} 실행 완료! 결과: {result}")

aspect.set_advice(PostProcessingAdvice())

@aspect.apply
def multiply(x, y):
    return x * y

print(multiply(5, 10))
```

**출력 결과**
```
multiply 실행 완료! 결과: 50
50
```

### 🔄 비동기 함수(async def) 지원

AOPHelper는 async def 함수에도 적용할 수 있습니다.

```python
import asyncio

class AsyncAdvice(BaseAdvice):
    async def before(self, func, *args, **kwargs):
        print(f"(비동기) {func.__name__} 실행 전!")

aspect.set_advice(AsyncAdvice())

@aspect.apply
async def async_task():
    await asyncio.sleep(1)
    print("비동기 작업 완료!")

asyncio.run(async_task())
```
**출력 결과**
```
(비동기) async_task 실행 전!
비동기 작업 완료!
```

이제 더 강력한 AOP 기능을 활용해 보세요! 🚀

## 기여 방법
버그 리포트나 기능 제안은 **GitHub Issues**에 남겨주세요
