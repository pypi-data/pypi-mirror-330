import os
import sys

mock_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_data"))
if mock_dir not in sys.path:
    sys.path.insert(0, mock_dir)
from mock_openai_patch import chat_completions_generate,chat_completions_stream ,chat_completions_toolcall, chat_completions_jsonschema

from unittest.mock import patch, MagicMock
from unittest.mock import ANY

from openai import OpenAI

from gai.lib.config import GaiClientConfig

from gai.openai.patch import patch_chatcompletions

"""
GPT models require OPENAI_API_KEY to be set in the environment.
"""
@patch("os.environ.get",return_value="")
def test_patch_chatcompletions_openai_create_failed_without_apikey(mock_os_environ_get):
    try:
        client = patch_chatcompletions(OpenAI())
        client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":"tell me a one sentence story"}])
    except Exception as e:
        assert str(e) == "Connection error."


"""
generate: OpenAI
"""
@patch("gai.lib.config.GaiClientConfig.from_name", new_callable=MagicMock)
@patch("gai.lib.config.GaiClientConfig.from_dict", new_callable=MagicMock)
def test_patch_chatcompletions_openai_generate(mock_from_dict,mock_from_name):
    from gai.openai.patch import patch_chatcompletions
    
    client = patch_chatcompletions(OpenAI())
    
    # Mock the original create function() with data generator
    
    client.chat.completions.original_openai_create = lambda **kwargs: chat_completions_generate("openai")
    
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":"tell me a one sentence story"}])
    
    # Reading config is not required for openai models
    
    mock_from_dict.assert_not_called()
    mock_from_name.assert_not_called()
    
    # openai_create() is called and extract() is injected correctly
    
    assert response.extract()["content"] == '"Despite being lost in the dense, mystifying forest for hours, the brave little puppy finally managed to find his way back home, surprising his family who welcomed him with more love than ever before."'
    
"""
generate: Ollama
"""
@patch("ollama.chat")
def test_patch_chatcompletions_ollama_generate(mock_ollama_chat):
    mock_ollama_chat.return_value = chat_completions_generate("ollama")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "ollama",
        "model": "llama3.1",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    response = client.chat.completions.create(model="llama3.1", messages=[{"role":"user","content":"tell me a one sentence story"}])
    
    gai_client_config = GaiClientConfig.from_dict(client_config)
    mock_ollama_chat.assert_called_once_with(model="llama3.1", messages=[{"role":"user","content":"tell me a one sentence story"}], options={'temperature': None, 'top_k': None, 'top_p': None, 'num_predict': None}, stream=False, tools=None)
    
"""
generate: Gai
"""
@patch("gai.ttt.client.TTTClient._generate_dict")
def test_patch_chatcompletions_gai_generate(mock_tttclient_call):
    mock_tttclient_call.return_value = chat_completions_generate("gai")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "gai",
        "url": "http://localhost:12031/gen/v1/chat/completions",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    response = client.chat.completions.create(model="gai", messages=[{"role":"user","content":"tell me a one sentence story"}])
    
    print(response)
    
    extracted=response.extract()
    assert extracted["content"] == "Under a tree, a little boy shared his last bread with a hungry crow. They became friends, teaching him that kindness can feed more than just Hunger."
    
    gai_client_config = GaiClientConfig.from_dict(client_config)
    mock_tttclient_call.assert_called_once_with(url='http://localhost:12031/gen/v1/chat/completions', messages=[{'role': 'user', 'content': 'tell me a one sentence story'}, {'role': 'assistant', 'content': ''}], stream=False, max_tokens=None, temperature=None, top_p=None, top_k=None, json_schema=None, tools=None, tool_choice=None, stop=None, timeout=None)
    

"""
stream: OpenAI
"""
@patch("gai.lib.config.GaiClientConfig.from_name", new_callable=MagicMock)
@patch("gai.lib.config.GaiClientConfig.from_dict", new_callable=MagicMock)
def test_patch_chatcompletions_openai_stream(mock_from_dict,mock_from_name):
    from gai.openai.patch import patch_chatcompletions
    
    client = patch_chatcompletions(OpenAI())
    
    # Mock the original create function() with data generator
    
    client.chat.completions.original_openai_create = lambda **kwargs: chat_completions_stream("openai")
    
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":"tell me a one sentence story"}], stream=True)

    content = ""
    for chunk in response:
        extracted=chunk.extract()
        if extracted and type(extracted)==str:
            content+=extracted
    
    assert content=='"Once upon a time, a tiny, curious frog set on a journey to reach the top of the mountain, and against all odds, found a kingdom of thriving frogs living beautifully above the clouds."'

"""
stream: Ollama
"""
@patch("ollama.chat")
def test_patch_chatcompletions_ollama_stream(mock_ollama_chat):
    mock_ollama_chat.return_value = chat_completions_stream("ollama")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "ollama",
        "model": "llama3.1",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    response = client.chat.completions.create(model="llama3.1", messages=[{"role":"user","content":"tell me a one sentence story"}], stream=True)

    content = ""
    for chunk in response:
        if hasattr(chunk,"extract"):
            extracted=chunk.extract()
            if extracted and type(extracted)==str:
                content+=extracted
    print(content)
    assert content=="As she lay in bed, Emily couldn't shake the feeling that someone had been watching her from the shadows of her childhood home."

"""
stream: Gai
"""
@patch("gai.ttt.client.TTTClient._stream_dict")
def test_patch_chatcompletions_gai_stream(mock_tttclient_stream):
    mock_tttclient_stream.return_value = chat_completions_stream("gai")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "gai",
        "url": "http://localhost:12031/gen/v1/chat/completions",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)
    response = client.chat.completions.create(model="gai", messages=[{"role":"user","content":"tell me a one sentence story"}], stream=True)

    content = ""
    for chunk in response:
        if hasattr(chunk,"extract"):
            extracted=chunk.extract()
            if extracted and type(extracted)==str:
                content+=extracted
    assert content=="An angry old drunk walks through the streets yelling at cars and throwing bottles."

"""
toolcall: OpenAI
"""
@patch("gai.lib.config.GaiClientConfig.from_name", new_callable=MagicMock)
@patch("gai.lib.config.GaiClientConfig.from_dict", new_callable=MagicMock)
def test_patch_chatcompletions_openai_toolcall(mock_from_dict,mock_from_name):
    from gai.openai.patch import patch_chatcompletions
    
    client = patch_chatcompletions(OpenAI())
    
    # Mock the original create function() with data generator
    
    client.chat.completions.original_openai_create = lambda **kwargs: chat_completions_toolcall("openai")
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[{"role": "user", "content": "What is the current time in Singapore?"}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "google",
                    "description": "The 'google' function is a powerful tool that allows the AI to gather external information from the internet using Google search. It can be invoked when the AI needs to answer a question or provide information that requires up-to-date, comprehensive, and diverse sources which are not inherently known by the AI. For instance, it can be used to find current date, current news, weather updates, latest sports scores, trending topics, specific facts, or even the current date and time. The usage of this tool should be considered when the user's query implies or explicitly requests recent or wide-ranging data, or when the AI's inherent knowledge base may not have the required or most current information. The 'search_query' parameter should be a concise and accurate representation of the information needed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "The search query to search google with. For example, to find the current date or time, use 'current date' or 'current time' respectively."
                            }
                        },
                        "required": ["search_query"]
                    }
                }
            }
        ],
        tool_choice="required",
    )
    #print(response.choices[0].tool_calls[0].function)
    print(response.choices[0].message.tool_calls[0].function)
    
    assert response.choices[0].message.tool_calls[0].function.name == "google"
    assert response.choices[0].message.tool_calls[0].function.arguments == '{"search_query":"current time in Singapore"}'

"""
toolcall: Ollama
"""
@patch("ollama.chat")
def test_patch_chatcompletions_ollama_toolcall(mock_ollama_chat):
    mock_ollama_chat.return_value = chat_completions_toolcall("ollama")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "ollama",
        "model": "llama3.1",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)

    response = client.chat.completions.create(
        model="llama3.1", 
        messages=[{"role": "user", "content": "What is the current time in Singapore?"}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "google",
                    "description": "The 'google' function is a powerful tool that allows the AI to gather external information from the internet using Google search. It can be invoked when the AI needs to answer a question or provide information that requires up-to-date, comprehensive, and diverse sources which are not inherently known by the AI. For instance, it can be used to find current date, current news, weather updates, latest sports scores, trending topics, specific facts, or even the current date and time. The usage of this tool should be considered when the user's query implies or explicitly requests recent or wide-ranging data, or when the AI's inherent knowledge base may not have the required or most current information. The 'search_query' parameter should be a concise and accurate representation of the information needed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "The search query to search google with. For example, to find the current date or time, use 'current date' or 'current time' respectively."
                            }
                        },
                        "required": ["search_query"]
                    }
                }
            }
        ],
        tool_choice="required",
        stream=False
    )
    
    assert response.choices[0].message.tool_calls[0].function.name == "google"
    assert response.choices[0].message.tool_calls[0].function.arguments == '{"search_query": "current time in Singapore"}'

"""
toolcall: Gai
"""
@patch("gai.ttt.client.TTTClient._generate_dict")
def test_patch_chatcompletions_gai_toolcall(mock_tttclient):
    mock_tttclient.return_value = chat_completions_toolcall("gai")
    
    from gai.openai.patch import patch_chatcompletions
    client_config = {
        "client_type": "gai",
        "url": "http://localhost:12031/gen/v1/chat/completions",
    }
    client = patch_chatcompletions(OpenAI(), client_config=client_config)

    response = client.chat.completions.create(
        model="gai",
        messages=[{"role": "user", "content": "What is the current time in Singapore?"}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "google",
                    "description": "The 'google' function is a powerful tool that allows the AI to gather external information from the internet using Google search. It can be invoked when the AI needs to answer a question or provide information that requires up-to-date, comprehensive, and diverse sources which are not inherently known by the AI. For instance, it can be used to find current date, current news, weather updates, latest sports scores, trending topics, specific facts, or even the current date and time. The usage of this tool should be considered when the user's query implies or explicitly requests recent or wide-ranging data, or when the AI's inherent knowledge base may not have the required or most current information. The 'search_query' parameter should be a concise and accurate representation of the information needed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "The search query to search google with. For example, to find the current date or time, use 'current date' or 'current time' respectively."
                            }
                        },
                        "required": ["search_query"]
                    }
                }
            }
        ],
        tool_choice="required",
        stream=False
    )
    
    assert response.choices[0].message.tool_calls[0].function.name == "google"
    assert response.choices[0].message.tool_calls[0].function.arguments == '{"search_query": "current time in Singapore"}'
