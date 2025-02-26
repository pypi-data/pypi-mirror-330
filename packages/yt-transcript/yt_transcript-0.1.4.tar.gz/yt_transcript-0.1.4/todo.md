# TODO Checklist for `yt-transcript` Project

A step-by-step checklist to guide the development of the `yt-transcript` tool. Each phase builds on the previous phases, ensuring incremental progress, thorough testing, and cohesive integration.

---

## Phase 1: Basic CLI Skeleton & Logging

- [x] **Create Project Structure**
  - [x] Create a top-level directory named `yt_transcript/`.
  - [x] Within it, add `__init__.py` (empty) and `cli.py`.
  - [x] Prepare a `tests/` directory for test files.

- [x] **Implement Basic CLI with Click**
  - [x] In `cli.py`, create a `click` group (e.g., `yt_transcript_cli`).
  - [x] Add a `main()` command or similar placeholder that prints basic help or a greeting.
  - [x] Ensure `yt-transcript --help` shows usage instructions.

- [x] **Set Up Logging**
  - [x] Configure Python's `logging` in `cli.py` (or a dedicated logger file).
  - [x] Set default level to `logging.INFO`.
  - [x] Add a `--verbose` flag that toggles logging to `DEBUG`.

- [x] **Create a Basic Test**
  - [x] In `tests/test_cli.py`, write a test to invoke the CLI with `--help`.
  - [x] Verify it runs without errors and prints the help text.

---

## Phase 2: URL Parsing & Basic Video Info Fetching

- [ ] **Utility for URL/ID Extraction**
  - [ ] Create `yt_transcript/utils.py`.
  - [ ] Implement `extract_video_id(youtube_url: str) -> str` with basic validation.
    - [ ] Handle standard YouTube link patterns (`v=VIDEO_ID`).
    - [ ] Raise `ValueError` for invalid URLs.

- [ ] **Mock Video Info Fetching**
  - [ ] In `utils.py`, create `fetch_video_info(video_id: str) -> dict`.
    - [ ] Return a mock dictionary (e.g., `{"title": "...", "channel_name": "...", "video_id": video_id}`).
    - [ ] Prepare to replace with real API calls later.

- [ ] **Integrate with CLI**
  - [ ] In `cli.py`, add a command (e.g., `info`) that:
    - [ ] Accepts a `url` argument.
    - [ ] Parses the video ID, fetches mock info, and logs/prints it.

- [ ] **Tests**
  - [ ] In `tests/test_cli.py`, test `info` command:
    - [ ] Validate correct output for valid URL.
    - [ ] Validate it raises an error for invalid URLs.
  - [ ] Confirm logs or prints match expected mock data.

---

## Phase 3: Official Transcript Fetching & Caching

- [ ] **Transcript Fetching**
  - [ ] Create `yt_transcript/transcript_fetcher.py`.
  - [ ] Implement `fetch_transcript(video_id: str) -> list[dict]`:
    - [ ] For now, return a mock transcript list (e.g., `[{"start": 0.0, "duration": 5.0, "text": "Line"}]`).
    - [ ] Later, integrate with an official YouTube transcript API.
  - [ ] Handle fallback to auto-generated transcripts if official is unavailable.

- [ ] **Caching Mechanism**
  - [ ] Decide on a cache directory (e.g., `~/.yt-transcript-cache/`).
  - [ ] Check if `<video_id>.json` already exists:
    - [ ] If yes, load and return it.
    - [ ] If not, fetch a new transcript, save it as JSON, and return it.
  - [ ] Add `--no-cache` option to bypass caching.

- [ ] **CLI Integration**
  - [ ] In `cli.py`, add a command (e.g., `fetch`) that:
    - [ ] Accepts a `url` argument.
    - [ ] Extracts `video_id`, calls `fetch_transcript`.
    - [ ] Prints or logs the transcript result.

- [ ] **Tests**
  - [ ] In `tests/test_transcript_fetcher.py`:
    - [ ] Mock file I/O to test the caching flow (cache hit vs. cache miss).
    - [ ] Verify that transcripts are saved and loaded correctly.
    - [ ] Check behavior with `--no-cache`.

---

## Phase 4: Summarization with OpenAI GPT

- [ ] **Chapter Extraction or Creation**
  - [ ] Determine how to split the transcript into chapters:
    - [ ] If YouTube's chapter timestamps exist, parse them.
    - [ ] Otherwise, chunk by time segments or text length.

- [ ] **OpenAI GPT Summaries**
  - [ ] Create `yt_transcript/summarizer.py`.
  - [ ] Implement `summarize_transcript(video_info: dict, transcript: list[dict]) -> dict`.
    - [ ] For now, return a mock summary structure (e.g., `{"chapters": [{"title": "Mock", "summary": "Text"}]}`).
    - [ ] Later, replace with a real OpenAI API call.

- [ ] **Markdown Summary Generation**
  - [ ] In the same file, add `generate_markdown_summary(video_info: dict, summary_data: dict) -> str`.
    - [ ] Format a simple Markdown doc with chapter titles, timestamps, etc.

- [ ] **CLI Integration**
  - [ ] Add a `--summarize` flag to the `fetch` command or create a new command (e.g., `summarize`).
  - [ ] If `--summarize`, after fetching transcripts, call `summarize_transcript` and log/print the result.
  - [ ] Optionally save the summary JSON or Markdown in the same directory.

- [ ] **Tests**
  - [ ] In `tests/test_summarizer.py`:
    - [ ] Test the mock summarization function.
    - [ ] Validate the Markdown output structure.
    - [ ] Confirm error handling (e.g., empty transcript, missing video_info).

---

## Phase 5: Whisper Integration

- [ ] **Audio Extraction with `yt-dlp`**
  - [ ] Create `yt_transcript/whisper_integration.py`.
  - [ ] Implement a placeholder function to call `yt-dlp` and get an audio file path.
    - [ ] For now, mock the process of downloading.

- [ ] **Local Whisper Transcription**
  - [ ] In the same file, implement `transcribe_with_whisper(video_id: str, audio_path: str) -> list[dict]`:
    - [ ] Return a mock list of transcripts (e.g., `[{"start": 0.0, "duration": 3.0, "text": "Whisper mock line"}]`).
    - [ ] Later, integrate real Whisper.cpp calls.

- [ ] **Fallback Logic**
  - [ ] Detect if official transcripts are unavailable. 
  - [ ] If `--whisper` is provided, run Whisper transcription automatically.
  - [ ] Save the Whisper-based transcript as `<video_id>_whisper.json`.

- [ ] **Tests**
  - [ ] In `tests/test_whisper_integration.py`:
    - [ ] Mock `yt-dlp` calls and Whisper interactions.
    - [ ] Confirm fallback logic when official transcripts are missing.
    - [ ] Check correct file naming and caching approach.

---

## Phase 6: Additional CLI Commands & Options

- [ ] **`list` Command**
  - [ ] In `cli.py`, implement a command to scan the cache directory (or specified output directory).
  - [ ] Print a table listing known transcripts with columns: video_id, title, date, etc.

- [ ] **`delete` Command**
  - [ ] Add `delete <video_id>` command.
  - [ ] Confirm and remove the JSON transcript file (and any summary files) for that video.

- [ ] **`clear-cache` Command**
  - [ ] Add a command that deletes all cached transcripts or a subset.
  - [ ] Provide a confirmation prompt.

- [ ] **Expanded CLI Options**
  - [ ] `--output-dir <path>`: specify where to store JSON/Markdown files.
  - [ ] `--language <lang>`: pass a language code to transcript fetch / whisper logic.
  - [ ] `--log-file <path>`: override default log file path.

- [ ] **Tests**
  - [ ] In `tests/test_cli.py`:
    - [ ] Validate `list` output.
    - [ ] Confirm `delete` removes the correct files.
    - [ ] Check that `clear-cache` behaves as expected.
    - [ ] Test new CLI options (output directory, language, etc.).

---

## Phase 7: Final Testing, Refinements & Packaging

- [ ] **Refine & Expand Tests**
  - [ ] Ensure all modules have thorough test coverage.
  - [ ] Use mocks for network calls (YouTube, OpenAI, Whisper).
  - [ ] Test typical user flows end-to-end (fetch transcript, summarize, list, delete, etc.).

- [ ] **Replace Mocks with Real Implementations (Optional)**
  - [ ] Integrate actual YouTube Transcript API or other official approach.
  - [ ] Call OpenAI GPT endpoints for real summaries.
  - [ ] Set up Whisper.cpp for actual audio transcription.
  - [ ] Provide environment variables or config for API keys.

- [ ] **Packaging**
  - [ ] Create `setup.py` or `pyproject.toml` with `entry_points` referencing the main CLI (`yt_transcript.cli:yt_transcript_cli`).
  - [ ] Verify `pip install .` or `pip install --editable .` sets up the CLI tool correctly.
  - [ ] Add versioning (e.g., 0.1.0) in a `__version__` variable or config file.

- [ ] **Documentation**
  - [ ] Write or update `README.md` with usage examples and instructions.
  - [ ] Add docstrings to all public functions.
  - [ ] Optionally generate Sphinx or MkDocs documentation.

- [ ] **Final Verification**
  - [ ] Run all tests to ensure 100% pass.
  - [ ] Manually test the CLI in a fresh environment.
  - [ ] Validate caching, transcripts, summaries, and logs are produced as expected.

---

## Optional & Future Enhancements

- [ ] **GUI or Web Frontend**
  - [ ] Consider building a lightweight web interface for non-technical users.

- [ ] **Multi-Language Summaries**
  - [ ] Detect transcript language automatically for summarization.
  - [ ] Provide translation features if desired.

- [ ] **Advanced Logging & Error Handling**
  - [ ] Log to different output channels (JSON logs, rotating logs, etc.).
  - [ ] Add more robust error messages for missing APIs or dependencies.

- [ ] **CI/CD Pipeline**
  - [ ] Set up GitHub Actions or another CI service for automated testing and linting.
  - [ ] Automate PyPI releases on tagged commits.

