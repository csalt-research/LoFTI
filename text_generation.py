from utils import LLM_gen
import json
import argparse
from pathlib import Path
from datasets import load_dataset

def get_llm_output(
    sample: dict,
    model: str, 
    prompt_format: None
    ):
    claim_id = sample["id"]
    claim = sample["reference_text"]
    hyperlocality = sample["hyperlocal_score"]
    location = sample["target_location"]
    category = sample["category"]
    target_sent_prompt = "TARGET_SENT_GEN_PROMPT_WITH_LOCATION"
    target_sent, reason_for_target_sent = LLM_gen.run_target_claim_generation(
        claim=claim,
        location=location,
        prompt=target_sent_prompt,
        model=model,
        prompt_format=prompt_format,
    )
    output = {
        "claim_id": claim_id,
        "category:": category,
        "reference_claim": claim,
        "target_location": location,
        "hyperlocal_score": hyperlocality,
        "model": model,
        "target_claim_gen": target_sent,
        "reason_for_target_claim_gen": reason_for_target_sent
    }
    return output

def llm_generation(data, model, prompt_format, output_path):
    outputs = []
    for sample in data:
        print("Claim: ", sample["id"])
        outputs.append(get_llm_output(sample, model, prompt_format))
        break
    # Dump the list into the JSON file
    output_file = Path(output_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, 'w') as json_file:
        json.dump(outputs, json_file, indent=4, ensure_ascii=False)
    print(f"Outputs saved to {output_path}.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Evaluate an LLM using LoFTI benchmark.')
    parser.add_argument('--model', type=str, required=True, help='LLM model path (gguf format) or openai model names (like gpt-4-turbo)')
    parser.add_argument('--prompt_format', type=str, required=True, help="Prompt format for the model. Supported formats: 'llama', 'mixtral, 'gpt'.")
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the output texts')
    args = parser.parse_args()

    # Load from huggingface
    # data = load_dataset("sonasimon/LoFTI", split='test')
    # Or load the local file
    data = load_dataset('json', data_files={'test': 'dataset/LoFTI.jsonl'}, split='test')

    # get generation from an LLM
    llm_generation(data, args.model, args.prompt_format, args.output_path)
