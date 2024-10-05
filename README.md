# Video Analysis Project

## Overview

This project converts a landscape video (e.g., 16:9) to a portrait format (9:16) suitable for mobile devices. It dynamically crops the video based on face detection to ensure the main subject remains centered.

## Features

- Extracts frames from the input video.
- Detects faces in each frame using DLIB.
- Determines optimal crop positions to center the largest detected face.
- Smooths crop positions to prevent jitter.
- Generates video segments based on crop positions.
- Processes video segments with FFmpeg.
- Concatenates segments and reapplies the original audio.
- Implements robust logging for easy debugging and monitoring.
- Cleans up temporary files after processing.

## Requirements

- Python 3.6+
- FFmpeg
- Homebrew (for macOS users)
- Python Libraries:
  - opencv-python
  - dlib
  - numpy

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/video_analysis_project.git
    cd video_analysis_project
    ```

2. **Install Homebrew (macOS only)**:

    If not already installed, install Homebrew using:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

3. **Install FFmpeg Using Homebrew (macOS)**:

    ```bash
    brew install ffmpeg
    ```

4. **Install Dependencies**:

    It's recommended to use a virtual environment.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

5. **Install `dlib`**:

    ```bash
    brew install cmake boost
    pip install dlib
    ```

    **Note:** Ensure that `cmake` and `boost` are installed via Homebrew before installing `dlib` via `pip`.

6. **Verify FFmpeg Installation**:

    ```bash
    ffmpeg -version
    ```

    You should see the installed FFmpeg version.

## Usage

1. **Configure Parameters**:

    Edit `config.py` to set your input video path and output directories.

2. **Run the main script**:

    ```bash
    python3 main.py
    ```

3. **Output**:

    - The final cropped video will be saved as specified in `config.py` (default: `final_cropped_video.mp4`).
    - A log file named `video_analysis.log` will be created in the project directory, detailing the processing steps and any issues encountered.

## Logging

The project uses Python's built-in `logging` module to provide detailed logs of the processing stages. Logs are output to both the console and a log file named `video_analysis.log`.

- **Log Levels**:
  - `INFO`: General information about the processing stages.
  - `DEBUG`: Detailed diagnostic information (enabled by setting the log level to `DEBUG` in `utils.py`).
  - `WARNING`: Potential issues that aren't critical.
  - `ERROR`: Errors that occur during processing.
  - `CRITICAL`: Severe errors that may halt the program.

**To Enable Debug Logging**:

Modify the `setup_logging` function in `utils.py` to set the log level to `DEBUG`:

```python
def setup_logging(log_file='video_analysis.log'):
    """
    Configures the logging settings.

    Args:
        log_file (str): Path to the log file.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Changed from INFO to DEBUG
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging is configured.")
