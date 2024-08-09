# LoFTI: Localization and Factuality Transfer to Indian Locales

This repo contains the dataset and codes for [LoFTI: Localization and Factuality Transfer to Indian Locales](https://arxiv.org/pdf/2407.11833).

## Overview
LoFTI is an evaluation benchmark spanning multiple geographical locales that can be used to test the localization and factual transfer abilities of LLMs.

It can be used as a benchmark to evaluate the capabilities of LLMs in the Indian context. 
- Generating a localized response given a common question that can be asked across locations
- Factuality transfer from one locale to another.
<p align="center">
  <img src="https://raw.githubusercontent.com/csalt-research/LoFTI/main/LoFTI_Illustration.png" width="500" alt>
  <p align="center">
  <em> Illustration of LLM’s localized factual text transfer capabilities.</em>
  </p>
</p>

LoFTI dataset is available in [Hugging Face](https://huggingface.co/datasets/sonasimon/LoFTI).

```python
from datasets import load_dataset

# Load the dataset from Hugging Face
dataset = load_dataset('sonasimon/LoFTI')

# Access the data
print(dataset['test'][0])
```

## Dataset Structure
- Region: The region of the reference location.
- Category: The category of the entity in the factual text.
- Reference Location: A non-Indian location.
- Reference Entity: An entity from the reference location.
- Reference Text: Factual text about the reference entity.
- Target Location: A location in India.
- True Target Entity: An example of a correct localization of the reference entity in the target location.
- True Target Text: A localized factual text of the true target entity.
- Hyperlocal Score: The degree of hyperlocality within the Indian context. The dataset includes three hyperlocality scores: 1, 2, and 3. These scores correspond to the target locations ‘India,’ ‘any state in India,’ and ‘any city in India,’ respectively.
- High Cardinality: Cardinality denotes the potential count of replaceable entities for the reference entity within the target location. A high cardinality suggests there are many such replaceable entities. This feature is denoted by ’yes’ or ’no’ values.
- Common Questions: Questions extracted from the reference and the target texts.

## Dataset Distribution
<p align="center">
  <img src="https://raw.githubusercontent.com/csalt-research/LoFTI/main/map.png">
  <p align="center">
    <em>The global distribution of the reference entities and the spread of target entities in India.</em>
  </p>
</p>

## Dataset Creation

### Dataset Source
- Entity pairs: Humman annotators
- Reference text: Google API Client/Wikipedia
- Target text: [TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF(Q4_K_M)](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/blob/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf)
- Common questions: [TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF(Q4_K_M)](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/blob/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf)

### Dataset Creation Pipeline
![Dataset creation pipeline](https://raw.githubusercontent.com/csalt-research/LoFTI/main/pipeline.png)

### Annotations
To ensure the correctness of the LOFTI dataset, all the generations were carefully checked by human annotators. These annotators represent diverse demographics and have knowledge about samples from different geographic and hyperlocal regions.

## Reproducibility
### Environment
```
git clone https://github.com/csalt-research/LoFTI.git
cd LoFTI
pip install -r requirement.txt
```
### Localized Text Transfer
To do localized text transfer from a reference sentence to a target location on LoFTI dataset:
```
python3 localized_text_transfer.py \
  --model model \
  --prompt_format prompt_format \
  --output_path output_path
```
`model`: LLM model path (gguf format) or openai model names (like gpt-4-turbo).

`prompt_format`: Prompt format for the model. Supported formats: 'llama', 'mixtral, 'gpt'.

`output_path`: Output file path to a JSON file to store the generations.

Example:
```
python3 localized_text_transfer.py \
  --model gpt-3.5-turbo \
  --prompt_format gpt \
  --output_path outputs/TT_gpt3.5_generation.json
```

### Localized Question Answering
To do localized question answering for a given factual question and a target location on LoFTI dataset:
```
python3 localized_QA.py \
  --model model \
  --prompt_format prompt_format \
  --output_path output_path
```
`model`: LLM model path (gguf format) or openai model names (like gpt-4-turbo).

`prompt_format`: Prompt format for the model. Supported formats: 'llama', 'mixtral, 'gpt'.

`output_path`: Output file path to a JSON file to store the generations.

Example:
```
python3 localized_text_transfer.py \
  --model gpt-3.5-turbo \
  --prompt_format gpt \
  --output_path outputs/QA_gpt3.5_generation.json
```

### LLM as a LoFTI Evaluator
To evaluate the generations obtained for LoFTI using an LLMdo localized question answering for a given factual question and a target location on LoFTI dataset:
```
python3 llm_evaluator.py \
  --model model \
  --eval_type eval_type \
  --eval_json_file eval_json_file \
  --eval_metric ['eval_metric1', 'eval_metric2'] \
  --output_path output_path
```

`model`: Openai model names (like gpt-4-turbo).

`eval_type`: Provide QA for localized question answering, TT for localized text transfer.

`eval_json_file`: File to evaluate (JSON).

`eval_metric`: List of metrics to evaluate. Metrics supported EC, CQ, and FC.

`output_path`: Output file path to a JSON file to store the evaluations.

Example:
```
python3 llm_evaluator.py \
  --model gpt-4-turbo \
  --eval_type TT \
  --eval_json_file outputs/TT_gpt3.5_generation.json \
  --eval_metric ['EC', 'CQ', 'FC'] \
  --output_path outputs/TT_gpt3.5_gen_eval_gpt4_EC_CQ_FC.json
```

## Limitations
- The dataset is designed for localization from different locations in the world to India only. In order to perform localization to regions other than in India, we will need additional annotations. This is also reserved for a future release.
- LoFTI is entirely in English and does not contain any multilingual localizations. It is possible to use simple translation models to translate the data but it is not robust. This is a significant extension that we also intend to explore as future work.
- There can be several correct target entities localized to a target location which we refer to as high cardinality. High cardinality can make it hard to make the resulting evaluations precise, especially since some entities can be added in the future with respect to localization.

## Citation 

Please cite the following paper when using this dataset.

```
@misc{simon2024loftilocalizationfactualitytransfer,
      title={LoFTI: Localization and Factuality Transfer to Indian Locales}, 
      author={Sona Elza Simon and Soumen Kumar Mondal and Abhishek Singhania and Sayambhu Sen and Preethi Jyothi},
      year={2024},
      eprint={2407.11833},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.11833}, 
}
```

