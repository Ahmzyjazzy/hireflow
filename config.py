from dataclasses import dataclass
from google.genai import types

@dataclass
class Config:
    """Configuration settings for the Hireflow application.
    Attributes:
        MODEL_NAME (str): The name of the language model to be used.
    
    """

    app_name: str = "hireflow_app"
    
    model_name: str = "gemini-2.0-flash-001"

    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

config = Config()