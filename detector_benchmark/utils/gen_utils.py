from dataclasses import dataclass
import json
import os

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForMaskedLM, AutoModelForCausalLM


        
def transform_chat_template_with_prompt(prefix: str, prompt: str, tokenizer: AutoTokenizer,
                                        use_chat_template: bool = False, template_type: str = None,
                                        system_prompt: str = "", forced_prefix: str = "") -> str:
    
    """
    Transform a prefix with a prompt into a chat template
    
    Parameters:
    prefix : str
        The prefix to use
    prompt : str
        The prompt to use
    tokenizer : AutoTokenizer
        The tokenizer to use
    use_chat_template : bool, optional
        Whether to use a chat template, by default False
    template_type : str, optional
        The type of template to use, by default None
    system_prompt : str, optional
        The system prompt to use, by default ""
        
    Returns:
    str
        The transformed prefix
    """
        

    if prefix != "":
        text_instruction = f"{prompt} {prefix}"
    else:
        text_instruction = prompt
        
    if use_chat_template:
        if system_prompt == "":
            sys_prompt = "You are a helpful assistant."
        else:
            sys_prompt = system_prompt
        match template_type:
            case "system_user":
                messages = [
                {"role": "system", "content": f"{sys_prompt}"},
                {"role": "user", "content": f"{text_instruction}"},
                ]
            case "user":
                messages = [
                {"role": "user", "content": f"{text_instruction}"},
                ]
            case _:
                raise ValueError("Template type not supported")

        text_template = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # force prefix on the generated response
        #text_template = f"{text_template}\n{forced_prefix}"
        text_template = f"{text_template} {forced_prefix}"

    else:
        text_template = text_instruction

    return text_template
