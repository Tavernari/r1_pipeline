# R1 Pipeline

## Introduction
R1 Pipeline is a powerful Python-based pipeline that gives agentic capabilities to the Deepseek R1 reasoning model. It serves as an intelligent interface that can perform web searches, execute code, and scrape websites autonomously while maintaining a coherent conversation flow.

## Motivation
In the era of advanced AI models, there's a growing need for systems that can not only process information but also take actions based on that information. The R1 Pipeline was created to bridge this gap by providing a structured way for AI models to interact with various tools and services while maintaining a clear conversation flow and state management.

The project aims to:
- Enable AI models to perform real-world tasks autonomously
- Provide a structured framework for AI-driven decision making
- Create a reliable and extensible pipeline for AI operations

## Features

### Core Capabilities
- **Internet Search**: Perform web searches using DuckDuckGo's search engine
- **Code Execution**: Run Python code and capture its output
- **Web Scraping**: Extract and process content from websites
- **State Management**: Maintain conversation state and handle transitions

### Technical Features
- Built with modern Python using Pydantic for robust data validation
- Asynchronous support for efficient operation
- Modular design with clear separation of concerns
- Comprehensive error handling and state management
- Configurable through environment variables

## Contributing

We welcome contributions to the R1 Pipeline project! Here's how you can help:

### Prerequisites
- Python 3.x
- Required packages: openai==1.60.0, pydantic==2.10.5, duckduckgo_search==7.2.1, beautifulsoup4==4.12.3

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   - `DEEPSEEK_API_KEY`: Your Deepseek API key
   - `DEEPSEEK_BASE_URL`: Deepseek API base URL (optional)

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Document your code using docstrings
- Update requirements.txt if adding new dependencies

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description of the changes

## Support the Project
If you find R1 Pipeline useful and would like to support its development, please consider making a donation. See [DONATION_WALLETS.md](DONATION_WALLETS.md) for available donation options.

## License
This project is licensed under the MIT License - see the LICENSE file for details.