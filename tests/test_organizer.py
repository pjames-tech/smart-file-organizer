"""
Unit tests for the file organizer module.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from organizer import get_category, organize_files


class TestGetCategory:
    """Tests for the backward-compatible get_category function."""
    
    def test_image_category(self):
        """Image extensions should return 'Images'."""
        assert get_category(".jpg") == "Images"
        assert get_category(".png") == "Images"
        assert get_category(".gif") == "Images"
    
    def test_document_category(self):
        """Document extensions should return 'Documents'."""
        assert get_category(".pdf") == "Documents"
        assert get_category(".docx") == "Documents"
    
    def test_case_insensitive(self):
        """Extension matching should be case-insensitive."""
        assert get_category(".JPG") == "Images"
        assert get_category(".PDF") == "Documents"
    
    def test_unknown_category(self):
        """Unknown extensions should return 'Other'."""
        assert get_category(".xyz") == "Other"
        assert get_category(".unknown") == "Other"


class TestOrganizeFilesDryRun:
    """Tests for dry-run mode."""
    
    @pytest.fixture
    def temp_source_dir(self):
        """Create a temporary directory with test files."""
        temp_dir = tempfile.mkdtemp()
        # Create test files
        (Path(temp_dir) / "test.jpg").touch()
        (Path(temp_dir) / "document.pdf").touch()
        (Path(temp_dir) / "script.py").touch()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def temp_dest_dir(self):
        """Create a temporary destination directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_dry_run_no_files_moved(self, temp_source_dir, temp_dest_dir):
        """Dry run should not move any files."""
        # Setup logging to avoid errors
        from logging_config import setup_logging
        setup_logging(level="WARNING", log_file=None)
        
        # Count files before
        files_before = list(Path(temp_source_dir).iterdir())
        
        # Run in dry-run mode
        stats = organize_files(
            source_dir=temp_source_dir,
            dest_dir=temp_dest_dir,
            dry_run=True
        )
        
        # Count files after
        files_after = list(Path(temp_source_dir).iterdir())
        
        # Files should still be in source
        assert len(files_before) == len(files_after)
        assert stats["moved"] == 3  # Counted but not moved
    
    def test_dry_run_destination_empty(self, temp_source_dir, temp_dest_dir):
        """Dry run should not create destination folders."""
        from logging_config import setup_logging
        setup_logging(level="WARNING", log_file=None)
        
        organize_files(
            source_dir=temp_source_dir,
            dest_dir=temp_dest_dir,
            dry_run=True
        )
        
        # Destination should still be empty (no category folders created)
        dest_contents = list(Path(temp_dest_dir).iterdir())
        assert len(dest_contents) == 0


class TestOrganizeFilesErrors:
    """Tests for error handling."""
    
    def test_nonexistent_source_directory(self):
        """Should raise FileNotFoundError for non-existent source."""
        from logging_config import setup_logging
        setup_logging(level="WARNING", log_file=None)
        
        with pytest.raises(FileNotFoundError):
            organize_files(source_dir="/nonexistent/path/12345")
    
    def test_source_is_file(self, tmp_path):
        """Should raise NotADirectoryError if source is a file."""
        from logging_config import setup_logging
        setup_logging(level="WARNING", log_file=None)
        
        # Create a file instead of directory
        test_file = tmp_path / "not_a_dir.txt"
        test_file.touch()
        
        with pytest.raises(NotADirectoryError):
            organize_files(source_dir=str(test_file))


class TestOrganizeFilesActual:
    """Tests for actual file organization."""
    
    @pytest.fixture
    def temp_source_dir(self):
        """Create a temporary directory with test files."""
        temp_dir = tempfile.mkdtemp()
        (Path(temp_dir) / "photo.jpg").touch()
        (Path(temp_dir) / "report.pdf").touch()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def temp_dest_dir(self):
        """Create a temporary destination directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_files_organized_correctly(self, temp_source_dir, temp_dest_dir):
        """Files should be moved to correct category folders."""
        from logging_config import setup_logging
        setup_logging(level="WARNING", log_file=None)
        
        stats = organize_files(
            source_dir=temp_source_dir,
            dest_dir=temp_dest_dir,
            dry_run=False
        )
        
        # Check files were moved
        assert stats["moved"] == 2
        assert stats["errors"] == 0
        
        # Check destination structure
        assert (Path(temp_dest_dir) / "Images" / "photo.jpg").exists()
        assert (Path(temp_dest_dir) / "Documents" / "report.pdf").exists()
        
        # Check source is empty
        remaining = list(Path(temp_source_dir).iterdir())
        assert len(remaining) == 0
