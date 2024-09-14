## Overview

This project is a web application that summarizes YouTube videos and extracts key insights. It uses AI to analyze video transcripts, providing users with concise summaries, main points and actionable takeaways. The app streamlines the process of extracting valuable information from lengthy video content, saving users time and enhancing their learning experience.

## Technologies Used

- Frontend: HTML and CSS served via nginx 
- Backend: Python (Flask)
- Containerization: Docker
- Orchestration: Docker Compose

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/lperez37/aintngtft.git
   cd aintngtft
   ```

2. Set up environment variables:
   Copy the `.env.example` file to `.env` and fill in the necessary variables (OpenAI and Cloudflare)

3. Build and run the Docker containers:
   ```
   docker compose up --build
   ```

## Usage

1. Open your browser and navigate to `http://localhost:8076`. This repo uses Cloudflared to expose the local server to the internet, but feel free to use any other method to access the local server (such as nginx proxy manager)

2. Enter the YouTube URL you want to analyze and click the "Summarize" or "Extract Wisdom" button.

