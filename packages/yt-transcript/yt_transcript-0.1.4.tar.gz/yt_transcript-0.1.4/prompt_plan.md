1. High-Level Blueprint
Project Setup & CLI Skeleton

Create a Python package structure
Initialize click for the CLI
Configure basic command placeholders (yt-transcript, list, delete, etc.)
Add minimal logging setup
Core Transcript Fetching

Implement logic to parse YouTube URLs and extract video IDs
Add function to fetch transcripts from YouTube or from auto-generated captions
Cache transcript results
Save transcripts to JSON
Summarization with OpenAI GPT

Extract chapters from transcripts (or guess them if none are present)
Send each chapter (or chunk) to OpenAI GPT
Generate summaries and store them in JSON and Markdown
Whisper Integration

Detect if a transcript is unavailable
Use yt-dlp to extract audio
Call Whisper.cpp to transcribe audio
Save Whisper transcription to JSON
Advanced CLI Commands & Options

Implement list, delete, clear-cache
Add flags for --summarize, --markdown, --output-dir, --language, --whisper, --no-cache, etc.
Handle logging and error reporting consistently
Testing & Packaging

Implement pytest unit tests for each module
Mock out network calls for stable, repeatable tests
Provide coverage for caching, whisper fallback, summarization
Package using setuptools or poetry (publish to PyPI if desired)
2. Break Down Into Iterative Chunks
Here we partition the project into smaller deliverables that can be developed in logical order, each building on the previous. Each chunk is a unit of work that yields a stable, tested piece of the application.

Chunk 1: Basic CLI Skeleton & Logging

Create the click-based CLI
Implement the main command yt-transcript
Configure a logging mechanism
Provide a minimal help text
Chunk 2: URL Parsing & Basic Video Info Fetching

Add a function to parse YouTube URLs
Retrieve minimal metadata about a video (e.g., title, channel name)
Store data in an in-memory structure for now
Chunk 3: Official Transcript Fetching & Caching

Implement logic to fetch official or auto-generated captions
Add caching to save transcripts locally and avoid repeated network calls
Store transcripts in JSON files
Chunk 4: Summarization with OpenAI GPT

Integrate with OpenAI API
Split transcript into chapters or segments
Generate chapter-based summaries
Store summaries in JSON & Markdown
Chunk 5: Whisper Integration

If transcripts are unavailable, detect environment (e.g. Apple Silicon)
Extract audio with yt-dlp
Transcribe audio with Whisper.cpp
Save Whisper-based transcripts
Chunk 6: Additional CLI Commands & Options

Add list, delete, clear-cache commands
Add all relevant flags (--summarize, --markdown, --whisper, etc.)
Expand logging and error handling
Chunk 7: Testing, Refinements & Packaging

Unit tests for each subsystem with pytest
Validate caching logic, error handling, summarization correctness
Integrate coverage reports
Final packaging steps (e.g. setup.py, pyproject.toml)
3. Break Each Chunk Into Small, Safe, Testable Steps
We now detail each chunk further. We look for places to add testing right away, ensure steps are small enough to be integrated safely, and confirm there are no big leaps in complexity between steps.

Chunk 1: Basic CLI Skeleton & Logging
Create Project Structure
Create a directory yt_transcript/
Initialize a Python module structure: yt_transcript/__init__.py, yt_transcript/cli.py, etc.
Add Click to cli.py
Define the main CLI group @click.group()
Provide yt-transcript --help placeholder
Set Up Logging
Add a basic logging config (e.g., logging.basicConfig(level=logging.INFO))
Provide a --verbose option to increase log level
Sanity Test
Write a minimal test to invoke the CLI
Check that it returns help text or usage instructions
Chunk 2: URL Parsing & Basic Video Info Fetching
Write a Utility for URL/ID Extraction
Given a YouTube URL, parse out the video ID
Validate the format of the ID
Test with multiple types of YouTube links
Fetch Minimal Video Info (Mocked)
Create a function to fetch video title, channel name, etc.
Initially mock out the network calls for testing
Return a data object that includes basic video info
Integrate With CLI
Add an option to run a command like yt-transcript info <URL>
Display the fetched info in logs or console
Unit Tests
Test URL parsing with various valid/invalid inputs
Test mocked video info fetch for correct results
Confirm CLI handles common user mistakes gracefully
Chunk 3: Official Transcript Fetching & Caching
Transcript Fetching
Use the YouTube transcript API (e.g., youtube_transcript_api) or similar
Handle official transcripts first
Retry with auto-generated transcripts if official is unavailable
Caching
Create a cache directory (e.g., ~/.yt-transcript-cache/)
Store transcripts as JSON by <video_id>.json
Add a simple check to see if a transcript for the video is already cached
Provide a --no-cache CLI option
Integration & Testing
Expand the CLI to yt-transcript fetch <URL> to retrieve and cache transcript
Validate caching by calling the command twice
Add robust unit tests mocking YouTube transcript responses
Handle error states (video not found, transcript not available)
Chunk 4: Summarization with OpenAI GPT
Chapter Extraction or Creation
Parse YouTube chapter timestamps from the transcript if available
If not available, segment transcript by time or text length
Keep chapters in a structured list: [{"start": 312, "title": "Chapter 1", "end": 765}, ...]
OpenAI GPT Summaries
Write a function that sends transcript text + chapter context to OpenAI
Receive a summarized text
Mock OpenAI calls in tests
Storing Summaries
Store JSON in <video_id>_summary.json
Generate Markdown in <video_id>_summary.md
Include chapter timestamps as YouTube links
Integration & Testing
Add CLI flags like --summarize, --markdown
Test with short transcripts (mocked) to confirm the summarization flow
Validate error handling on OpenAI call timeouts or rate limits
Chunk 5: Whisper Integration
Audio Extraction
Use yt-dlp to extract audio
Handle different OS environments
Transcription with Whisper
Call Whisper.cpp with a chosen model
Map times to text for a transcript
Save result in <video_id>_whisper.json
Fallback Logic
If no official or auto-generated transcript is available, prompt user or automatically run Whisper
Add --whisper CLI option
Testing
Mock out Whisper calls in tests
Confirm integration with caching, file naming, fallback logic
Chunk 6: Additional CLI Commands & Options
list Command
Scan the output directory or cache directory
Print a table of stored transcripts with video ID, title, date
delete & clear-cache Commands
Remove a single transcript
Clear all transcripts or the entire cache
Confirmation prompts
All CLI Options
--output-dir, --language, --log-file
Validate that logs, caching, transcripts are all written to correct places
Testing
Test each command individually
Confirm correct log messages, error conditions
Chunk 7: Testing, Refinements & Packaging
Refine Tests
Expand coverage for all modules
Mock out YouTube and OpenAI calls
Validate concurrency or repeated calls
Packaging
Add a setup.py or pyproject.toml
Ensure correct entry point for the CLI
If desired, publish to PyPI
Documentation
Provide usage instructions in README
Add docstrings to public functions
Final Verification
Test actual network calls in a staging environment
Confirm that transcripts, summaries, and logs all behave as expected
4. Series of Code-Generation Prompts
Below is a set of prompts that you can give to a code-generation LLM to implement each chunk step-by-step using a test-driven approach. Each prompt is tagged with triple backticks. You would feed each prompt into your code-generation system sequentially, verifying the tests pass before moving on to the next step. Feel free to adjust or refine them to match your exact environment and naming conventions.

Prompt 1: Basic CLI Skeleton & Logging
vbnet
Copy
Edit
You are building the "yt-transcript" Python CLI tool. Start by creating the following structure:

1. A directory named "yt_transcript" with:
   - __init__.py (empty)
   - cli.py

2. In cli.py, create a click-based CLI group "yt_transcript_cli" with a single command, "main()":
   - When invoked, it should just print a greeting or basic help message.

3. Set up logging using Python's logging module:
   - Default to INFO level.
   - Add a "--verbose" flag that sets the logger level to DEBUG.

4. Write a Pytest test in "tests/test_cli.py" that checks:
   - The CLI runs without error when called with "--help".
   - The CLI prints the greeting or help text.

Return the code for all these files. Provide docstrings or inline comments to explain what each part does.
Make sure everything is syntactically correct and self-contained. 
Prompt 2: URL Parsing & Basic Video Info Fetching
mathematica
Copy
Edit
Continue building the "yt-transcript" tool. Now:

1. Create a new file, "yt_transcript/utils.py":
   - Implement a function "extract_video_id(youtube_url: str) -> str" that extracts the video ID.
   - For now, handle simple cases like "https://www.youtube.com/watch?v=VIDEO_ID".
   - Raise ValueError if the URL is invalid.

2. Add a function "fetch_video_info(video_id: str) -> dict":
   - Return a dict with mock data: {"title": "Mock Title", "channel_name": "Mock Channel", "video_id": video_id}.
   - We'll integrate real API calls later.

3. In "cli.py", add a command "info()" that:
   - Accepts a "url" argument.
   - Calls "extract_video_id" and "fetch_video_info".
   - Logs or prints the retrieved info.

4. In "tests/test_cli.py":
   - Add tests ensuring valid/invalid URLs behave correctly.
   - Check that "info" command prints the mock data.

Return all modified code. 
Prompt 3: Official Transcript Fetching & Caching
mathematica
Copy
Edit
Now implement transcript fetching and caching:

1. In "yt_transcript/transcript_fetcher.py":
   - Implement "fetch_transcript(video_id: str) -> list[dict]". 
     For now, simulate calling the YouTube transcript API by returning a mock transcript list of dicts: 
       [{"start": 0.0, "duration": 5.0, "text": "Mock transcript line."}]
   - Implement a caching mechanism in "~/.yt-transcript-cache/" or a platform-appropriate directory. 
     - If a JSON file "<video_id>.json" exists, load and return it.
     - Otherwise, generate the mock transcript, save it to JSON, and return it.
   - Handle a "--no-cache" flag that forces a fresh transcript fetch.

2. In "cli.py":
   - Add a command "fetch()" that:
     - Accepts a "url" argument.
     - Extracts video_id.
     - Calls "fetch_transcript".
     - Logs or prints the loaded transcript.

3. In "tests/test_transcript_fetcher.py":
   - Add tests to ensure caching logic works. 
   - Mock filesystem or environment calls for repeatable results. 
   - Check that transcripts are saved, loaded, or regenerated based on flags.

Return all modified code.
Prompt 4: Summarization with OpenAI GPT
python
Copy
Edit
Implement GPT-based summarization:

1. In "yt_transcript/summarizer.py":
   - Add a function "summarize_transcript(video_info: dict, transcript: list[dict]) -> dict" 
     that simulates calling OpenAI GPT. 
     For now, just return a mock summary: {"chapters": [{"title": "Mock Chapter", "summary": "Mock summary text"}]}. 
   - Later we will replace the mock with a real OpenAI API call.

2. In "cli.py":
   - Add a "--summarize" option to "fetch()" command for demonstration. 
   - If "--summarize" is set, after fetching the transcript, call "summarize_transcript" and log/print the summary.

3. In "yt_transcript/summarizer.py":
   - Add a helper "generate_markdown_summary(video_info: dict, summary_data: dict) -> str" 
     that produces a sample markdown string. 
   - Include video title, chapters with mock timestamps, etc.

4. Create "tests/test_summarizer.py":
   - Test "summarize_transcript" with a sample transcript. 
   - Check that "chapters" come back in the mock data.
   - Validate the markdown function output.

Return all modified code.
Prompt 5: Whisper Integration
vbnet
Copy
Edit
Add Whisper integration:

1. In "yt_transcript/whisper_integration.py":
   - Implement "transcribe_with_whisper(video_id: str, audio_path: str) -> list[dict]":
     - For now, mock the behavior: just return a mock list of transcript dicts.
     - We'll integrate actual Whisper calls later.
   - Handle the logic for detecting Apple Silicon (M1/M2) in a placeholder function "detect_macos_arm() -> bool".

2. In "cli.py":
   - Add a "--whisper" flag to "fetch()" so that if official transcripts are unavailable, the user can choose to run Whisper.
   - For demonstration, if the user passes "--whisper", call the "transcribe_with_whisper" function after simulating an unavailable official transcript.

3. Write "tests/test_whisper_integration.py":
   - Test that "transcribe_with_whisper" returns the mock transcripts.
   - Test the fallback logic when official transcripts are absent.

Return all modified code.
Prompt 6: Additional CLI Commands & Options
sql
Copy
Edit
Add more commands and refine CLI:

1. In "cli.py":
   - Implement "list" command:
     - Scans the cache directory (or the output dir).
     - Prints a table of found transcripts (video_id, title, date).
   - Implement "delete" command:
     - Deletes a specific transcript JSON and associated summaries if found.
   - Implement "clear-cache" command:
     - Deletes all transcripts in cache.

2. Add CLI options:
   - "--output-dir": specify where to store JSON/MD files.
   - "--language": pass a language code (e.g., "en", "es") to "fetch_transcript" or "transcribe_with_whisper" in the future.
   - "--log-file": specify an alternative path to store logs.

3. Update tests accordingly in "test_cli.py" and others:
   - Check "list" output, "delete" behavior, "clear-cache" behavior.

Return all updated code.
Prompt 7: Final Testing, Refinements & Packaging
sql
Copy
Edit
Finalize and package the project:

1. Create a "setup.py" or "pyproject.toml" to define "yt-transcript" as a CLI tool:
   - The entry point should be "yt_transcript.cli:yt_transcript_cli".

2. Refine the existing test files:
   - Ensure coverage for all modules: "utils.py", "transcript_fetcher.py", "summarizer.py", "whisper_integration.py", "cli.py".
   - Add a few integration tests that simulate an end-to-end run.

3. Update any mock logic to call real APIs if desired:
   - For production, implement actual calls to the YouTube transcript API, Whisper.cpp, and OpenAI GPT.
   - Keep a "mock mode" for tests.

4. Return the final project code with:
   - "setup.py" or "pyproject.toml"
   - All modules fully wired together
   - Instructions on how to install and run "yt-transcript"

Ensure no orphaned code remains. Everything should be integrated into a cohesive CLI tool.
5. Final Check & Iteration
Are these steps sufficiently small and testable?

Each chunk focuses on a discrete set of functionality, adding a small but meaningful feature set.
Each chunk has recommended tests, ensuring incremental, stable progress.
Are there any big leaps in complexity?

The introduction of OpenAI GPT and Whisper are somewhat more complex, but they are isolated in their own modules, introduced only after the foundation is built.
Is the final system cohesive?

The final prompts ensure everything is wired together, from CLI commands to caching, logging, and summarization.
By following these prompts in order, you incrementally build and test each feature of the yt-transcript tool until you reach a complete, production-ready system.

