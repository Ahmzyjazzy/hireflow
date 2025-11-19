from dataclasses import dataclass

@dataclass
class Config:
    """Configuration settings for the Hireflow application.
    Attributes:
        MODEL_NAME (str): The name of the language model to be used.
    
    """
    
    model_name: str = "gemini-2.0-flash-001"

config = Config()