# ZMP Markdown Translator

![Platform Badge](https://img.shields.io/badge/platform-zmp-red)
![Component Badge](https://img.shields.io/badge/component-translator-red)
![CI Badge](https://img.shields.io/badge/ci-github_action-green)
![License Badge](https://img.shields.io/badge/license-MIT-green)
![PyPI - Version](https://img.shields.io/pypi/v/zmp-md-translator)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/zmp-md-translator)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zmp-md-translator)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/zmp-md-translator)

A high-performance markdown translator that supports multiple languages and preserves markdown formatting. Uses OpenAI's GPT models for translation.

## Features

- Translates entire directories of markdown files
- Preserves markdown formatting and structure
- Supports multiple target languages simultaneously
- Handles large files through automatic chunking
- Maintains Docusaurus-compatible directory structures
- Shows real-time progress with colorized output

## Installation

```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install .
```

## Usage

### Basic Command Structure

```bash
poetry run zmp-translate \
  --source-dir SOURCE_DIR \
  --target-dir TARGET_DIR \
  --languages LANG_CODES
```

### Example Usage

```bash
poetry run zmp-translate \
  --source-dir "./repo/docs/ZCP" \
  --target-dir "./repo/i18n" \
  --languages "ko,ja,zh"
```
or
```bash
poetry run zmp-translate \
  --s "./repo/docs/ZCP" \
  --t "./repo/i18n" \
  --l "ko,ja,zh"
```
### Command Line Options

- `-s, --source-dir`: Source directory containing markdown files (required)
- `-t, --target-dir`: Target directory for translations (default: "i18n")
- `-l, --languages`: Comma-separated list of target language codes (required)
- `-m, --model`: OpenAI model to use (overrides .env setting)
- `-c, --chunk-size`: Maximum chunk size for translation (overrides .env setting)
- `-n, --concurrent`: Maximum concurrent requests (overrides .env setting)

### Supported Language Codes

The following language codes are supported:

| Code | Language    |
|------|------------|
| ko   | Korean     |
| fr   | French     |
| ja   | Japanese   |
| es   | Spanish    |
| de   | German     |
| zh   | Chinese    |
| ru   | Russian    |
| it   | Italian    |
| pt   | Portuguese |
| ar   | Arabic     |

### Environment Configuration

Create a `.env` file in your project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=your-model-here

# Performance Settings
MAX_CHUNK_SIZE=4000
MAX_CONCURRENT_REQUESTS=5
```

## Directory Structure

The translator maintains a Docusaurus-compatible directory structure based on the source directory name:

- For `*_zcp` sources:
  ```
  [target_dir]/[lang]/docusaurus-plugin-content-docs-zcp/current/
  ```
- For `*_apim` sources:
  ```
  [target_dir]/[lang]/docusaurus-plugin-content-docs-apim/current/
  ```
- For `*_amdp` sources:
  ```
  [target_dir]/[lang]/docusaurus-plugin-content-docs-amdp/current/
  ```
- For other sources:
  ```
  [target_dir]/[lang]/docusaurus-plugin-content-docs/current/
  ```

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run test

# Run tests with watch mode
poetry run watch
```

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.
