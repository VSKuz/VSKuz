import asyncio

class AsyncCounter:
    def __init__(self):
        self._value = 0
        self._lock = asyncio.Lock()

    async def increment(self):
        async with self._lock:
            self._value += 1
            print(f"Incremented: {self._value}")

    async def decrement(self):
        async with self._lock:
            self._value -= 1
            print(f"Decremented: {self._value}")

    async def get_value(self):
        async with self._lock:
            return self._value

async def worker(counter, increments, decrements):
    for _ in range(increments):
        await counter.increment()
    for _ in range(decrements):
        await counter.decrement()

async def main():
    counter = AsyncCounter()
    tasks = [
        worker(counter, 5, 3),
        worker(counter, 2, 4),
        worker(counter, 3, 3)
    ]
    await asyncio.gather(*tasks)
    final_value = await counter.get_value()
    print(f"Final counter value: {final_value}")

if __name__ == "__main__":
    asyncio.run(main())

# Объяснение:
#1. **AsyncCounter**: Это класс, который инкапсулирует счетчик и обеспечивает синхронный доступ к нему с помощью `asyncio.Lock`.
#2. **increment и decrement**: Эти асинхронные методы изменяют значение счетчика. Они используют `async with self._lock` для обеспечения того, что только одна задача может изменять значение счетчика в любой момент времени.
#3. **get_value**: Этот метод возвращает текущее значение счетчика. Он также использует блокировку для обеспечения согласованности данных.
#4. **worker**: Это функция, которая выполняет несколько инкрементов и декрементов счетчика. Она может быть запущена как отдельная задача.
#5. **main**: В этой функции создается экземпляр `AsyncCounter` и запускаются несколько задач, которые изменяют счетчик параллельно. В конце выводится итоговое значение счетчика.
#Этот пример демонстрирует, как можно безопасно управлять общим состоянием (счетчиком) в асинхронной среде, используя `asyncio` и механизмы синхронизации.