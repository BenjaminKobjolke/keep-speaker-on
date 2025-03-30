"""
Utility functions for file operations.
"""
import os
import logging
from typing import List, Tuple


class AudioFileManager:
    """
    Class to manage audio files in a directory.
    """
    # Supported audio file extensions
    SUPPORTED_EXTENSIONS = ('.wav', '.mp3', '.ogg')
    
    def __init__(self, input_dir: str = "input"):
        """
        Initialize AudioFileManager with the given input directory.
        
        Args:
            input_dir: Path to the directory containing audio files
        """
        self.input_dir = input_dir
        
    def get_audio_files(self) -> List[str]:
        """
        Get a list of audio files in the input directory.
        
        Returns:
            List of audio file paths
        """
        if not os.path.exists(self.input_dir):
            logging.error(f"Input directory '{self.input_dir}' does not exist")
            return []
        
        audio_files = []
        
        try:
            for file in os.listdir(self.input_dir):
                file_path = os.path.join(self.input_dir, file)
                
                # Check if it's a file and has a supported extension
                if os.path.isfile(file_path) and self._is_supported_audio_file(file):
                    audio_files.append(file_path)
        except Exception as e:
            logging.error(f"Error listing files in '{self.input_dir}': {e}")
            return []
        
        if not audio_files:
            logging.warning(f"No audio files found in '{self.input_dir}'")
        
        return audio_files
    
    def _is_supported_audio_file(self, filename: str) -> bool:
        """
        Check if the file has a supported audio extension.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if the file has a supported extension, False otherwise
        """
        return filename.lower().endswith(self.SUPPORTED_EXTENSIONS)
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate that an audio file exists and is readable.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, f"File '{file_path}' does not exist"
        
        if not os.path.isfile(file_path):
            return False, f"'{file_path}' is not a file"
        
        if not self._is_supported_audio_file(file_path):
            return False, f"File '{file_path}' is not a supported audio file"
        
        # Check if the file is readable
        try:
            with open(file_path, 'rb') as f:
                # Just read a small part to check if it's readable
                f.read(1024)
            return True, ""
        except Exception as e:
            return False, f"Error reading file '{file_path}': {e}"
