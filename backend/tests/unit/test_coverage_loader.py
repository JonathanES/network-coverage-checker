import pytest
import tempfile
import os
from pathlib import Path
from src.data.coverage_loader import CoverageDataLoader
from src.models.records import CoverageRecord


@pytest.fixture
def create_test_csv():
    """Fixture to create temporary CSV files for testing"""
    temp_files = []

    def _create_csv(content: str) -> str:
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
        temp_file.write(content)
        temp_file.close()
        temp_files.append(temp_file.name)
        return temp_file.name

    yield _create_csv

    # Cleanup all created files
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except FileNotFoundError:
            pass  # File already deleted


class TestCoverageDataLoader:
    """Unit tests for CoverageDataLoader"""

    def test_load_data_success(self, create_test_csv):
        """Test successful loading of CSV data"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0
SFR,103113,6848661,1,1,0
Bouygues,103114,6848664,1,1,1"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)
        records = loader.load_data()

        assert len(records) == 3

        # Test first record
        assert records[0].operator == "Orange"
        assert records[0].x == 102980
        assert records[0].y == 6847973
        assert records[0].network_2g == 1
        assert records[0].network_3g == 1
        assert records[0].network_4g == 0

        # Test second record
        assert records[1].operator == "SFR"
        assert records[1].x == 103113
        assert records[1].y == 6848661
        assert records[1].network_2g == 1
        assert records[1].network_3g == 1
        assert records[1].network_4g == 0

        # Test third record
        assert records[2].operator == "Bouygues"
        assert records[2].x == 103114
        assert records[2].y == 6848664
        assert records[2].network_2g == 1
        assert records[2].network_3g == 1
        assert records[2].network_4g == 1

    def test_load_data_with_different_coverage_values(self, create_test_csv):
        """Test loading CSV with different coverage combinations"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0
SFR,103113,6848661,0,1,1"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)
        records = loader.load_data()

        assert len(records) == 2
        assert records[0].operator == "Orange"
        assert records[0].network_2g == 1
        assert records[0].network_4g == 0
        assert records[1].operator == "SFR"
        assert records[1].network_2g == 0
        assert records[1].network_4g == 1

    def test_load_data_caching(self, create_test_csv):
        """Test that data is cached after first load"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)

        # First load
        records1 = loader.load_data()
        assert len(records1) == 1
        assert loader._loaded is True

        # Second load should return cached data
        records2 = loader.load_data()
        assert records1 is records2  # Same object reference

    def test_load_data_empty_csv(self, create_test_csv):
        """Test loading empty CSV (only headers)"""
        csv_content = """Operateur,x,y,2G,3G,4G"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)
        records = loader.load_data()

        assert len(records) == 0
        assert isinstance(records, list)

    def test_load_data_invalid_coordinates(self, create_test_csv):
        """Test handling of invalid coordinate data"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,invalid,6847973,1,1,0"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)

        # Should raise ValueError when trying to convert 'invalid' to int
        with pytest.raises(ValueError):
            loader.load_data()

    def test_load_data_invalid_coverage_values(self, create_test_csv):
        """Test handling of invalid coverage values"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,invalid,1,0"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)

        # Should raise ValueError when trying to convert 'invalid' to int
        with pytest.raises(ValueError):
            loader.load_data()

    def test_load_data_file_not_found(self):
        """Test handling of non-existent file"""
        loader = CoverageDataLoader("nonexistent_file.csv")

        with pytest.raises(FileNotFoundError):
            loader.load_data()

    def test_coverage_record_validation(self):
        """Test that CoverageRecord validates data correctly"""
        # Valid record
        record = CoverageRecord(
            operator="Orange",
            x=102980,
            y=6847973,
            network_2g=1,
            network_3g=1,
            network_4g=0,
        )

        assert record.operator == "Orange"
        assert record.x == 102980
        assert record.y == 6847973
        assert record.network_2g == 1
        assert record.network_3g == 1
        assert record.network_4g == 0

    def test_csv_path_handling(self):
        """Test that CSV path is handled correctly"""
        loader = CoverageDataLoader("/path/to/test.csv")

        assert isinstance(loader.csv_path, Path)
        assert str(loader.csv_path) == "/path/to/test.csv"
        assert loader._loaded is False
        assert loader._data == []

    def test_reload_functionality(self, create_test_csv):
        """Test reload() method properly clears cache and reloads data"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)

        # Initial load
        records1 = loader.load_data()
        assert len(records1) == 1
        assert loader._loaded is True
        assert len(loader._data) == 1

        # Reload should clear cache and reload
        records2 = loader.reload()
        assert len(records2) == 1
        assert loader._loaded is True

        # Should be same list object (memory efficient) but freshly loaded
        assert records1 is records2  # Same list object
        assert records2[0].operator == "Orange"  # Freshly loaded content

    def test_reload_with_file_changes(self, create_test_csv):
        """Test reload() picks up changes to the CSV file"""
        initial_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0"""

        csv_path = create_test_csv(initial_content)

        loader = CoverageDataLoader(csv_path)

        # Initial load
        records1 = loader.load_data()
        assert len(records1) == 1
        assert records1[0].operator == "Orange"

        # Modify the file
        updated_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0
SFR,103113,6848661,1,1,0"""

        with open(csv_path, "w") as f:
            f.write(updated_content)

        # Regular load_data() returns cached data (no change)
        records2 = loader.load_data()
        assert len(records2) == 1  # Still cached

        # reload() picks up the changes
        records3 = loader.reload()
        assert len(records3) == 2  # New data
        assert records3[0].operator == "Orange"
        assert records3[1].operator == "SFR"

    def test_reload_clears_data_on_empty_reload(self, create_test_csv):
        """Test reload() properly handles transition to empty file"""
        initial_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0"""

        csv_path = create_test_csv(initial_content)

        loader = CoverageDataLoader(csv_path)

        # Initial load with data
        records1 = loader.load_data()
        assert len(records1) == 1

        # Replace with empty file (only headers)
        empty_content = """Operateur,x,y,2G,3G,4G"""
        with open(csv_path, "w") as f:
            f.write(empty_content)

        # reload() should pick up empty file
        records2 = loader.reload()
        assert len(records2) == 0
        assert loader._loaded is True

    def test_reload_state_management(self, create_test_csv):
        """Test reload() properly manages internal state"""
        csv_content = """Operateur,x,y,2G,3G,4G
Orange,102980,6847973,1,1,0"""

        csv_path = create_test_csv(csv_content)

        loader = CoverageDataLoader(csv_path)

        # Initial state
        assert loader._loaded is False
        assert len(loader._data) == 0

        # After load
        loader.load_data()
        assert loader._loaded is True
        assert len(loader._data) == 1

        # After reload - state should be properly managed
        loader.reload()
        assert loader._loaded is True  # Should be loaded after reload
        assert len(loader._data) == 1  # Should contain reloaded data
