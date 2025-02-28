from openai import OpenAI

from .config import settings


class AIML_API(OpenAI):
    """Construct a new synchronous aiml client instance.

    This automatically infers the following arguments from their corresponding environment variables if they are not provided:

    - api_key from ```AIML_API_KEY```
    - base_url from ```AIML_API_URL```"""

    def __init__(
        self, aiml_api_key: str | None = None, aiml_api_url: str | None = None
    ) -> None:
        """
        Initializes the AIML_API instance
        """

        if aiml_api_url is None:
            aiml_api_url = settings.aiml_api_url
        if aiml_api_url is None:
            aiml_api_url = "https://api.aimlapi.com/v1"
        if aiml_api_key is None:
            aiml_api_key = settings.aiml_api_key

        super().__init__(api_key=settings.aiml_api_key, base_url=settings.aiml_api_url)

        self.system_prompt = "You are a helpful assistant. Provide concise responses using from two sentences to 650 words maximum."
        self.user_prompt = "hi"
