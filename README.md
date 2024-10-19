# OpenAI Image Data Extraction

## Overview

The OpenAI Image Data Extraction scripts serve the purpose of processing PDF documents to extract text and image content using OpenAI's language models. These scripts provide functionality to convert PDF files into images, encode images, and generate readable message content through the OpenAI API. They are designed to facilitate the automatic extraction, summarization, and organization of document content into JSON format.

## Prerequisites

- **Python 3.7+** is required to run these scripts.
- An **OpenAI API key** is necessary to interact with OpenAI models. This should be stored in an `.env` file as `OPENAI_API_KEY`.
- Dependencies include:
  - [OpenAI Python library](https://github.com/openai/openai-python).
  - [pdf2image](https://pypi.org/project/pdf2image/) to convert PDF files into images.
  - [python-dotenv](https://pypi.org/project/python-dotenv/) for loading environment variables.
  
Ensure these packages are installed using pip:

```bash
pip install openai pdf2image python-dotenv
```

## Usage

### File: `app-docstring.py`

- **Purpose**: This script demonstrates the procedure of processing a single PDF file, converting it to images, and interacting with the OpenAI API to extract and summarize content.
- **Example**:

  ```python
  if __name__ == "__main__":
      script = OpenAI_Image_Data_Extraction()
      script.file_path = r"OpenAI-Blog.pdf"
      script.system_prompt = """Summarize the content for a markdown document"""
      script.process_file()
  ```

  This will process `OpenAI-Blog.pdf`, summarizing its content using the OpenAI model.
  
### File: `app.py`

- **Purpose**: This script extends `app-docstring.py` by adding functionality to process multiple PDF files within a directory and save the result as a JSON.
- **Example**:

  ```python
  if __name__ == "__main__":
      script = OpenAI_Image_Data_Extraction()
      directory = r"path/to/directory"
      script.system_prompt = """Extract detailed lesson content to JSON..."""
      script.process_multiple_files(directory, json_filename='result.json')
  ```

  This processes all PDFs in the specified directory and appends the extracted content to `result.json`.

## Key Functions and Methods

- `check_file_path()`: Validates the file path for processing.
- `convert_pdf_to_images(pdf_path, output_folder)`: Converts the PDF to a series of images stored in the given folder.
- `message_with_images(images)`: Encodes images as base64 and creates a user message for OpenAI API consumption.
- `system_message()`: Prepares the system's initial message configuration.
- `run_openai(messages)`: Calls the OpenAI API to process provided messages.
- `process_file()`: Wrapper method to execute file processing and API interaction.
- `process_multiple_files(directory, json_filename)`: Processes multiple PDFs in a directory, saving outputs in JSON format.

## Configuration Options

- **API Key**: Must be set in a `.env` file.
- **Model Name**: Configure the model via `model_name` during initialization, defaulting to `"gpt-4-vision-preview"`.
- **Page Range**: Optional `first_page` and `last_page` attributes to limit PDF conversion to specific pages.
- **System/User Prompts**: