# README - OpenAI Image Data Extraction

This module provides an efficient solution for extracting data from images and PDFs using the OpenAI API. It parses a set of images or a pdf file and returns a response based on the user prompt.

## How to use the module

Below are the steps to use the module:

1. Initialize the module as per your requirement
2. Provide the path of the image or pdf file in `file_path`
3. [Optional] For pdf files specify the `first_page` and `last_page` for parsing specific pages
4. Provide the instruction in `system_prompt`
5. Run `process_file` function to get the inference

## Features

- PDF to image conversion: The module can convert each page of a PDF to an image which is then processed by the AI model.
- System/user prompts: It allows the user to specify system and user prompts to guide the data extraction process.
- Customizable options: You can customize several options, like the AI model and maximum tokens.

## Example 

This is a basic implementation of the module:

```python
    if __name__ == "__main__":
        script = OpenAI_Image_Data_Extraction()
        script.file_path = r"OpenAI-Blog.pdf"
        script.system_prompt = "Summarize the content for a markdown document"
        script.process_file()
```

You can also set `first_page` and `last_page` to process specific pages:

```python
    if __name__ == "__main__":
        script = OpenAI_Image_Data_Extraction()
        script.file_path = r"OpenAI-Blog.pdf"
        script.first_page = 2
        script.last_page = 4
        script.system_prompt = "Summarize the content for a markdown document"
        script.process_file()
```

## Getting Started

Refer to the [OpenAI API documentation](https://beta.openai.com/docs/guides/chat/) for detailed steps on how to use and configure the OpenAI API.

![OpenAI Logo](https://styles.redditmedia.com/t5_2nka6/styles/communityIcon_90r63d0n8uu41.png?width=256&s=e4b937d5f786fe18d25553881d0dc0f3)

The **system prompt** is used to guide the AI model's extraction process. For instance, to extract and summarize text, the system prompt would be something like "Summarize the content for a markdown document".

The **user prompt** typically includes more specific instructions and the data for the model to parse.

## Contributing/Feedback

We would love your contributions and feedback on this code. For any questions or issues, please open an issue on GitHub.