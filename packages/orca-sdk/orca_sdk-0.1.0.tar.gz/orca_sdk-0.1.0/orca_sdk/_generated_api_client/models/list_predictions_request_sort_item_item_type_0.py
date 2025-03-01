from enum import Enum


class ListPredictionsRequestSortItemItemType0(str, Enum):
    CONFIDENCE = "confidence"
    TIMESTAMP = "timestamp"

    def __str__(self) -> str:
        return str(self.value)
