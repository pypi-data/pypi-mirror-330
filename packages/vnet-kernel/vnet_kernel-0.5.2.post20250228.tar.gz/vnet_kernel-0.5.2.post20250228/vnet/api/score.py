import json
from ctypes import CDLL
from dataclasses import asdict, dataclass, field


@dataclass
class CheckPoint:
    description: str = ""
    is_passed: bool = False
    score_weight: int = 10
    expected_output: str = ""


@dataclass
class ScoreVO:
    score: int = 0  # 总分
    all_checkpoints: list[str] = field(default_factory=list)
    failed_checkpoints: list = field(default_factory=list)

    _checkpoints: list = field(default_factory=list)

    def __init__(self, desc, expected_outputs, scores):
        self._checkpoints = [
            CheckPoint(checkpoint_name, False, score, expected_output)
            for checkpoint_name, score, expected_output in zip(desc, scores, expected_outputs)
        ]
        self.all_checkpoints = desc  # 存放checkpoint描述
        self.failed_checkpoints = []  # Initialize failed_checkpoints

    def to_json(self):
        data = asdict(self)
        data.pop("_checkpoints", None)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def calculate_score(self, export_to_json_file=True):
        self.score = sum(cp.score_weight for cp in self._checkpoints if cp.is_passed)
        if export_to_json_file:
            json_data = self.to_json()
            # Write to file
            with open("result.json", "w") as f:
                f.write(json_data)

    def add_failed_checkpoint(self, checkpoint, actual_output):
        self.failed_checkpoints.append(
            {
                "test_point": checkpoint.description,
                "expected": checkpoint.expected_output,
                "actually": actual_output,
            }
        )


class LibUtils:
    @staticmethod
    def load_library(lib_path, functions: list[tuple]):
        lib = CDLL(lib_path)

        func_not_found = []

        for func_name, argtypes, restype in functions:
            if hasattr(lib, func_name):
                func = getattr(lib, func_name)
                func.argtypes = argtypes
                func.restype = restype
            else:
                func_not_found.append(func_name)
        return lib, func_not_found

    @staticmethod
    def func_not_found_handler(func_name: list[str], score_vo: ScoreVO):
        for checkpoint in score_vo._checkpoints:
            score_vo.add_failed_checkpoint(
                checkpoint, f"请勿修改函数签名{func_name}，否则无法通过测试"
            )
        score_vo.calculate_score()
        return
