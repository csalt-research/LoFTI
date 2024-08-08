TARGET_SENT_GEN_PROMPT_WITH_LOCATION = """You are a localization assistant. Convert the reference entity sentence from English to the Indian domain by localizing the reference sentence with a similar entity from the target location. Make the needed modifications in the sentence to make it factually correct for the target location. Output answers in English using multi-entity localization. Use the below format.

My reference sentence: <reference claim>
Target location: <target_location>
Target sentence: <localized target sent>
Reason: <reason for the localization>.

My reference sentence: {claim}
Target location: {location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
""".strip()

TARGET_SENT_GEN_PROMPT_WITH_LOCATION_mixtral = """[INST]You are a localization assistant. Convert the reference entity sentence from English to the Indian domain by localizing the reference sentence with a similar entity from the target location. Make the needed modifications in the sentence to make it factually correct for the target location. Output answers in English using multi-entity localization. Use the below format.

My reference sentence: <reference claim>
Target location: <target_location>
Target sentence: <localized target sent>
Reason: <reason for the localization>.

My reference sentence: {claim}
Target location: {location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
[/INST]""".strip()

TARGET_SENT_GEN_PROMPT_WITH_LOCATION_llama = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a localization assistant. Convert the reference entity sentence from English to the Indian domain by localizing the reference sentence with a similar entity from the target location. Make the needed modifications in the sentence to make it factually correct for the target location. Output answers in English using multi-entity localization. Use the below format.

My reference sentence: <reference claim>
Target location: <target_location>
Target sentence: <localized target sent>
Reason: <reason for the localization>.
<|eot_id|><|start_header_id|>user<|end_header_id|>

My reference sentence: {claim}
Target location: {location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
<|eot_id|><|start_header_id|>assistant<|end_header_id|>""".strip()

TARGET_SENT_GEN_PROMPT_WITH_CQ = """Given a question and a target location, generate a factually correct sentence such that it answers the given question using an entity from the target location. A reference location and sentence is given as an example.Output the answers in English. Use the below format.

Question: <question_to_be_answered>
Reference location: <example_reference_location>
Reference sentence: <example_reference_sentence>
Target location: <target_location>
Target sentence: <target_sent>
Reason: <reason for the localization>.

Question: {question}
Reference location: {ref_location}
Reference sentence: {ref_claim}
Target location: {tar_location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
""".strip()

TARGET_SENT_GEN_PROMPT_WITH_CQ_mixtral = """[INST]Given a question and a target location, generate a factually correct sentence such that it answers the given question using an entity from the target location. A reference location and sentence is given as an example.Output the answers in English. Use the below format.

Question: <question_to_be_answered>
Reference location: <example_reference_location>
Reference sentence: <example_reference_sentence>
Target location: <target_location>
Target sentence: <target_sent>
Reason: <reason for the localization>.

Question: {question}
Reference location: {ref_location}
Reference sentence: {ref_claim}
Target location: {tar_location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
[/INST]""".strip()

TARGET_SENT_GEN_PROMPT_WITH_CQ_llama = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>Given a question and a target location, generate a factually correct sentence such that it answers the given question using an entity from the target location. A reference location and sentence is given as an example.Output the answers in English. Use the below format.

Question: <question_to_be_answered>
Reference location: <example_reference_location>
Reference sentence: <example_reference_sentence>
Target location: <target_location>
Target sentence: <target_sent>
Reason: <reason for the localization>.
<|eot_id|><|start_header_id|>user<|end_header_id|>

Question: {question}
Reference location: {ref_location}
Reference sentence: {ref_claim}
Target location: {tar_location}
Target sentence: <fill_your_answer_here>
Reason: <fill_your_answer_here>
<|eot_id|><|start_header_id|>assistant<|end_header_id|>""".strip()