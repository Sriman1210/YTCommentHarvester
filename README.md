# Youtube Comment harvester

**YouTubeInsightsExtractor** is a Python-based tool designed to extract video data and top-level comments from all videos of specified YouTube channels. It leverages the YouTube Data API v3 to gather video IDs and retrieve comments, making it ideal for researchers, content analysts, and developers.

## Features
- Extracts all video IDs from a specified YouTube channel.
- Retrieves top-level comments from each video for analysis.
- Processes multiple channels by reading URLs or IDs from a CSV file.
- Outputs results in a structured format for further use.

## Requirements
- Python 3.x
- Required Python libraries:
  - `pandas` for CSV file handling
  - `google-api-python-client` for interacting with the YouTube Data API

## Installation and Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/YouTubeInsightsExtractor.git
   cd YouTubeInsightsExtractor
   ```

2. ```bash
   python youtube_comments.py
   ```

## Setup
- Google Cloud Project Configuration
- Create a project in Google Cloud Console.
- Enable the YouTube Data API v3.
- Generate an API key and restrict it to the YouTube Data API for security.