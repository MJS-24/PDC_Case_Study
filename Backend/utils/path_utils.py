"""Path resolution utilities for cross-platform CSV access"""

from pathlib import Path


class DataPathResolver:
    """Resolve CSV paths from root /data folder"""
    
    @staticmethod
    def get_project_root():
        """Get project root (parent of Backend/)"""
        backend_dir = Path(__file__).parent.parent
        return backend_dir.parent
    
    @staticmethod
    def get_data_folder(subfolder: str = "") -> Path:
        """Get /data folder (at project root)"""
        root = DataPathResolver.get_project_root()
        data_path = root / "data"
        
        if subfolder:
            data_path = data_path / subfolder
        
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path
    
    @staticmethod
    def get_csv_path(filename: str) -> Path:
        """Get full path to CSV file"""
        return DataPathResolver.get_data_folder() / filename
    
    @staticmethod
    def ensure_csv_exists(filename: str) -> bool:
        """Verify CSV exists"""
        path = DataPathResolver.get_csv_path(filename)
        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {path}")
        return True
