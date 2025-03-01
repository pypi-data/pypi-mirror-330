import os
import json
import sys

mock_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_data"))
if mock_dir not in sys.path:
    sys.path.insert(0, mock_dir)
from mock_openai_patch import chat_completions_jsonschema

from unittest.mock import patch, MagicMock
from unittest.mock import ANY

from openai import OpenAI

"""
structured output: OpenAI
"""
@patch("gai.lib.config.GaiClientConfig.from_name", new_callable=MagicMock)
@patch("gai.lib.config.GaiClientConfig.from_dict", new_callable=MagicMock)
def test_patch_chatcompletions_openai_create(mock_from_dict,mock_from_name):
    from gai.openai.patch import patch_chatcompletions
    
    client = patch_chatcompletions(OpenAI())
    
    # Mock the original create function() with data generator
    
    client.beta.chat.completions.original_openai_parse = lambda **kwargs: chat_completions_jsonschema("openai")
    
    from pydantic import BaseModel
    class Book(BaseModel):
        title: str
        summary: str
        author: str
        published_year: int
    data = """Foundation is a science fiction novel by American writer
            Isaac Asimov. It is the first published in his Foundation Trilogy (later
            expanded into the Foundation series). Foundation is a cycle of five
            interrelated short stories, first published as a single book by Gnome Press
            in 1951. Collectively they tell the early story of the Foundation,
            an institute founded by psychohistorian Hari Seldon to preserve the best
            of galactic civilization after the collapse of the Galactic Empire."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o", 
        response_format=Book,
        messages=[{"role":"user","content":data}]
        )
    
    # Reading config is not required for openai models
    
    mock_from_dict.assert_not_called()
    mock_from_name.assert_not_called()
    
    jsoned = json.loads(response.choices[0].message.content)
    assert jsoned["title"] == "Foundation"
    assert jsoned["author"] == "Isaac Asimov"
    assert jsoned["published_year"] == 1951
    
"""
structured output: Ollama
"""
@patch("ollama.chat")
def test_patch_chatcompletions_ollama_parse(mock_ollama_chat):
    mock_ollama_chat.return_value = chat_completions_jsonschema("ollama")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "ollama",
        "model": "llama3.1",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    
    from pydantic import BaseModel
    class Book(BaseModel):
        title: str
        summary: str
        author: str
        published_year: int
    data = """Foundation is a science fiction novel by American writer
            Isaac Asimov. It is the first published in his Foundation Trilogy (later
            expanded into the Foundation series). Foundation is a cycle of five
            interrelated short stories, first published as a single book by Gnome Press
            in 1951. Collectively they tell the early story of the Foundation,
            an institute founded by psychohistorian Hari Seldon to preserve the best
            of galactic civilization after the collapse of the Galactic Empire."""
    response = client.beta.chat.completions.parse(
        model="llama3.1", 
        response_format=Book,
        messages=[{"role":"user","content":data}]
        )
    
    jsoned = json.loads(response.choices[0].message.content)
    assert jsoned["title"] == "Foundation"
    assert jsoned["author"] == "Isaac Asimov"
    assert jsoned["published_year"] == 1951
    
"""
structured output: Gai
"""
@patch("gai.ttt.client.TTTClient._generate_dict")
def test_patch_chatcompletions_gai_parse(mock_ollama_chat):
    mock_ollama_chat.return_value = chat_completions_jsonschema("gai")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "gai",
        "url": "http://localhost:12031/gen/v1/chat/completions",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    
    from pydantic import BaseModel
    class Book(BaseModel):
        title: str
        summary: str
        author: str
        published_year: int
    data = """Foundation is a science fiction novel by American writer
            Isaac Asimov. It is the first published in his Foundation Trilogy (later
            expanded into the Foundation series). Foundation is a cycle of five
            interrelated short stories, first published as a single book by Gnome Press
            in 1951. Collectively they tell the early story of the Foundation,
            an institute founded by psychohistorian Hari Seldon to preserve the best
            of galactic civilization after the collapse of the Galactic Empire."""
    response = client.beta.chat.completions.parse(
        response_format=Book,
        messages=[{"role":"user","content":data}]
        )
    
    jsoned = json.loads(response.choices[0].message.content)
    assert jsoned["title"] == "Foundation"
    assert jsoned["author"] == "Isaac Asimov"
    assert jsoned["published_year"] == 1951
