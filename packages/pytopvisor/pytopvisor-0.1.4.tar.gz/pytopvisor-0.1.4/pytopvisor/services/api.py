import requests
from pytopvisor.utils.logger import logger
from pytopvisor.utils.exceptions import (
    TopvisorAPIError,
    ERROR_MAPPING
)


class TopvisorAPI:
    def __init__(self, user_id, api_key):
        self.base_url = "https://api.topvisor.com"
        self.headers = {
            "Content-type": "application/json",
            "User-Id": user_id,
            "Authorization": f"bearer {api_key}",
        }

    def send_request(self, endpoint, payload):

        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            # Logging a successful request
            logger.debug(f"API request completed successfully: {url}")

            # Attempt to parse the response as JSON
            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"JSON parsing error: {e}. Response: {response.text}")
                raise RuntimeError("Response from API is not valid JSON.")

            # Check for errors in the response
            if "errors" in data and data["errors"]:
                self._handle_api_errors(url, data["errors"])

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during API request: {e}")
            raise

    def send_text_request(self, endpoint, payload):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.debug(f"API request completed successfully: {url}")
            return self.parse_text_response(response.text)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during API request: {e}")
            raise

    def parse_text_response(self, text, delimiter=";"):
        """
        Parses a text response in CSV format with a specified delimiter.
        :param text: Text response from the API.
        :param delimiter: Delimiter used in the text (default ';').
        :return: A list of lists containing the data.
        """

        decoded_text = text.encode("raw_unicode_escape").decode("cp1251")
        lines = decoded_text.strip().split("\n")
        result = []

        for line in lines:
            values = line.split(delimiter)
            result.append(values)

        return result

    def _handle_api_errors(self, url, errors):
        """
        Handles API errors and raises appropriate exceptions.
        """
        for error in errors:
            code = error.get("code")
            message = error.get("string", "Unknown error")
            detail = error.get("detail", "")

            logger.error(
                f"API Error [{code}]: {message}. Details: {detail}. URL: {url}"
            )

            exception_class = ERROR_MAPPING.get(code, TopvisorAPIError)
            raise exception_class(f"[{code}] {message}. {detail}")

