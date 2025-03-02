import json
from curl_cffi import requests

COMMON_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Mode": "cors",
    "Accept-Encoding": "gzip, deflate",
    "Origin": "https://grok.com",
    "Cookie": None,
    "Priority": "u=3, i",
}

class GrokAPIAuth:
    def __init__(self, cookies: dict = None, cookie_string: str = None):
        if cookies is not None and cookie_string is not None:
            raise ValueError("Provide either cookies dict or cookie_string, not both")
        if cookies is None and cookie_string is None:
            raise ValueError("Must provide either cookies dict or cookie_string")

        if cookies is not None:
            self.cookies = cookies.copy()
            if "sso-rw" not in self.cookies:
                self.cookies["sso-rw"] = self.cookies["sso"]
            self.cookie_string = "; ".join(f"{key}={value}" for key, value in self.cookies.items())
        elif cookie_string is not None:
            if len(cookie_string) < 100:
                raise ValueError("Cookie string is likely invalid as it's less than 100 characters long.")
            self.cookies = dict(cookie.split("=", 1) for cookie in cookie_string.split("; "))
            self.cookie_string = cookie_string

        required_cookies = {"sso"}
        if not all(cookie in self.cookies for cookie in required_cookies):
            raise ValueError("Missing required cookies (sso)")
        if len(self.cookies.get("sso", "")) < 50:
            raise ValueError("SSO cookie is likely invalid as it's less than 50 characters long.")

    def get_headers(self) -> dict:
        headers = COMMON_HEADERS.copy()
        headers["Cookie"] = self.cookie_string
        return headers

class GrokAPI:
    def __init__(self, auth: GrokAPIAuth):
        """
        Args:
            auth (GrokAPIAuth): Authentication instance with valid cookies.
        """
        self.auth = auth
        self.headers = auth.get_headers()
        self.conversation_id = None
        self.parent_response_id = None

    def _post(self, url, **kwargs):
        """
        Helper method to perform a POST request.
        Always passes impersonate="chrome".
        """
        return requests.post(url, impersonate="chrome", **kwargs)

    def create_conversation(self, prompt: str, enable_think=False):
        """
        Initiates a new conversation with Grok API using the provided prompt.

        Args:
            prompt (str): The initial message content to start the conversation.
            enable_think (bool, optional): Enables advanced reasoning mode when True. Defaults to False.

        Yields:
            str: Tokens from the streamed response.

        Side Effects:
            Updates internal conversation_id and parent_response_id.
        """
        url = "https://grok.com/rest/app-chat/conversations/new"
        payload = {
            "temporary": False,
            "modelName": "grok-3",
            "message": prompt,
            "fileAttachments": [],
            "imageAttachments": [],
            "disableSearch": False,
            "enableImageGeneration": True,
            "returnImageBytes": False,
            "returnRawGrokInXaiRequest": False,
            "enableImageStreaming": True,
            "imageGenerationCount": 2,
            "forceConcise": False,
            "toolOverrides": {},
            "enableSideBySide": True,
            "isPreset": False,
            "sendFinalMetadata": True,
            "customInstructions": "",
            "deepsearchPreset": "",
            "isReasoning": enable_think
        }

        res = self._post(url, headers=self.headers, json=payload, stream=True)
        try:
            res.raise_for_status()
            for line in res.iter_lines():
                if not line:
                    continue
                if isinstance(line, bytes):
                    line = line.decode("utf-8")
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                result = data.get("result", {})
                if "conversation" in result:
                    conv = result["conversation"]
                    self.conversation_id = conv.get("conversationId")
                if "response" in result:
                    resp = result["response"]
                    if "modelResponse" in resp:
                        self.parent_response_id = resp["modelResponse"].get("responseId")
                    if "token" in resp and "isThinking" in resp and not resp["isThinking"]:
                        yield resp["token"]
        finally:
            if hasattr(res, "close"):
                res.close()

    def send_followup(self, message: str, parent_response_id: str = None, enable_think=False):
        """
        Sends a follow-up message in an existing conversation with Grok API.

        Args:
            message (str): The follow-up message content.
            parent_response_id (str, optional): Parent response ID to reply to.
            enable_think (bool, optional): Enables advanced reasoning mode when True. Defaults to False.

        Yields:
            str: Tokens from the streamed response.

        Raises:
            ValueError: If conversation IDs are not initialized.
        """
        if not self.conversation_id or not self.parent_response_id:
            raise ValueError("Conversation and parent response IDs must be set. Call create_conversation first.")

        effective_parent = parent_response_id if parent_response_id is not None else self.parent_response_id
        url = f"https://grok.com/rest/app-chat/conversations/{self.conversation_id}/responses"
        payload = {
            "message": message,
            "modelName": "grok-3",
            "parentResponseId": effective_parent,
            "disableSearch": False,
            "enableImageGeneration": True,
            "imageAttachments": [],
            "returnImageBytes": False,
            "returnRawGrokInXaiRequest": False,
            "fileAttachments": [],
            "enableImageStreaming": True,
            "imageGenerationCount": 2,
            "forceConcise": False,
            "toolOverrides": {},
            "enableSideBySide": True,
            "sendFinalMetadata": True,
            "customInstructions": "",
            "deepsearchPreset": "",
            "isReasoning": enable_think
        }

        headers = self.headers.copy()
        headers["Referer"] = f"https://grok.com/chat/{self.conversation_id}"
        res = self._post(url, headers=headers, json=payload, stream=True)
        try:
            res.raise_for_status()
            for line in res.iter_lines():
                if not line:
                    continue
                if isinstance(line, bytes):
                    line = line.decode("utf-8")
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                res_data = data.get("result", {})
                if "modelResponse" in res_data:
                    self.parent_response_id = res_data["modelResponse"].get("responseId")
                if "token" in res_data and "isThinking" in res_data and not res_data["isThinking"]:
                    yield res_data["token"]
        finally:
            if hasattr(res, "close"):
                res.close()

    def _fetch_single_rate_limit(self, request_kind: str, model_name: str = "grok-3") -> dict:
        """
        Retrieves rate limit info for a specific request type from Grok API.

        Args:
            request_kind (str): Type of request ('DEFAULT', 'REASONING', 'DEEPSEARCH').
            model_name (str, optional): The Grok API model name. Defaults to "grok-3".

        Returns:
            dict: JSON response with rate limit details.
        """
        url = "https://grok.com/rest/rate-limits"
        base_headers = self.auth.get_headers()
        base_headers.update({"Referer": "https://grok.com/chat"})
        payload = {"requestKind": request_kind, "modelName": model_name}
        json_payload = json.dumps(payload)
        headers = base_headers.copy()
        headers["Content-Length"] = str(len(json_payload))
        response = self._post(url, headers=headers, data=json_payload)
        return response.json()

    def fetch_rate_limits(self) -> dict:
        """
        Retrieves rate limit data for DEFAULT, REASONING, and DEEPSEARCH requests.

        Returns:
            dict: Dictionary containing rate limits for each request type.
        """
        return {
            "DEFAULT": self._fetch_single_rate_limit("DEFAULT"),
            "REASONING": self._fetch_single_rate_limit("REASONING"),
            "DEEPSEARCH": self._fetch_single_rate_limit("DEEPSEARCH")
        }
