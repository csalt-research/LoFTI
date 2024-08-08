import json
import argparse
from pathlib import Path
from datasets import load_dataset
from utils import api, openai_gen
from prompts import evaluation_prompts


# ec correctness         
def evaluate_target_claim_by_entity(ref_entity, ref_loc, ref_claim, tar_claim, location, true_tar_entity, category, model):
    entity = ""
    score = 0
    reason = ""
    prompt = evaluation_prompts.DETECT_ENTITY_PROMPT
    prompt = prompt.format(
        ref_entity=ref_entity,
        ref_loc = ref_loc,
        ref_sent = ref_claim,
        tar_sent = tar_claim,
        tar_loc = location,
        category = category)
    for i in range(0,3):
        response = openai_gen.openai_model(prompt, model, api.OPENAI_KEY)
        entity_search_string = "Target entity detected from the target sentence:"
        for resp in response.split("\n"):
            if entity_search_string in resp:
                entity = resp.split(entity_search_string)[1].strip()
        if(entity != ""):
            break
    if(entity != ""):
        prompt = evaluation_prompts.EVAL_THE_ENTITY_PROMPT
        prompt = prompt.format(
            tar_loc = location,
            poss_tar_entity = true_tar_entity,
            target_entity = entity,
            category = category)
        response = openai_gen.openai_model(prompt, model, api.OPENAI_KEY)
        score_search_string = "Score:"
        reason_search_string = "Reason:"
        for resp in response.split("\n"):
            if score_search_string in resp:
                score_ = resp.split(score_search_string)[1].strip()
                if(score_ == '2'):
                    score = 2
                elif(score_ == '1'):
                    score = 1
            elif reason_search_string in resp:
                reason = resp.split(reason_search_string)[1].strip()
    return score, reason, entity

# fc correctness
def evaluate_target_claim_by_fact(tar_claim, location, true_tar_entity, true_tar_claim, flag, entity_detected, model):
    if(flag == 2):
        prompt = evaluation_prompts.EVAL_BY_TRUE_TARGET_CLAIM_PROMPT
        prompt = prompt.format(
            tar_sent = tar_claim,
            poss_tar_claim = true_tar_claim)
    else: #flag == 1
        prompt = evaluation_prompts.EVAL_BY_TRUE_EXAMPLE_PROMPT
        prompt = prompt.format(
            tar_sent = tar_claim,
            tar_loc = location,
            poss_tar_entity = true_tar_entity,
            poss_tar_claim = true_tar_claim,
            entity_detected = entity_detected)

    response = openai_gen.openai_model(prompt, model, api.OPENAI_KEY)
    score_search_string = "Score:"
    reason_search_string = "Reason:"
    score = 0
    for resp in response.split("\n"):
        if score_search_string in resp:
            score_ = resp.split(score_search_string)[1].strip()
            if(score_ == '1'):
                score = 1
        elif reason_search_string in resp:
            reason = resp.split(reason_search_string)[1].strip()
    return score, reason

# cq correctness
def evaluate_target_claim_by_common_ques(claim, location, question, model):
    prompt = evaluation_prompts.EVAL_BY_GENERIC_QUES_PROMPT
    prompt = prompt.format(target_location=location,
                           target_claim=claim,
                           common_ques=question)
    response = openai_gen.openai_model(prompt, model, api.OPENAI_KEY)
    score_search_string = "Score:"
    reason_search_string = "Reason:"
    score = 0
    reason = ""
    for resp in response.split("\n"):
        if score_search_string in resp:
            score_ = resp.split(score_search_string)[1].strip()
            if(score_ == '1'):
                score = 1
        if reason_search_string in resp:
            reason = resp.split(reason_search_string)[1].strip()
    return score, reason

def evaluate_factual_correctness(ec_score, entity, tar_claim, tar_location, true_tar_entity, true_tar_claim, model):
    score = 0
    reason = ""
    if(ec_score != 0):
        for _ in range(3):  # try 3 times
            try:
                score, reason = evaluate_target_claim_by_fact(
                    tar_claim,
                    tar_location,
                    true_tar_entity,
                    true_tar_claim,
                    ec_score,
                    entity
                    )
                break # as soon as it works, break out of the loop
            except Exception as e:
                print(e)
                continue 
    return score, reason

def evaluate_entity_correctness(ref_entity, ref_loc, ref_claim, tar_claim, tar_location, true_tar_entity, category, model):
    score = 0
    reason = ""
    entity = ""
    for _ in range(3):  # try 3 times
        try:
            score, reason, entity = evaluate_target_claim_by_entity(
                ref_entity,
                ref_loc,
                ref_claim,
                tar_claim,
                tar_location,
                true_tar_entity,
                category
                )
            break # as soon as it works, break out of the loop
        except Exception as e:
            print(e)
            continue 
    return score, reason, entity

def evaluate_common_ques_correctness(ec_score, tar_claim, tar_location, common_questions, eval_type, model):
    score_list = []
    reason_list = []
    for ques_n in common_questions.keys():
        score = 0
        reason = "EC = 0"
        if(ec_score != 0):
            for _ in range(3):  # try 3 times
                try:
                    score, reason = evaluate_target_claim_by_common_ques(tar_claim, tar_location, common_questions[ques_n])
                    break # as soon as it works, break out of the loop
                except Exception as e:
                    print(e)
                    continue  
        score_list.append(score)
        reason_list.append(reason)
    return score_list, reason_list

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Use OpenAI models to evaluate the outputs of localized QA or localized text transfer.')
    parser.add_argument('--model', type=str, required=True, help='Openai model names (like gpt-4-turbo).')
    parser.add_argument('--eval_type', type=str, required=True, help='Provide QA for localized QA, TT for localized text transfer.')
    parser.add_argument('--eval_json_file', type=str, required=True, help='File to evaluate (JSON).')
    parser.add_argument('--eval_metric', type=list, required=True, help='List of metrics to evaluate. Metrics supported EC, CQ, FC.')
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the evaluations.')
    args = parser.parse_args()

    # Load from huggingface
    # data = load_dataset("sonasimon/LoFTI", split='test')
    # Or load the local file
    lofti_data = load_dataset('json', data_files={'test': 'dataset/LoFTI.jsonl'}, split='test')

    # Load the data to evaluate
    with open(args.eval_json_file, 'r') as json_file:
        data = json.load(json_file)

    output_list = {}
    ec_score_list = []
    cq_score_list = []
    fc_score_list = []

    if('EC' or 'FC' or 'CQ' in args.eval_metric):
        model = args.model
        for item in data:
            id = item["claim_id"]
            print(f"Evaluating claim {id} ...")
            result = lofti_data[str(id)].copy()
            # Entity Correctness
            e_score, e_reason, entity = evaluate_entity_correctness(
                    result["reference_entity"],
                    result["reference_location"],
                    result["reference_claim"],
                    item["target_claim_gen"],
                    result["target_location"],
                    result["true_target_entity"],
                    result["category"],
                    model
                    )
            result["claim_to_evaluate"] = item["target_claim_gen"]
            result["entity_detected"] = entity
            if(e_score == 2):
                result["EC "+ args.model+" score"] = 1
                result["EC "+ args.model+" score reason"] = "Exact match. " + e_reason
            else:
                result["EC "+ args.model+" score"] = e_score
                result["EC "+ args.model+" score reason"] = e_reason
            ec_score_list.append(result["EC "+ args.model+" score"])

            # Common Question Correctness
            if('CQ' in args.eval_metric):
                c_score, c_reason = evaluate_common_ques_correctness(
                    e_score,
                    item["target_claim_gen"],
                    result["target_location"],
                    result["common_questions"],
                    args.eval_type,
                    model
                )
                result["CQ "+ args.model+" score"] = c_score
                result["CQ "+ args.model+" score reason"] = c_reason
                cq_score_list.extend(c_score)

            # Factual Correctness
            if('FC' in args.eval_metric):
                f_score, f_reason = evaluate_factual_correctness(
                    e_score,
                    entity,
                    item["target_claim_gen"],
                    result["target_location"],
                    result["true_target_entity"],
                    result["true_target_claim"],
                    model
                )
                result["FC "+args.model+" score"] = f_score
                result["FC "+args.model+" score reason"] = f_reason
                fc_score_list.append(f_score)

            output_list[id] = result
        
        with open(args.output_path, 'w', encoding='utf-8') as json_file:
            json.dump(output_list, json_file, indent=4, ensure_ascii=False)

        EC_metric = sum(ec_score_list)/len(ec_score_list)
        print(f"EC_metric: \n# samples = {len(ec_score_list)}\nEC = {EC_metric}")
        if('CQ' in args.eval_metric):
            CQ_metric = sum(cq_score_list)/len(cq_score_list)
            print(f"CQ_metric: \n# questions = {len(cq_score_list)}\nCQ = {CQ_metric}")
        if('FC' in args.eval_metric):
            FC_metric = sum(fc_score_list)/len(fc_score_list)
            print(f"FC_metric: \n# samples = {len(fc_score_list)}\nFC = {FC_metric}")
        
    else:
        print("Unsupported metric. Give the metric as a list. Metrics supported EC, CQ, FC.")
    
    
        
    
