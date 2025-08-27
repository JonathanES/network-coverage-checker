import csv
from pathlib import Path
from typing import List
from src.models.records import CoverageRecord


class CoverageDataLoader:
    """Loads and manages coverage data from CSV file"""

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self._data: List[CoverageRecord] = []
        self._loaded = False

    def load_data(self) -> List[CoverageRecord]:
        """Load coverage data from CSV file"""
        if self._loaded:
            return self._data

        with open(self.csv_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                record = CoverageRecord(
                    operator=row["Operateur"],
                    x=int(row["x"]),
                    y=int(row["y"]),
                    network_2g=int(row["2G"]),
                    network_3g=int(row["3G"]),
                    network_4g=int(row["4G"]),
                )
                self._data.append(record)

        self._loaded = True
        return self._data

    def reload(self) -> List[CoverageRecord]:
        """Force reload data from CSV file, discarding any cached data"""
        self._loaded = False
        self._data.clear()
        return self.load_data()
