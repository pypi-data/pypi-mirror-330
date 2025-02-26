import re
from typing import List

# This is used to compress a list into a smaller string to be passed as a single USER message to the prompt template.
def chat_list_to_string(messages):
    if type(messages) is str:
        return messages
    prompt=""        
    for message in messages:
        if prompt:
            prompt+="\n"
        content = message['content'].strip()
        role = message['role'].strip()
        if content:
            prompt += f"{role}: {content}"
        else:
            prompt += f"{role}:"
    return prompt

# This is useful for converting text dialog to chatgpt-style dialog
def chat_string_to_list(messages):
    # Split the messages into lines
    lines = messages.split('\n')

    # Prepare the result list
    result = []

    # Define roles
    roles = ['system', 'user', 'assistant']

    # Initialize current role and content
    current_role = None
    current_content = ''

    # Process each line
    for line in lines:
        # Check if the line starts with a role
        for role in roles:
            if line.lower().startswith(role + ':'):
                # If there is any content for the current role, add it to the result
                if current_role is not None and current_content.strip() != '':
                    result.append({'role': current_role, 'content': current_content.strip()})
                
                # Start a new role and content
                current_role = role
                current_content = line[len(role) + 1:].strip()
                break
        else:
            # If the line does not start with a role, add it to the current content
            current_content += ' ' + line.strip()

    # Add the last role and content to the result
    if current_role is not None:
        result.append({'role': current_role, 'content': current_content.strip()})

    return result

def chat_list_to_INST(input_list):
    # Initialize an empty string for the output
    output = "<s>\n\t[INST]\n"
    
    # if last message is an AI placeholder, remove it
    last_role = input_list[-1]["role"].lower()
    last_content = input_list[-1]["content"]
    if last_role != "system" and last_role != "user" and last_content == "":
        input_list.pop()

    # Loop through the list of dictionaries
    for item in input_list:
        # Check the role
        role = item["role"].lower()
        if role == "system":
            # Add the system message
            output += f"\t\t<<SYS>>\n\t\t\t{item['content']}\n\t\t<</SYS>>\n"
        elif role == "user":
            # Add the user message
            output += f"\t\t{item['content']}\n"
            output += "\t[/INST]\n\n\t"
        else:
            # Add the AI message
            output += f"{item['content']}\n\n"
            # AI message marks the end of 1 turn
            output += "</s>\n"
            # Add the beginning of next turn
            output += "<s>\n\t[INST]\n"
   
    return output

def INST_output_to_output(output_string):
    # The rfind method returns the last index where the substring is found
    last_index = output_string.rfind('[/INST]\n\n\t')

    # Add the length of '[/INST]\n\n\t' to get the start of the desired substring
    start_of_substring = last_index + len('[/INST]\n\n\t')

    # Extract the substring from start_of_substring till the end of the string
    result = output_string[start_of_substring:]

    return result

def ASSISTANT_output_to_output(output_string):
    return re.split('\n.+:',output_string)[-1].strip()

