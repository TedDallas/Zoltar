import os
import openai
import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox
import tiktoken

# Set up Open AI
api_key = ""
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key == "" or api_key == None:
        raise Exception("You must create a system environment variable named OPENAI_API_KEY, and paste in your OpenAI API key as the value.")
    openai.api_key = api_key
except Exception as e1:
    messagebox.showerror("OpenAI API Key Failure", str(e1))
    exit()

max_tokens = {'gpt-4':8192, 'gpt-4-32k':32768, 'gpt-3.5-turbo':4096, 'gpt-3.5-turbo-16k':16384}

def text_box_text(text_box)->str:
    if text_box != None:
        return text_box.get("1.0", tk.END)
    else:
        return ""

def count_tokens(prompt:str)->int:
    # encoding = tiktoken.get_encoding("cl100k_base")
    # cl100k_base 	        gpt-4, gpt-3.5-turbo, text-embedding-ada-002
    # p50k_base 	        Codex models, text-davinci-002, text-davinci-003
    # r50k_base (or gpt2) 	GPT-3 models like davinci
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(prompt))

# code from OpenAI documentation - maybe slightly modified
def count_chat_tokens(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        #print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        #print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_chat_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        #print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_chat_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-3.5-turbo-16k":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def submit_prompt(Prompt:str, Temperature=0.3, Model="gpt-4")->str:
    response = None
    response_text = ""
    Messages=[{"role": "user", "content": Prompt}]
    MAX_TOKENS = max_tokens[Model] - count_tokens(Prompt) - 8
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',#Model,
            max_tokens = MAX_TOKENS,
            temperature=Temperature,
            messages = Messages)
        response_text = str.strip(response.choices[0].message.content)
    except Exception as e:
        messagebox.showerror("submit_prompt() error in Local_Lib", str(e))
    return response_text

def fix_spelling(prompt:str)->str:
    fix_mah_spellings = 'Correct the spelling in the following text: '+prompt.strip()
    return submit_prompt(Prompt=fix_mah_spellings, Temperature=0.1, Model="gpt-3.5-turbo")

def fix_grammar_spelling(prompt:str)->str:
    fix_mah_spellings = 'Correct for grammar and spelling in the following text: '+prompt.strip()
    return submit_prompt(Prompt=fix_mah_spellings, Temperature=0.1, Model="gpt-3.5-turbo")