"""
Audio player module for playing sound files.
"""
import os
import time
import logging
import pygame
from typing import List, Optional


class AudioPlayer:
    """
    Class to play audio files using pygame.
    """
    def __init__(self):
        """
        Initialize the audio player.
        """
        self._initialize_pygame()
    
    def _initialize_pygame(self) -> None:
        """
        Initialize pygame mixer for audio playback.
        """
        try:
            pygame.mixer.init()
            logging.info("Pygame mixer initialized successfully")
        except pygame.error as e:
            logging.error(f"Failed to initialize pygame mixer: {e}")
            raise RuntimeError(f"Failed to initialize audio system: {e}")
    
    def play_file(self, file_path: str) -> bool:
        """
        Play an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if playback started successfully, False otherwise
        """
        if not os.path.exists(file_path):
            logging.error(f"Audio file not found: {file_path}")
            return False
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            logging.info(f"Playing audio file: {file_path}")
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            logging.info(f"Finished playing: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Error playing audio file {file_path}: {e}")
            return False
    
    def play_files(self, file_paths: List[str]) -> int:
        """
        Play multiple audio files in sequence.
        
        Args:
            file_paths: List of paths to audio files
            
        Returns:
            Number of files played successfully
        """
        if not file_paths:
            logging.warning("No audio files to play")
            return 0
        
        success_count = 0
        
        for file_path in file_paths:
            if self.play_file(file_path):
                success_count += 1
        
        return success_count
    
    def stop(self) -> None:
        """
        Stop any currently playing audio.
        """
        try:
            pygame.mixer.music.stop()
            logging.info("Stopped audio playback")
        except Exception as e:
            logging.error(f"Error stopping playback: {e}")
    
    def cleanup(self) -> None:
        """
        Clean up pygame resources.
        """
        try:
            pygame.mixer.quit()
            logging.info("Pygame mixer resources released")
        except Exception as e:
            logging.error(f"Error cleaning up pygame mixer: {e}")
