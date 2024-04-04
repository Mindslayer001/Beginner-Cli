
# Beginner CLI Tool

## Description

The Beginner CLI Tool is a Python-based command-line interface designed to assist beginners in learning and executing Linux commands interactively. It provides features such as command explanations and scenario-based command suggestions.

## Project Structure

```
.
├── beg_cli
│   ├── argsparser.py        # Main script for command-line parsing
│   ├── config.ini           # Configuration file
│   ├── demo.py              # Demo script or additional functionality
│   ├── __init__.py          # Initialization file for the CLI package
│   └── __pycache__          # Cache directory (automatically generated)
│       └── argsparser.cpython-311.pyc
├── LICENSE.md               # License file
├── poetry.lock              # Poetry lock file (dependency lock)
├── pyproject.toml           # Poetry project configuration
├── README.md                # Project README file (you are here!)
└── tests
    └── __init__.py          # Initialization file for tests (if any)
```

## Installation

To install the Beginner CLI Tool, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Mindslayer001/Beginner-Cli.git
    ```

2. Navigate into the project directory:

    ```bash
    cd Beginner-Cli
    ```

3. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

## Usage

To use the Beginner CLI Tool, you have several options:

1. **Command Explainer**: Provide basic information and examples of a specific Linux command.
   
    ```bash
    poetry run python beg_cli/argsparser.py --info [COMMAND]
    ```
   
    Example:
   
    ```bash
    poetry run python beg_cli/argsparser.py --info mkdir
    ```

2. **Scenario-based Command Suggestion**: Suggests commands based on a user scenario.
   
    ```bash
    poetry run python beg_cli/argsparser.py --scenario
    ```
   
    Example:
   
    ```bash
    poetry run python beg_cli/argsparser.py --scenario
    ```

To enable access to the Gemini API, you'll need to obtain an API key. Follow these steps to get your API key:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Obtain your brand new API key. The free tier is available with a few limitations.
3. Once you have your API key, replace the placeholder `YOUR_API_KEY` in the `config.ini` file located in the `beg_cli` directory with your actual API key.

```
[GENAI]
api_key = YOUR_API_KEY
```

With your API key configured, you'll be able to use the Beginner CLI Tool with access to the Gemini API.

## Contributing

Contributions to the Beginner CLI Tool are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your_feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your_feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

This project utilizes the Gemini API provided by [GenAI](https://genai.ai/) under their free tier. Please refer to the [GenAI Terms of Service](https://genai.ai/terms) for more information about the usage of their services.
