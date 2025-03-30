#!/usr/bin/env python3
"""
Keep Speaker On - A Python application to play audio files at specified intervals.

This application plays audio files from the input directory at a specified interval
to keep speakers or audio devices active.
"""
import os
import sys
import time
import logging
import signal
import schedule
from typing import List, NoReturn

from src.config.settings import Settings
from src.utils.file_utils import AudioFileManager
from src.audio.player import AudioPlayer


class KeepSpeakerOn:
    """
    Main application class for Keep Speaker On.
    """
    def __init__(self):
        """
        Initialize the application.
        """
        # Setup configuration
        self.settings = Settings()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self.file_manager = AudioFileManager()
        self.player = AudioPlayer()
        
        # Flag to control the main loop
        self.running = True
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self) -> None:
        """
        Set up logging configuration.
        """
        log_level_str = self.settings.get_log_level()
        log_file = self.settings.get_log_file()
        
        # Convert string log level to logging constant
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logging.info("Logging initialized")
    
    def _signal_handler(self, sig, frame) -> None:
        """
        Handle termination signals.
        
        Args:
            sig: Signal number
            frame: Current stack frame
        """
        logging.info(f"Received signal {sig}, shutting down...")
        self.running = False
        self.player.stop()
    
    def play_audio(self) -> None:
        """
        Play all audio files in the input directory.
        """
        audio_files = self.file_manager.get_audio_files()
        
        if not audio_files:
            logging.warning("No audio files found to play")
            return
        
        logging.info(f"Playing {len(audio_files)} audio file(s)")
        self.player.play_files(audio_files)
    
    def run(self) -> NoReturn:
        """
        Run the application.
        """
        interval_minutes = self.settings.get_interval_minutes()
        
        logging.info(f"Starting Keep Speaker On with {interval_minutes} minute interval")
        
        # Schedule the audio playback
        schedule.every(interval_minutes).minutes.do(self.play_audio)
        
        # Play once at startup
        self.play_audio()
        
        # Main loop
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, shutting down...")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """
        Clean up resources before exiting.
        """
        logging.info("Cleaning up resources...")
        self.player.cleanup()
        logging.info("Shutdown complete")


def main():
    """
    Main entry point for the application.
    """
    app = KeepSpeakerOn()
    app.run()


if __name__ == "__main__":
    main()
