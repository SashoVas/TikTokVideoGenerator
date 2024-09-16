# TikTok Video Generator

This Python project automates the process of generating TikTok videos using stories scraped from Reddit. The generated video includes:
- Subtitles of the story.
- Background video to maintain engagement.
- GIFs placed strategically to retain viewer attention.
- AI-generated audio using Eleven Labs' Text-to-Speech API.

The TikTok account i use to dump all the test generated videos: https://www.tiktok.com/@bulgarian_story

## Table of Contents
- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)

## Usage
1. **Scrape stories from Reddit:** The project uses a custom Python script to scrape stories from a Reddit subreddit of your choice. You can specify the subreddit and number of stories to scrape.

2. **Generate AI Voiceover:** The project uses the Eleven Labs API to generate realistic voiceovers from the scraped stories. Make sure your API key is in the .env file.

3. **Generate Video:** The project will use background videos, GIFs, and the voiceover to create a final TikTok video with:
    - Subtitles in sync with the audio.
    - Pop-up GIFs to keep viewers engaged.
## Prerequisites

Before running the project, ensure you have the following:

1. A `.env` file in the root directory containing your Eleven Labs API key:
   ```plaintext
   ELEVEN_LABS_API_KEY=your-eleven-labs-api-key
2. Two folders in the root directory:
  - background_videos: This folder should contain background videos that will be used in the final TikTok video.
  - popups: This folder should contain GIFs that will be used as attention-grabbing popups throughout the video.

## Installation
1. Clone the repository:
  ```
    git clone https://github.com/your-username/tiktok-video-generator.git
    cd tiktok-video-generator
  ```
2. Install dependencies:
  ```
    pip install -r requirements.txt
  ```
3. Create a `.env` file in the root directory and add your Eleven Labs API key:
  ```
  touch .env
  echo "ELEVEN_LABS_API_KEY=your-eleven-labs-api-key" > .env
  ```
4. Ensure that the `background_videos` and `popups` folders contain the required assets for video generation.

   
## Project Structure
```
tiktok-video-generator/
│
├── background_videos/      # Folder containing background videos
├── popups/                 # Folder containing attention-grabbing GIFs
├── main.py                 # Main script for running the project
├── requirements.txt        # Python dependencies
├── .env                    # API keys and environment variables
├── README.md               # Project documentation
├── scraper.py               # Module for scraping stories
├── video_generator.py       # Module for generating the videos
├── auto_video_generator.py  # Module for automaticly generating the final video
├── text_to_speech.py        # Module for generating AI voiceover
└── subtitle_generator.py    # Module for generating subtitles
```