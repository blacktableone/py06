from typing import Any
# "from X import Y" reuses code from another file, here your exercise 0.
# data_processor.py must be in the same folder.
from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class DataStream:
	# `__init__()` 是一个特殊method方法。当你创建新object对象时，Python 会自动执行它。
	# stream = DataStream()
	# 这会自动运行 `__init__()`
	# 为这个 `stream` 对象创建一个空 list：`self._processors`。
    def __init__(self) -> None:
        # The stream only knows the PARENT type DataProcessor.
        # Numeric/Text/Log objects can all live in this one list.
        # 这行代码创建一个空 list，用来保存 processor 对象。
        # `list[DataProcessor]` 是type annotation类型注解
        # 意思是这个 list 预期存放 `DataProcessor` 或它的subclasses。
        self._processors: list[DataProcessor] = []
	
	# 注册 processor，也就是把 processor 加入 `_processors`。
    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
	    # `stream` is the input list. `element` represents one item at a time.
        for element in stream:  # one element of the batch at a time
        
	        # 每次处理新的item时，先设为 `False`，表示目前还没有 processor 处理它。
            handled = False  # a flag: "did someone accept it yet?"
            
            # 这个 loop 会依次检查已注册的 processor，直到某个 processor 接受当前元素。
            # with 42
            # `NumericProcessor.validate(42)` returns `True`.
            # The item is sent to `NumericProcessor`.
            # The loop stops, so the other processors do not need to check `42`.
            for proc in self._processors:
                # POLYMORPHISM: we call validate/ingest without knowing
                # which child class proc is. Each child answers in its
                # own way.
                # 先检查数据是否适合这个 processor
                if proc.validate(element):
		            
		            # 如果适合，就真正处理并存储数据
                    proc.ingest(element)
                    
                    # 标记这条数据已经被处理。
                    handled = True
                    
                    # 停止检查其他 processor，转去处理下一条数据。
                    # `break` 仅会退出最内​​层的循环——在此例中，即内层的 `for proc` 循环
                    # 它不会停止外层的 `for element` 循环。
                    break  # stop searching: first match wins
            if not handled:  # the loop ended and nobody accepted it
                print("DataStream error - Can't process element "
                      f"in stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        
        # 在 Python 中，空 list `[]` 会被视为 falsy（假值）。
        # 等价于检查“processor 列表是不是空的”。
        if not self._processors:
            print("No processor found, no data")
            
            # 用 `return` 提前结束 `print_processors_stats()`，
            return  # leave the function early
        for proc in self._processors:
            # proc = NumericProcessor()
            # print(type(proc)) 
            # OUTPUT: <class '__main__.NumericProcessor'>
            # __name__ gets the name of that class as a string.
            # print(type(proc).__name__)
            # OUTPUT: NumericProcessor
            #  `.replace()` 是字符串的 method，不会改变 processor，只会生成一个新的字符串
            name = type(proc).__name__.replace("Processor", " Processor")
            print(f"{name}: total {proc.total_ingested()} items "
                  f"processed, remaining {proc.remaining()} on processor")


def consume(proc: DataProcessor, count: int) -> None:
    # takes "count" pieces out of a processor, ignoring the values
    for _ in range(count):
        proc.output()


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Registering other data processors")
    text = TextProcessor()
    logs = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(logs)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    consume(numeric, 3)
    consume(text, 2)
    consume(logs, 1)
    stream.print_processors_stats()