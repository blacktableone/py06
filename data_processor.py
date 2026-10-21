from abc import ABC, abstractmethod
from typing import Any
# ABC = Abstract Base Class: a class that cannot be used directly,
#   it only defines a "contract" that child classes must follow.
# abstractmethod = marks a method that children MUST write themselves.
# Any = "any type is accepted" (needed by validate, per the subject).


class DataProcessor(ABC):  # inherit from ABC -> this class is abstract
    def __init__(self) -> None:
        # list[str] is a type annotation: a list that holds strings.
        # The leading "_" is a convention: "internal, don't touch".
        self._storage: list[str] = []  # queue of pieces waiting
        self._rank: int = 0  # how many pieces were already output

    @abstractmethod  # children are forced to override this method
    def validate(self, data: Any) -> bool:
        """Return True if this processor can ingest data."""

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Store data, or raise an exception if it is invalid."""

    def output(self) -> tuple[int, str]:
        # Normal (non-abstract) method: children inherit it as-is.
        if not self._storage:
            raise IndexError("No data to output")
        value = self._storage.pop(0)  # pop(0) removes the OLDEST item
        rank = self._rank
        self._rank += 1  # next output gets the next rank
        return rank, value  # a tuple[int, str]

    def remaining(self) -> int:
        return len(self._storage)

    def total_ingested(self) -> int:
        return self._rank + len(self._storage)


class NumericProcessor(DataProcessor):
    def _is_number(self, item: Any) -> bool:
        # bool is a subclass of int in Python (True == 1), so we
        # exclude it explicitly, otherwise True would count as number.
        return isinstance(item, (int, float)) and not isinstance(
            item, bool
        )

    def validate(self, data: Any) -> bool:
	    # 当一个函数接受不同类型的输入，而每种类型需要不同的处理方式时，可以用 isinstance()分支
        if isinstance(data, list):  # 就是在问：“`data` 是不是一个 list？”
            # all(...) is True only if EVERY element passes the test
            return all(self._is_number(item) for item in data)
            # for item in data 逐个拿出 list 中的元素
            # isinstance(item, str 检查当前元素是不是字符串
            # all(...) 只有所有检查都为 True 最终结果才是 True
        return self._is_number(data)

    # "int | float" means "int OR float" (needs Python 3.10+)
    # list[int | float] 这是 type annotation（类型注解)
    # 它告诉读代码的人和 mypy 这份数据预期是什么类型。它本身不会在运行时自动验证每个元素。
    def ingest(self, data: int | float | list[int | float]) -> None:
        # Validate BEFORE touching storage: a bad input must never
        # leave the storage half-filled (protects against corruption).
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:  #如果是 list，就逐个处理里面的数字。
                self._storage.append(str(item))  # numbers -> strings
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            self._storage.extend(data)  # extend = append many at once
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    def _is_log(self, item: Any) -> bool:
        # A valid log is a dict where every key and value is a str
        return isinstance(item, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in item.items()
        ) 
        # isinstance(item, dict) 检查 `item` 是不是 dictionary
        # item.items() 取得 dictionary 中的 key-value pairs
        # isinstance(k, str) and isinstance(v, str) 检查 key 和 value 是否都是字符串。
        # all(... for k, v in item.items()) 检查每一对 key-value 是否都符合要求。
        # and 表示：`item` 必须先是 dictionary，而且所有 key 和 value 都必须是字符串。
        # _log 名字前面的 `_` 是一种约定，表示它主要供这个 class 内部使用。

    def validate(self, data: Any) -> bool:
	    # Case B: a list of dictionaries 逐个检查 list 中的 dictionary
	    # 只有每个 dictionary 都有效，结果才是 `True`。
        if isinstance(data, list):
            return all(self._is_log(item) for item in data)
        
        # Case A: one dictionary 直接检查整个data。
        return self._is_log(data)

    def _format(self, log: dict[str, str]) -> str:
        # .get(key, default) avoids a crash if the key is missing
        # .get 是 dictionary 的 method
        # 意思是: 如果存在 `"log_level"`，返回对应的值；如果不存在，返回默认值 `"LOG"`
        level = log.get("log_level", "LOG")
        message = log.get("log_message", "")
        return f"{level}: {message}"  # f-string: {} inserts variables

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
	    
        # Case B: 输入是两个 log 的 list，就逐个调用 `_format(log)`
        if isinstance(data, list):
	        # 在 `for log in data` 中，每次循环拿到的单个 dictionary 
            for log in data:
                self._storage.append(self._format(log))
        # Case A: 输入是一个 log dictionary，就直接调用 `_format(data)`。
        else:
            self._storage.append(self._format(data))


# This block runs only when you do "python3 data_processor.py",
# not when another file imports this one.
if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior "
          "validation:")
    try:
        numeric.ingest("foo")  # type: ignore is NOT used: the subject
        # wants the mypy warning here, on purpose
    except ValueError as error:  # catch the exception, keep program alive
        print(f"Got exception: {error}")
    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    numeric.ingest(numbers)
    print("Extracting 3 values...")
    # `range(3)` 表示循环三次，循环计数值依次是 `0`、`1`、`2`。
    # `_` 不是特殊语法，它只是一个变量名。通常用 `_` 表示：需要循环，但不需要使用计数值。
    # 这里只需要连续取出三个结果，所以不需要使用计数器本身。
    for _ in range(3):  # "_" = a loop variable we don't need
	    # tuple unpacking（元组解包）
	    # 因为你的 `output()` 返回两个值：return rank, value
	    # 所以可以用两个变量分别接收
	    # 如果只写一个变量 result = numeric.output()
	    # 那么 `result` 会接收到整个 tuple，即 `(0, "42")`。
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f"Processing data: {words}")
    text.ingest(words)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("Testing Log Processor...")
    logs = LogProcessor()
    print(f"Trying to validate input 'Hello': {logs.validate('Hello')}")
    entries = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {entries}")
    logs.ingest(entries)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f"Log entry {rank}: {value}")