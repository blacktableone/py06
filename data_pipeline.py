from typing import Any, Protocol
# "from X import Y" reuses code from another file, here your exercise 0.
# data_processor.py must be in the same folder.
from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)

class ExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...

class CSVPlugin:
    def _escape(self, value: str) -> str:
        if "," in value or "\n" in value or '"' in value:
            value = value.replace('"', '""')
            return '"' + value + '"'
        return value

    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields = [self._escape(value) for _, value in data]
        print("CSV Output:")
        print(",".join(fields))


class JSONPlugin:
    def _escape(self, value: str) -> str:
        value = value.replace("\\", "\\\\")
        value = value.replace('"', '"\\')
        return value.replace("\n", "\n\\")

    def process_output(self, data: list[tuple[int, str]]) -> None:
        parts: list[str] = [] # why parts is list[str]?
        for rank, value in data:
            text = self._escape(value)
            parts.append(f'"item_{rank}": "{text}"')
        print("JSON Output:")
        print("{" + ", ".join(parts) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
	
	# 注册 processor，也就是把 processor 加入 `_processors`。
    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
	    # `stream` is the input list. `element` represents one item at a time.
        for element in stream:  # one element of the batch at a time
        
	        # 每次处理新的item时，先设为 `False`，表示目前还没有 processor 处理它。
            handled = False  # a flag: "did someone accept it yet?"

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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            for _ in range(min(nb, proc.remaining())):
                # proc.output取得这个 method 本身
                # proc.output() 调用 method，取得返回值
                batch.append(proc.output())
            if batch:
                plugin.process_output(batch)

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        
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
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch1: list[Any] = [
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
    print(f"\nSend first batch of data on stream: {batch1}")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVPlugin())
    stream.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch2}")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONPlugin())
    stream.print_processors_stats()