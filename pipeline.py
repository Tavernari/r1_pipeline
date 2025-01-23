"""
Title: r1-pipeline
Author: Victor Carvalho Tavernari
Date: 2025-01-23
Version: 0.0.1
License: MIT
Description:
    This pipeline give the agentic power to the model deepseek r1 reasoning model.
Requirements: openai==1.60.0, pydantic==2.10.5, duckduckgo_search==7.2.1, beautifulsoup4==4.12.3
"""

from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from typing import List, Union, Generator, Iterator, Optional
from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime
from openai import OpenAI
from duckduckgo_search import DDGS
import os
import json


# Mark: Functions

class TextWebSearchRequest(BaseModel):
    """
    Model representing a text web search request for DuckDuckGo.
    """
    keywords: str = Field(
        ...,
        description="Keywords for the query."
    )
    region: str = Field(
        description="Region code, e.g., 'wt-wt', 'us-en', 'uk-en', 'ru-ru'. Defaults to 'wt-wt'."
    )
    safesearch: str = Field(
        description="Safe search setting: 'on', 'moderate', 'off'. Defaults to 'moderate'."
    )
    timelimit: Optional[str] = Field(
        description="Time limit for search results: 'd' (day), 'w' (week), 'm' (month), 'y' (year). Defaults to None."
    )
    backend: str = Field(
        description=(
            "Backend to use for the search: 'api', 'html', 'lite'. Defaults to 'api'.\n"
            " - 'api' collects data from https://duckduckgo.com\n"
            " - 'html' collects data from https://html.duckduckgo.com\n"
            " - 'lite' collects data from https://lite.duckduckgo.com"
        )
    )
    max_results: Optional[int] = Field(
        description="Maximum number of results to return. If None, returns results only from the first response."
    )

    model_config = ConfigDict(
        extra='forbid',
    )

def execute_text_web_search_tool(text_web_search: TextWebSearchRequest) -> str:
        """
        Executes the text web search tool with the given parameters.
        """

        results = DDGS().text(
            keywords=text_web_search.keywords,
            region=text_web_search.region,
            safesearch=text_web_search.safesearch,
            timelimit=text_web_search.timelimit,
            backend=text_web_search.backend,
            max_results=text_web_search.max_results,
        )

        result = json.dumps(results, indent=0)
        return result

class WebSiteContent(BaseModel):
    """
    Model representing a website content.
    """
    url: str = Field(
        ...,
        description="URL of the website."
    )

    model_config = ConfigDict(
        extra='forbid',
    )

def execute_web_site_content_tool(web_site_content: WebSiteContent) -> str:
    """
    Executes the web site content tool with the given parameters.
    """
    logger.info(
        "(execute_web_site_content_tool) Getting content from URL: %s", web_site_content.url
    )
    try:
        html = urllib.urlopen(web_site_content.url).read()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                    for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        logger.debug(
            "(execute_web_site_content_tool) Web site content: %s", text
        )
        logger.info(
            "(execute_web_site_content_tool) Web site content complete for URL: %s", web_site_content.url
        )
        return text
    except Exception as e:
        logger.exception(
            "(execute_web_site_content_tool) Web site content failed for URL: %s", web_site_content.url
        )
        return str(e)

class CodeExecution(BaseModel):
    """
    Model representing a code execution request.
    """
    code: str = Field(
        ...,
        description="""
        The code to be executed in Python.
        To answer the step, you must add print statements to show the result of the code execution.
        """,
        strict=True,
    )

    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )

def execute_python_code(code: CodeExecution) -> (str, int):
    """
    Executes the given Python code and returns the output and return code.

    Args:
        code (str): The Python code to execute.

    Returns:
        Tuple[str, int]: A tuple containing the combined output and the return code.
    """
    try:
        result = subprocess.run(
            ["python", "-c", code.code],
            capture_output=True,
            text=True,
            check=True,
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # if fails, return the error message
        if result.returncode != 0:
            return stderr

        return stdout
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip()

        return stderr
    except Exception as e:
        return str(e)


# Mark: System Config

AVAILABLE_TOOLS = {
    "INTERNET_SEARCH": {
        "name": "Internet Search",
        "description": "Search the internet for the answer to the question.",
        "function": "internet_search",
        "input_description": TextWebSearchRequest.schema_json(),
    },
    "CODE_EXECUTER": {
        "name": "Code Executer",
        "description": "Execute code and return the result.",
        "function": "code_executer",
        "input_description": CodeExecution.schema_json(),
    },
    "SCRAPING": {
        "name": "Website Scraping",
        "description": "Scrape a specific website and return the content. If you need more information about the website, you must use the scraping tool.",
        "function": "scraping",
        "input_description": WebSiteContent.schema_json(),
    },
    "FINAL_ANSWER": {
        "name": "Final Answer",
        "description": "Return the final answer to the question, only if you are 100 percent sure about the answer",
        "function": "final_answer",
        "input_description": "The answer to the question.",
    },
}

def tag_generator(dict: dict) -> str:
    """
    Generate a tag from a tools dictionary
    Tag must start <function>{input_description}</function>
    """
    function = dict.get("function")
    return (
        f"\nFunction {dict.get('name')}: {dict.get('description')}\n"
        f"<{function}>{dict.get('input_description')}</{function}>\n"
    )

def available_tools_tags_generator(dict: dict) -> str:
    """
    Generate a tag from a tools dictionary
    Tag must start <function>{input_description}</function>
    """
    return "\n".join([tag_generator(dict) for dict in dict.values()])

SYSTEM_PROMPT = (
    "You should help the user to answer the question using the available tools."
    "Now is: {now}"
    "Your ouput MUST be only a tag based on these available tools:"
    f"Available tools: {available_tools_tags_generator(AVAILABLE_TOOLS)}"
    "MANDATORY: "
    " - Only return one tag per interaction"
    " - If you have source of the information, you must link on the final answer"
    " - Output must be in markdown format"
    " - You must answer using the same language of the question"
)

# MARK: Pipeline

# Enum State
class State(str, Enum):
    """
    Enum for the state of the pipeline.
    """
    NEXT_STEP = "next_step"
    ERROR = "error"
    FINISHED = "finished"

class StateResult(BaseModel):
    """
    Model representing the state of the pipeline.
    """
    state: State = Field(
        ...,
        description="The state of the pipeline."
    )
    message: str = Field(
        ...,
        description="The message to be sent to the user."
    )

class Pipeline:
    class Valves(BaseModel):
        DEEPSEEK_API_KEY: str = ""
        BASE_URL: str = "https://api.deepseek.com"
        pass

    def __init__(self):
        self.name = "🤖 R1 Deepseek Reasoner"
        self.valves = self.Valves(
            **{
                "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY", "your-deepseek-api-key-here"),
                "BASE_URL": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            }
        )
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        self.client = OpenAI(
            api_key=self.valves.DEEPSEEK_API_KEY,
            base_url=self.valves.BASE_URL
        )
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def calculate_state(self, assistant_message: str) -> StateResult:
        # This function is called when the server is started.
        print(f"calculate_state:{__name__}")

        # Check if the assistant message contains the tag for the Internet Search tool.
        if "<internet_search>" in assistant_message:
            try:
                # extract content between <internet_search> and </internet_search>
                content = assistant_message.split("<internet_search>")[1].split("</internet_search>")[0]
                text_web_search = TextWebSearchRequest(**json.loads(content))

                if text_web_search.keywords == None or text_web_search.keywords == "":
                    return StateResult(
                        state=State.NEXT_STEP,
                        message="Please provide the keywords for the search."
                    )

                # Execute the text web search tool.
                result = execute_text_web_search_tool(text_web_search)
                # Return the result as a message.
                return StateResult(
                    state=State.NEXT_STEP,
                    message=f"<internet_search.result>{result}</internet_search.result>"  
                )
            except Exception as e:
                return StateResult(
                    state=State.ERROR,
                    message=f"Error parsing the text web search request: {e}"
                ) 
        
        if "<code_executer>" in assistant_message:
            try:
                # extract content between <code_executer> and </code_executer>
                content = assistant_message.split("<code_executer>")[1].split("</code_executer>")[0]
                code_execution = CodeExecution(**json.loads(content))
                result = execute_python_code(code_execution)
                # Return the result as a message.
                return StateResult(
                    state=State.NEXT_STEP,
                    message=f"<code_executer.result>{result}</code_executer.result>"
                )
            except Exception as e:
                return StateResult(
                    state=State.ERROR,
                    message=f"Error parsing the code executer request: {e}"
                )

        if "<scraping>" in assistant_message:
            try:
                # extract content between <scraping> and </scraping>
                content = assistant_message.split("<scraping>")[1].split("</scraping>")[0]
                web_site_content = WebSiteContent(**json.loads(content))
                result = execute_web_site_content_tool(web_site_content)
                # Return the result as a message.
                return StateResult(
                    state=State.NEXT_STEP,
                    message=f"<scraping.result>{result}</scraping.result>"
                )
            except Exception as e:
                return StateResult(
                    state=State.ERROR,
                    message=f"Error parsing the scraping request: {e}"
                )
        if "<final_answer>" in assistant_message:
            try:
                # extract content between <final_answer> and </final_answer>
                content = assistant_message.split("<final_answer>")[1].split("</final_answer>")[0]
                # Return the result as a message.
                return StateResult(
                    state=State.FINISHED,
                    message=content
                )
            except Exception as e:
                return StateResult(
                    state=State.ERROR,
                    message=f"Error parsing the final answer request: {e}"
                )

    def process_state(self, messages: List[dict], max_depth: int = 5) -> str:
        """Recursively process state transitions and messages."""
        if max_depth <= 0:
            return "Max recursion depth exceeded"

        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=False
        )

        assistant_message = response.choices[0].message.content
        reasoning_content = response.choices[0].message.reasoning_content

        print((
            "\n\n------- Reasoning ------\n"
            f"{reasoning_content}"
            "------------------------\n\n\n"
        ))

        messages.append({"role": "assistant", "content": assistant_message})

        state_result = self.calculate_state(assistant_message)
        print(f"State Result: {state_result}")

        if state_result.state == State.FINISHED:
            return state_result.message
        elif state_result.state == State.ERROR:
            messages.append({"role": "user", "content": state_result.message})
            return self.process_state(messages, max_depth - 1)
        elif state_result.state == State.NEXT_STEP:
            messages.append({"role": "user", "content": state_result.message})
            return self.process_state(messages, max_depth - 1)
        else:
            return "Error: Invalid state"

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Main pipeline entry point with recursive state handling."""
        print(f"pipe:{__name__}")

        system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT.replace("{now}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        messages = [system_message] + messages + [
            {"role": "user", "content": user_message}
        ]

        return self.process_state(messages).strip()