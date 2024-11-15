import json
import ast
import logging
import os
from time import sleep
from typing import List
from datasets import load_dataset
from transformers import AutoTokenizer
import transformers
import torch



logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
label_template = {"metaphor": "is a metaphor", "literal": "is literal", "anomaly": "is difficult to interpret"}
dataset_list = [  # dataset, dataset_name, split
    #"Quadruples_Green_set", "test"],
    ['../../../datasets/Cardillo/cardillo.jsonl', 'Pairs_Cardillo_set', "test"],
    #['../../../datasets/Jankowiak/Jankowiak.jsonl', 'Pairs_Jankowiac_set', "test"],
]


#permutations = [[0,1,2],[0,2,1],[1,2,0],[1,0,2],[2,0,1]]#,[2,1,0]]
permutations = [[1,2],[2,1]]


def Reorder(one_set:list,answers:list, perm:list):
    new_set = []
    for p in perm:
        i = answers.index(p)
        new_set.append(one_set[i])
    return new_set 


def get_reply(text):
    inputs = tokenizer(text, return_tensors="pt")                                         
    outputs = model.generate(**inputs,max_length=150, min_length=10) 
    o = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]   
    print(text)                         
    print("-->",o)                                    
    return o  



def prompt(options: List, answers, perm, is_sentence: bool = False):
    options = Reorder(options,answers,perm)
    if not is_sentence:
        assert all(len(i) == 4 for i in options), options
        statement = '\n'.join([f'{n+1}) {i[0]} is to {i[1]} what {i[2]} is to {i[3]}' for n, i in enumerate(options)])
    else:
        statement = '\n'.join([f'{n+1}) {i}' for n, i in enumerate(options)])
    __p = ["I will give you two sentences and I would like you to tell me which one is "
       "\"literal\" and which one is a \"metaphor\". There is exactly one metaphor and one "
      f"literal sentence among the two provided sentences. Here are the two sentences:\n{statement}\n\n"
      "Please provide the answer in separate lines for each sentence. Answer: Sentence 1) is"]
    return __p
    #__p = ["I will give you three sentences and I would like you to tell me which one is \"anomalous\", which one is "
    #        "\"literal\", and which one is a \"metaphor\". There is exactly one anomalous sentence, one metaphor, and one "
    #        f"literal sentence among the three provided sentences. Here are the three sentences:\n{statement}\n\n"
    #        "Please provide the answer in separate lines for each sentence. Answer:\n\nSentence 1) is"]




def get_chat(model, data, data_name, data_split,perm):
    dataset = load_dataset('json', data_files=data)
    if data_name == "Quadruples_Green_set":
        dataset_prompt = [prompt([ast.literal_eval(i['stem']) + c for c in i['pairs']],i["labels"],perm) for i in dataset["train"]]
    elif data_name in ["Pairs_Cardillo_set", "Pairs_Jankowiac_set"]:
        dataset_prompt = [prompt(i['sentences'],i["labels"], perm,is_sentence=True) for i in dataset["train"]]
    else:
        raise ValueError(f"unknown dataset {data_name}")
    # get scores
    scores = {"labels": [perm for i in range(len(dataset["train"]['answer']))]}
    output_list = []
    print(dataset_prompt)
    for i in dataset_prompt:
        output_list.append(get_reply(i[0]))
    scores["mixed"] = [{"input": x[0], "output": p} for x, p in zip(dataset_prompt, output_list)]
    return scores


##################################################################
# Load model
model_name = "google/flan-t5-xxl"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


os.makedirs('metaphor_results/flan-permutation', exist_ok=True)
# compute perplexity
for target_model in ["flan-t5-xxl"]: 
    for target_data, target_data_name, target_split in dataset_list:
        for p in permutations:
            perm = str(p[0])+str(p[1])#+str(p[2])
            scores_file = f"metaphor_results/flan-permutation/{target_model}.{os.path.basename(target_data)}_{target_data_name}_{target_split}.{perm}.json"
            if not os.path.exists(scores_file):
                logging.info(f"[GENERATING ANSWER] model: `{target_model}`, data: `{target_data}/{target_data_name}/{target_split}`")
                scores_dict = get_chat(target_model, target_data, target_data_name, target_split, p)
                with open(scores_file, 'w') as f:
                    json.dump(scores_dict, f)



