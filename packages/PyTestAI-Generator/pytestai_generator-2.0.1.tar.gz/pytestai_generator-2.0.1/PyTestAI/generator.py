# PyTestAI/generator.py

import os
import logging
import requests
import time
from pathlib import Path
from .utils import _get_api_key, _payload_setup, _extract_marked_definitions, _clean_api_response
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama for cross-platform support
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
MAX_RETRIES = 3 

def generate_test_cases(file_path: Path) -> str:
    """
    Generates pytest test cases for the given Python file using the DeepSeek API
    and saves them to a test file.

    Args:
        file_path (Path): Path to the original Python file.

    Returns:
        str: Path to the generated test file.
    """
    # Validate file path
    if not file_path.exists():
        logging.error(Fore.RED + f"❌ File '{file_path}' not found.")
        raise FileNotFoundError(f"❌ File '{file_path}' not found.")

    # Extract source code from the file
    source_code = _extract_marked_definitions(file_path)

    # Get the DeepSeek API key
    api_key = _get_api_key()

    # Prepare the API request payload
    payload = _payload_setup(file_path=file_path, source_code=source_code, model="deepseek-chat", temperature=1.0)

    # Call the DeepSeek API with retries
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        logging.info(Fore.CYAN + f"🔄 Generating test cases for file: {file_path} (Attempt {attempt}/{MAX_RETRIES})")

        # Display a progress bar while waiting for response
        with tqdm(total=15, desc="Processing", bar_format="{l_bar}{bar} {remaining}") as progress_bar:
            for _ in range(15):
                time.sleep(1)
                progress_bar.update(1)

        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

        if response.status_code == 429:  # Too Many Requests
            logging.warning(Fore.YELLOW + "⚠️ Rate limit exceeded. Retrying in 5 seconds...")
            time.sleep(5)
        else:
            break

    # Ensure API request was successful
    response.raise_for_status()

    try:
        response_data = response.json()
        test_code = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not test_code:
            raise ValueError("❌ Received empty test case from DeepSeek API.")
    except (IndexError, KeyError, ValueError) as e:
        logging.error(Fore.RED + f"🚨 Unexpected API response: {response.text}")
        raise RuntimeError("❌ Failed to generate test cases from API response.") from e

    # Convert explanations into comments and clean markdown artifacts
    # test_code = "\n".join(
    #     f"# {line}" if line.strip() and not line.strip().startswith(("#", "```", "from", "import", "def", "assert"))
    #     else line
    #     for line in test_code.splitlines()
    # )

    # # Remove markdown code blocks and "bash" keyword if present
    # test_code = re.sub(r"```(\w+)?", "", test_code).strip()
    # test_code = test_code.replace("bash", "").strip()
    # # Remove leading/trailing whitespace and empty lines
    # test_code = "\n".join(line for line in test_code.splitlines() if line.strip())

    # Clean up the test code
    test_code = _clean_api_response(test_code)

    # Save the test code to a file
    test_file_path = file_path.parent / f"test_{file_path.name}"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    logging.info(Fore.GREEN + f"✅ Test file successfully generated: {test_file_path}")
    return str(test_file_path)
