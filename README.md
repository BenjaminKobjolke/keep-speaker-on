# Keep Speaker On

A Python application that plays audio files from the input directory at specified intervals to keep speakers or audio devices active.

## Features

- Plays audio files from the input directory at a configurable interval
- Supports WAV, MP3, and OGG audio formats
- Configurable via settings.ini
- Detailed logging

## Requirements

- Python 3.6 or higher
- Dependencies listed in requirements.txt

## Installation

1. Clone this repository or download the source code
2. Run the installation script:

```
install.bat
```

This will create a virtual environment and install all required dependencies.

## Configuration

The application can be configured by creating a `settings.ini` file based on the provided `settings_example.ini` template:

```ini
[Settings]
# Interval in minutes between audio playback
interval_minutes = 5

[Logging]
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_level = INFO
# Log file path (relative to application root)
log_file = app.log
```

Note: `settings.ini` is ignored by git to prevent committing personal configurations.

## Usage

1. Place your audio files in the `input` directory
2. Run the application:

```
run.bat
```

The application will play all audio files in the input directory at the specified interval.

## How It Works

1. The application scans the input directory for supported audio files
2. It plays all audio files at startup
3. It then schedules playback at the specified interval (default: 5 minutes)
4. The application continues running until manually stopped (Ctrl+C)

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- OGG (.ogg)

## Troubleshooting

If you encounter any issues:

1. Check the log file (app.log by default) for error messages
2. Ensure your audio files are in a supported format
3. Verify that your audio device is properly connected and working

## License

This project is open source and available under the MIT License.
