# AI/ML API Python library

The AI/ML Python library provides convenient access to the AI/ML API. \
(Currently, only chat completion and embeddings are supported. If you'd like to help improve this library, feel free to join our [Discord](https://discord.gg/hvaUsJpVJf))

## Documentation

Getting started with the AI/ML API is simple. Follow these steps to set up your integration:

### 1. Get Your API Key  
To begin, you need an API key. You can obtain yours here:  
🔑 [Get Your API Key](https://aimlapi.com/app/keys/?utm_source=pipy&utm_medium=pipy&utm_campaign=integration)

### 2. Explore Available Models  
Looking for a different model? Browse the full list of supported models:  
📚 [Full List of Models](https://aimlapi.com/models?utm_source=pipy&utm_medium=pipy&utm_campaign=integration)

### 3. Read the Documentation  
For detailed setup instructions and usage guidelines, refer to the official documentation. If you’d like to get started quickly, check out our examples below.

And don’t forget the first step—you’ll need an API key! ^^ \
📖 [AI/ML API Docs](https://docs.aimlapi.com?utm_source=pipy&utm_medium=pipy&utm_campaign=integration)

### 4. Need Help?  
If you have any questions, feel free to reach out. We’re happy to assist! 🚀  [Discord](https://discord.gg/hvaUsJpVJf)


## Installation
#### After obtaining your API key, create an .env file and copy the required contents into it.
```sh
touch .env
```
Then, copy the code below, paste it into your .env file, and set your API key to AIML_API_KEY="".
```python
AIML_API_KEY = ""
AIML_API_URL = "https://api.aimlapi.com/v1"
```
#### Install aiml_api package 
```sh
# install from PyPI
pip install aiml_api
```

### Usage  
```python
from aiml_api import AIML_API

api = AIML_API()

completion = api.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {"role": "user", "content": "Explain the importance of low-latency LLMs"},
    ],
    temperature=0.7,
    max_tokens=256,
)

response = completion.choices[0].message.content
print("AI:", response)
```  

### Running the Script  
To execute the script, use:  
```sh
python3 <your_script_name>.py
```