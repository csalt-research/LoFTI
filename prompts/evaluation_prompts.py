# CQ Metric
EVAL_BY_GENERIC_QUES_PROMPT = """Given a target sentence, target location and a question, check whether the target sentence answers the given question correctly for the target location. Note that there could be multiple correct answers to the question for the target location. If the entity is from the target location and if the sentence correctly answers the question for the target location then assign a score of 1 and else assign a score of 0. Also, provide a reason for the score. For example:

Target sentence: ASCATSAT-1 is an Earth observation satellite developed by the Indian Space Research Organisation (ISRO). It was launched in 2016 to provide ocean wind vector data for weather forecasting, cyclone detection, and tracking. After its successful completion of the mission, it was handed over to the India Meteorological Department for routine operations.
Target location: India
Question: Mention the name of an earth observation satellite that consists of two satellites?
For the above target sentence, target location and question, the score and reason would be:
Score: 0
Reason: The target sentence mentions ASCATSAT-1, which is an Earth observation satellite developed by ISRO. However, it does not specify that ASCATSAT-1 consists of two satellites. The question specifically asks for an Earth observation satellite that consists of two satellites, and this information is not provided in the target sentence.

Target sentence: A train derailment occurred on February 3, 2023, at 8:55 p.m. IST, when 38 cars of a Vizianagaram freight train carrying hazardous materials derailed in Andhra Pradesh, India.
Target location: Andhra Pradesh
Question: Can you mention a train accident?
For the above target sentence, target location and question, the score and reason would be:
Score: 1
Reason: The target sentence clearly mentions a train derailment, which is a type of train accident, and specifies that it occurred in Andhra Pradesh. Thus, it answers the question in the context of the target location.

Target sentence: Amitabh Bachchan is an Indian actor and producer. He is widely regarded as one of India's leading actors, having appeared in a wide range of films in the protagonist role.
Target location: India
Question: Name an actor who has appeared in a wide range of films in an antagonist role?
For the above target sentence, target location and question, the score and reason would be:
Score: 0
Reason: The target sentence specifies that Amitabh Bachchan has appeared in films in the protagonist role, not the antagonist role. Therefore, it does not answer the question in the context of the target location (India).

Target sentence: {target_claim}
Target location: {target_location}
Question: {common_ques}
For the above target sentence, target location and question, the score and reason would be:
""".strip()

# EC Metric
DETECT_ENTITY_PROMPT = """Given a category, a reference location, reference sentence, reference entity, target location, and a target sentence, detect the target entity in the target sentence. 

For example:

Category: Actor/Actress
Reference location: US
Reference sentence: Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards, she has been named Hollywood's highest-paid actress multiple times.
Reference entity: Angelina Jolie
Target location: Kerala
Target sentence: Revathy is a renowned Indian actress and humanitarian from Kerala who has won several accolades including two National Film Awards.
The entity detected and the reason:
Target entity detected from the target sentence: Revathy
Reason: The sentence talks about actress Revathy.

Category: Amusement park
Reference location: France
Reference sentence: Disneyland Paris is an entertainment resort in Chessy, France, 32 kilometers east of Paris. It encompasses two theme parks, resort hotels, a shopping, dining and entertainment complex, and a golf course.
Reference entity: Disneyland Paris
Target location: India
Target sentence: Haw Par Villa is an entertainment resort in India. It includes multiple thrill rides, water attractions, theme parks, a shopping and dining complex, and hotel accommodations.
The entity detected and the reason:
Target entity detected from the target sentence: Haw Par Villa
Reason: The sentence talks about Haw Par Villa.

Category: {category}
Reference location: {ref_loc}
Reference sentence: {ref_sent}
Reference entity: {ref_entity}
Target location: {tar_loc}
Target sentence: {tar_sent}
The entity detected and the reason:
""".strip()

EVAL_THE_ENTITY_PROMPT = """Given a target location, category, possible target entity and a target entity to check, provide the score as below:
 
1) If the target entity EXACTLY matches the provided possible target entity, provide score 2.
2) Else if it is another POSSIBLE factually correct replacement for the possible target entity in the given target location, provide score 1. The entities should belong to the same given category and share similar properties.
3) Else, provide score 0.
 
Also, provide a reason for the score.
For example:
 
Target location: India
Category: Airlines
Possible target entity: Indigo
The score and reason are :
The target entity to check: Indigo
Score: 2
Reason: Exact match of entity.
 
Target location: Kerala
Category: Actor/Actress
Possible target entity: Manju Warrier
The target entity to check: Revathy
The score and reason are :
Score: 1
Reason: Revathy is also a renowned actress from Kerala similar to Manju Warrier.
 
Target location: India
Category: Amusement park
Possible target entity: Wonderla
The target entity to check: Haw Par Villa
The score and reason are:
Score: 0
Reason: Haw Par Villa is a theme park in Singapore but the target location is India, hence it is not a correct localization.
 
Target location: {tar_loc}
Category: {category}
Possible target entity: {poss_tar_entity}
The target entity to check: {target_entity}
The score and reason are:
""".strip()

# FC Metric
EVAL_BY_TRUE_TARGET_CLAIM_PROMPT = """Given an input sentence and true sentence, check if the input sentence is factually correct based on the true sentence provided. If the input sentence is factually correct compared to the true sentence, then assign a score of 1, else 0. Also, provide a reason for the score. If the input has any extra information that is not present in the true sentence, ensure that this extra information is factually correct based on your world knowledge.
For example:

Input sentence: Manju Warrier is a renowned Indian actress, predominantly working in the Malayalam film industry, based in Kerala. She has won numerous accolades for her acting skills, including four Kerala State Film Awards and a National Film Award. Often hailed as one of the finest actresses in the Malayalam cinema, Manju Warrier is a cultural icon in Kerala. has won several accolades including National Film Awards.
True sentence: Manju Warrier is an Indian actress, She has won numerous accolades, including the Kerala State Film Awards, and won a special mention from the jury for the National Film Awards. She is hailed as one of the finest actresses in the Malayalam cinema. She is hailed as one of the finest and highest-paid actresses in the Malayalam cinema.
The score and the reason:
Score: 1
Reason: All the details mentioned about Manju Warrier in the input sentence factually match with the true sentence.

Input sentence: Kempegowda International Airport is a 'The Green themed' entertainment and retail complex linked to the passenger terminals of Bengaluru Airport.
True sentence: Kempegowda International Airport is a 'Naurasa themed' with entertainment and retail area connected to the passenger terminals of Kempegowda International Airport, Bengaluru.
The score and the reason:
Score: 0
Reason: Kempegowda International Airport is not a 'The Green themed' airport but a 'Naurasa themed' according to the true sentence.

Input sentence: {tar_sent}
True sentence: {poss_tar_claim}
The score and the reason:
""".strip()

EVAL_BY_TRUE_EXAMPLE_PROMPT= """Given a sentence, check if the input sentence is factually correct for the given target location. A possible target entity and its factually correct sentence are given for your reference. Note, that there can be multiple correct entities for the given location.

If the input sentence is factually correct compared to the true sentence, then assign a score of 1, else 0. Also, provide a reason for the score.

Factually correct sentence of {poss_tar_entity} in {tar_loc}: {poss_tar_claim}

Now check if the below input sentence is also a factually correct statement for {entity_detected} in {tar_loc}:

Input sentence: {tar_sent}
The score and the reason:
Score: <fill score here>
Reason: <fill reason here>
""".strip()
