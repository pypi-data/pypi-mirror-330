yt-transcript: Developer Specification

Overview

yt-transcript is a Python CLI tool that fetches YouTube video transcripts and optionally summarizes them using OpenAI's GPT. It also supports chapter-based summarization, Whisper-based transcription for videos without captions, and caching for efficiency.

Key Features

Fetch YouTube transcripts via video URL

Automatically detect and retrieve transcripts in the correct language

Optionally use auto-generated captions if no official transcript is available

Save transcripts in JSON format

Summarize transcripts by chapter using OpenAI GPT

Store summaries separately in JSON and Markdown formats

Add YouTube timestamp links in Markdown summaries

Support local Whisper.cpp transcription for videos without transcripts

Provide a CLI interface with click

Cache transcripts to avoid redundant API calls

Include logging and error handling

Support basic unit tests for core functionality

Architecture & Implementation

1. CLI Interface

Command Structure

yt-transcript <youtube_url> [OPTIONS]

Options:

Option

Description

--summarize

Generate LLM-based chapter summaries

--markdown

Output a markdown summary (<video_id>_summary.md)

--output-dir <path>

Specify an output directory (default: current directory)

--language <lang>

Fetch transcript in a specific language (default: auto-detect)

--verbose

Print detailed logs for debugging

--whisper

Use Whisper.cpp if no transcript is available

--whisper-model <model>

Specify Whisper model (default: medium)

--no-cache

Force fresh transcript retrieval, ignoring cache

--clear-cache [video_id]

Delete cached transcripts (all or specific video)

--log-file <path>

Specify a log file (default: yt-transcript.log)

--version

Display tool version

2. Transcript Fetching

Process:

Extract video ID from the provided YouTube URL.

Attempt to fetch the official transcript.

If unavailable, retry with auto-generated captions.

If neither is available, prompt the user to use Whisper transcription.

Save transcript in JSON format.

JSON Output Structure:

{
  "video_id": "abc123",
  "title": "Example Video Title",
  "channel_name": "Example Channel",
  "channel_id": "channel123",
  "published_date": "2024-02-21",
  "retrieved_at": "2025-02-21T14:00:00Z",
  "language": "en",
  "transcript": [
    {
      "start": 0.0,
      "duration": 5.0,
      "text": "This is the first line of the transcript."
    }
  ],
  "video_description": "This is a sample description of the video.",
  "video_url": "https://www.youtube.com/watch?v=abc123"
}

3. Summarization Process

Extract YouTube chapter markers, if available.

If no chapters exist, use an AI-based topic segmentation.

Call OpenAI GPT API to generate chapter-based summaries.

Store summaries separately in JSON and Markdown formats.

Markdown Output Example:

# [Example Video Title](https://www.youtube.com/watch?v=abc123)

*Channel:* Example Channel  
*Published:* 2024-02-21  
*Language:* English  

---

## Summary by Chapters

### [Chapter 1: Chapter Title](https://www.youtube.com/watch?v=abc123&t=312s)
(00:05:12 - 00:12:45)  
Summary of this chapter...

*Generated on 2025-02-21*

4. Whisper-based Transcription

Use yt-dlp to extract audio-only.

Run Whisper.cpp locally for speech-to-text.

Detect Apple Silicon (M1/M2/M3) and apply Mac optimizations automatically.

Save Whisper-generated transcript separately in <video_id>_whisper.json.

5. Caching

Store cached transcripts in ~/.yt-transcript-cache/.

Never expire cached transcripts unless manually deleted.

Show warning when using cached data.

Allow users to disable caching with --no-cache.

Provide a yt-transcript clear-cache command for manual cache clearing.

6. Logging & Error Handling

Default logs to yt-transcript.log.

Provide a --log-file <path> option.

Error handling approach:

Exit on failure (e.g., API errors, transcript not found).

Retry twice on rate limits before failing.

Log full details (stack trace, timestamps) for debugging.

Use tqdm progress bars for visual feedback.

7. Storage & File Handling

Transcript & Summary Storage:

JSON: <video_id>.json, <video_id>_summary.json

Markdown: <video_id>_summary.md

Whisper transcript: <video_id>_whisper.json

Default to current working directory unless --output-dir is specified.

Overwrite files without confirmation.

8. CLI Utility Commands

Command

Description

yt-transcript list

Display saved transcripts in a table format

yt-transcript delete <video_id>

Confirm and delete a specific transcript

yt-transcript clear-cache

Delete all cached transcripts

yt-transcript --help

Show CLI usage details

Testing Plan

Unit Tests

Validate YouTube URL parsing.

Ensure proper transcript fetching.

Verify JSON output structure.

Test LLM summarization logic.

Check Whisper transcription handling.

Confirm CLI commands execute correctly.

Test Framework

Use pytest for unit testing.

Mock API calls (YouTube & OpenAI) to prevent unnecessary requests.

Validate caching behavior.

Ensure logs and errors behave as expected.

Packaging & Distribution

Package as a pip-installable CLI tool.

Publish on PyPI for easy installation (pip install yt-transcript).

Use semantic versioning (MAJOR.MINOR.PATCH).

Support auto-completions for Bash, Zsh, and Fish shells.

Conclusion

This specification provides a clear blueprint for the implementation of yt-transcript. With a structured CLI, caching, logging, Whisper integration, and OpenAI-based summarization, the tool will be a powerful utility for YouTube content processing. The next step is development based on this spec.

