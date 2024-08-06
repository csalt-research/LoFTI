"""Utils for running target sentence generation."""

from llama_cpp import Llama
from prompts import llm_prompts
from utils import api, openai_gen
import openai

def parse_llm_response(response: str):
    """Extract target sentence from the LLM response.
    Args:
        response: Target sentence generation response from LLM.
    Returns:
        Target sentence and reason
    """
    Sent_search_string = "Target sentence:"
    Reason_search_string = "Reason:"
    sentence = ""
    reason = ""
    for response in response.split("\n"):
        if Sent_search_string in response:
            sentence = response.split(Sent_search_string)[1].strip()
        elif Reason_search_string in response:
            reason = response.split(Reason_search_string)[1].strip()
    return sentence, reason

def run_target_claim_generation(
    claim: str,
    location: str,
    prompt: str,
    model: str,
    prompt_format: str,
    ):
    """Generates target sentence based on target location and reference claim.
    Args:
        claim: Reference claim
        location: Target location
        prompt: Prompt name
        model: LLM model
        prompt_format: Prompt format for the model
    Returns:
        target sentence and reason
    """

    if(model in openai.Model.list()['data']): # for all openai model
        prompt_ = getattr(llm_prompts, prompt)
        llm_input = prompt_.format(claim=claim, location=location)
        response = openai_gen.openai_model(llm_input, model, api.OPENAI_KEY)
    else:
        model = Llama(
            model_path=model,  
            n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
            n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
            n_gpu_layers=35 ,        # The number of layers to offload to GPU, if you have GPU acceleration available
            verbose=False
            ) 
        if(prompt_format == 'llama'):
            prompt = getattr(llm_prompts, prompt+"_llama")
            llm_input = prompt.format(location=location, claim=claim).strip()
            output = model(llm_input, max_tokens=256)
            response = output['choices'][0]['text']
        elif(prompt_format == 'mixtral'):
            prompt = getattr(llm_prompts, prompt+"_mixtral")
            llm_input = prompt.format(location=location, claim=claim).strip()
            output = model(llm_input, max_tokens=256)
            response = output['choices'][0]['text']
        else:
            print("Model not found! Invalid model name.")
            exit()
   
    target_sent, reason = parse_llm_response(response.strip())
    return target_sent, reason