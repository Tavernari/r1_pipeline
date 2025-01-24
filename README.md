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
- **Internet Search**: Perform web searches using Tavily's search engine with customizable parameters
- **Code Execution**: Run Python code and capture its output
- **Web Scraping**: Extract and process content from websites using trafilatura
- **State Management**: Maintain conversation state and handle transitions
- **LLM Integration**: Built-in integration with Deepseek's language models for content analysis

### Technical Features
- Built with modern Python using Pydantic for robust data validation
- Asynchronous support for efficient operation
- Modular design with clear separation of concerns
- Comprehensive error handling and state management
- Configurable through environment variables

## Architecture

### Pipeline Components
1. **State Management**
   - Handles conversation flow through states: NEXT_STEP, ERROR, FINISHED, UNKNOWN
   - Manages recursive processing with configurable depth

2. **Tool Integration**
   - Internet Search: Customizable web search with filtering options
   - Code Execution: Secure Python code execution environment
   - Web Scraping: Robust content extraction from websites

3. **Message Processing**
   - Tag-based command system for tool interaction
   - Structured response format with confidence levels
   - Markdown output formatting

## Configuration

### Environment Variables
- `DEEPSEEK_API_KEY`: Your Deepseek API key for LLM access
- `DEEPSEEK_BASE_URL`: Deepseek API base URL (optional)
- `TVLY_API_KEY`: Your Tavily API key for web search functionality

### Search Parameters
- Search depth: 'basic' or 'advanced'
- Topic filtering: 'general' or 'news'
- Time range filtering: 'day', 'week', 'month', 'year'
- Domain inclusion/exclusion lists
- Image and description options

## Contributing

We welcome contributions to the R1 Pipeline project! Here's how you can help:

### Prerequisites
- Python 3.x
- Required packages: 
  - openai==1.60.0
  - pydantic==2.10.5
  - typing-extensions==4.12.2
  - schemas==0.7.1
  - tavily-python==0.5.0
  - trafilatura==2.0.0
  - lxml_html_clean==0.4.1

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   - `DEEPSEEK_API_KEY`: Your Deepseek API key
   - `DEEPSEEK_BASE_URL`: Deepseek API base URL (optional)
   - `TVLY_API_KEY`: Your Tavily API key

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Document your code using docstrings
- Update requirements.txt if adding new dependencies

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License - see LICENSE file for details