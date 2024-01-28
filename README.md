# OpenAI Image Data Extraction

## Overview

The OpenAI Image Data Extraction script is designed to process images or PDF files, converting the visual content into text-based summaries using OpenAI's GPT-4 Vision API. The code can handle both individual images and multiple pages of a PDF, converting each page into an image for analysis.

## Dependencies

To run this script, you will need the following dependencies installed:

- `openai` - The OpenAI Python client library.
- `pdf2image` - A library for converting PDF files to images.
- `python-dotenv` - To load environment variables from the `.env` file.
- `base64` - A Python module for encoding binary data to ASCII characters.
- `os` and `pathlib` - Standard libraries for file and path operations in Python.

You must also have an active OpenAI account with API key access.

## Environment Setup

Before running the script, make sure to set up the environment variables:

1. Create a `.env` file in the script's directory.
2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY='your_api_key_here'
   ```

## Usage

To use the script, follow these steps:

1. Initialize the `OpenAI_Image_Data_Extraction` class.
2. Set the `file_path` with the path to your image or PDF file.
3. (Optional) Set `first_page` and `last_page` if you want to process a subset of pages from a PDF.
4. Set the `system_prompt` with instructions for the OpenAI model.
5. Call the `process_file()` method.

### Example

```python
script = OpenAI_Image_Data_Extraction()
script.file_path = "path_to_your_file.pdf"
script.system_prompt = "System prompt that describes what you want to extract or process"
result = script.process_file()
```

## Configuration Options

- `model_name`: Set the model to be used for processing images. Default is `gpt-4-vision-preview`.
- `max_tokens`: Maximum number of tokens to generate in the output.

## Design Decisions

- The class inherits from OpenAI and adds functionality specific to handling images and PDF conversions.
- PDF files are converted to images first to accommodate the OpenAI API's image processing capabilities.
- The code follows a pattern of preparing the input as a sequence of messages before sending it to the OpenAI API.

## Limitations and Future Improvements

- The script currently assumes all images in a PDF need to be processed. Fine-grained control over which pages to convert would be a welcome addition.
- Adding support for different image formats or specific image processing requirements can increase the utility of the script.
- Error handling and logging can be improved to handle various edge cases more gracefully.

## Contributing

If you are interested in contributing to the development of this script, please ensure you follow the best practices for Python coding and adhere to the existing design patterns within the codebase.