# ASK CONNECT CLI

ASK CONNECT CLI is a command-line application that allows users to interact with Google's Gemini AI models. It enables users to select AI models, ask questions, and receive AI-generated responses. The application also supports environment variable configuration and automatically sets default values upon installation.

## Features

- Select from available Gemini AI models
- Ask AI-powered questions and get real-time responses
- Rich CLI interface using `typer`, `rich`, and `InquirerPy`
- Automatic environment variable setup
- Supports `.env` file for persistent settings

## Installation

### Prerequisites

Ensure you have Python 3.10+ installed. You can check your version by running:
```sh
python --version
```

### Install from PyPI
You can install ASK CONNECT CLI using `pip`:
```sh
pip install ask-connect-cli
```

### Manual Installation
Clone the repository and install dependencies:
```sh
git clone https://github.com/yourusername/ask-connect-cli.git
cd ask-connect-cli
pip install -r requirements.txt
```

## Usage

### 1. Set up the API Key
Before using the CLI, set your Gemini API key:
```sh
export GEMINI_API_KEY='your_api_key'
```
For Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_api_key"
```
Alternatively, you can add it to a `.env` file in the project directory:
```sh
echo "GEMINI_API_KEY=your_api_key" > .env
```

### 2. Select an AI Model
Run the following command to list available AI models and select one:
```sh
ask models
```
This will allow you to choose a model interactively and save it in the `.env` file.

### 3. Ask a Question
Once a model is selected, ask a question using:
```sh
ask q "What is the capital of France?"
```

## Environment Variables
The CLI automatically sets up default environment variables upon installation. These can be found in the `.env` file:
```ini
GRPC_VERBOSITY=ERROR
GRPC_ENABLE_FORK_SUPPORT=0
CURRENT_MODEL=gemini-1.5-flash
```
If needed, you can manually edit these values in `.env`.

## Development
If you want to contribute or modify the project, follow these steps:
```sh
git clone https://github.com/AutoDictate/ask-connect-cli.git
cd ask-connect-cli
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Publishing to PyPI
To publish a new version to PyPI:
```sh
python -m build
python -m twine upload dist/*
```

## License
This project is licensed under the MIT License.

## Contact
For support or issues, open an issue on GitHub or contact `techie4coffee@gmail.com`.

