import json
from prompts import eval_prompts
from utils import chatgpt_prompt, api

# ec correctness         
def evaluate_target_claim_by_entity(ref_entity, ref_loc, ref_claim, tar_claim, location, true_tar_entity, category):
    entity = ""
    score = 0
    reason = ""
    prompt = eval_prompts.DETECT_ENTITY_PROMPT
    prompt = prompt.format(
        ref_entity=ref_entity,
        ref_loc = ref_loc,
        ref_sent = ref_claim,
        tar_sent = tar_claim,
        tar_loc = location,
        category = category)
    for i in range(0,3):
        response = chatgpt_prompt.chat_gpt(prompt, api.OPENAI_KEY)
        entity_search_string = "Target entity detected from the target sentence:"
        for resp in response.split("\n"):
            if entity_search_string in resp:
                entity = resp.split(entity_search_string)[1].strip()
        if(entity != ""):
            break
    if(entity != ""):
        prompt = eval_prompts.EVAL_THE_ENTITY_PROMPT
        prompt = prompt.format(
            tar_loc = location,
            poss_tar_entity = true_tar_entity,
            target_entity = entity,
            category = category)
        response = chatgpt_prompt.chat_gpt(prompt, api.OPENAI_KEY)
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
def evaluate_target_claim_by_fact(tar_claim, location, true_tar_entity, true_tar_claim, flag, entity_detected):
    if(flag == 2):
        prompt = eval_prompts.EVAL_BY_TRUE_TARGET_CLAIM_PROMPT
        prompt = prompt.format(
            tar_sent = tar_claim,
            poss_tar_claim = true_tar_claim)
    else: #flag == 1
        prompt = eval_prompts.EVAL_BY_TRUE_EXAMPLE_PROMPT
        prompt = prompt.format(
            tar_sent = tar_claim,
            tar_loc = location,
            poss_tar_entity = true_tar_entity,
            poss_tar_claim = true_tar_claim,
            entity_detected = entity_detected)

    response = chatgpt_prompt.chat_gpt(prompt, api.OPENAI_KEY)
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
def evaluate_target_claim_by_common_ques(claim, location, question):
    prompt = eval_prompts.EVAL_BY_GENERIC_QUES_PROMPT
    prompt = prompt.format(target_location=location,
                           target_claim=claim,
                           common_ques=question)
    response = chatgpt_prompt.chat_gpt(prompt, api.OPENAI_KEY)
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

def evaluate_factual_correctness(ec_score, entity, tar_claim, tar_location, true_tar_entity, true_tar_claim):
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

def evaluate_entity_correctness(ref_entity, ref_loc, ref_claim, tar_claim, tar_location, true_tar_entity, category):
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

def evaluate_common_ques_correctness(ec_score, tar_claim, tar_location, common_questions):
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
    with open("/root/RnD_Project/dataset/new_1100_dataset.json", 'r', encoding='utf-8') as json_file:
        eval_data = json.load(json_file)

    # i = 500
    # input_file_dir = "/root/RnD_Project/mixtral_model/outputs/mixtral_zero_shot/1100_samples/outputs_"+str(i)+"_"+str(i+100)+"/"
    # with open(input_file_dir+"results.json", 'r') as json_file:
    #     claim_data = json.load(json_file)
    
    input_file_dir = "/root/RnD_Project/llama3/outputs/250_samples/"
    with open(input_file_dir+"results.json", 'r') as json_file:
        claim_data = json.load(json_file)

    output_list = {}
    e_score_list = []
    f_score_list = []
    for i,item in enumerate(claim_data):
        claim_id = item["claim_id"]
        result = eval_data[str(claim_id)].copy()
        e_score, e_reason, entity = evaluate_entity_correctness(
                    result["reference_entity"],
                    result["reference_location"],
                    result["reference_claim"],
                    item["target_claim_gen"],
                    result["target_location"],
                    result["true_target_entity"],
                    result["category"]
                    )

        f_score, f_reason = evaluate_factual_correctness(
                    e_score,
                    entity,
                    item["target_claim_gen"],
                    result["target_location"],
                    result["true_target_entity"],
                    result["true_target_claim"]
                )

        c_score, c_reason = evaluate_common_ques_correctness(
                    e_score,
                    item["target_claim_gen"],
                    result["target_location"],
                    result["common_questions"]
                )

        result["claim_to_evaluate"] = item["target_claim_gen"]
        result["entity_detected"] = entity
        if(e_score == 2):
            result["EC GPT4 score"] = 1
            result["EC GPT4 score reason"] = "Exact match. " + e_reason
        else:
            result["EC GPT4 score"] = e_score
            result["EC GPT4 score reason"] = e_reason

        result["CQ GPT4 score"] = c_score
        result["CQ GPT4 score reason"] = c_reason
        result["FC GPT4 score"] = f_score
        result["FC GPT4 score reason"] = f_reason
        e_score_list.append(result["EC GPT4 score"])
        f_score_list.append(f_score)
        output_list[claim_id] = result
        print(f"Claim {claim_id} done")
    
    with open(input_file_dir+"EC_CQ_FC_.json", 'w', encoding='utf-8') as json_file:
        json.dump(output_list, json_file, indent=4, ensure_ascii=False)
        
    EC_metric = sum(e_score_list)/len(e_score_list)
    FC_metric = sum(f_score_list)/len(f_score_list)
    print("Count", sum(e_score_list))
    print("Total_samples", len(e_score_list))
    print("EC_metric", EC_metric)
    print("Count", sum(f_score_list))
    print("Total_samples", len(f_score_list))
    print("FC_metric", FC_metric)
    
