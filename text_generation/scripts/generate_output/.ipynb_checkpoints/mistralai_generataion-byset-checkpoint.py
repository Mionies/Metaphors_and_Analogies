""" Solving Metaphor Detection via Prompting
https://docs.google.com/document/d/1ZITlADHkJTuDBlIANCjTr1g5yhiLf7BoGkQyNrzfp4M/edit
"""
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
    ['Joanne/Metaphors_and_Analogies', "Quadruples_Green_set", "test"],
    ['Joanne/Metaphors_and_Analogies', 'Pairs_Cardillo_set', "test"],
    ['Joanne/Metaphors_and_Analogies', 'Pairs_Jankowiac_set', "test"],
]


def get_reply(text):
    sequences = pipeline(
        text,
        do_sample=False,
        #top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=200,
    )     
    return sequences[0]['generated_text']


def prompt(options: List, is_sentence: bool = False, prompt_type="3", cot: bool = False):
    if not is_sentence:
        assert all(len(i) == 4 for i in options), options
        statement = '\n'.join([f'{n+1}) {i[0]} is to {i[1]} what {i[2]} is to {i[3]}' for n, i in enumerate(options)])
    else:
        statement = '\n'.join([f'{n+1}) {i}' for n, i in enumerate(options)])
    if prompt_type == "3":
        __p = ["I will give you three sentences and I would like you to tell me which one is \"anomalous\", which one is "
               "\"literal\", and which one is a \"metaphor\". There is exactly one anomalous sentence, one metaphor, and one "
              f"literal sentence among the three provided sentences. Here are the three sentences:\n{statement}\n\n"
              "Please provide the answer in separate lines for each sentence.\n\nAnswer:\n\nSentence 1) is"]
        return __p


def get_chat(model, data, data_name, data_split, prompt_id, cot):
    dataset = load_dataset(data, data_name, split=data_split)
    if data_name == "Quadruples_Green_set":
        dataset_prompt = [prompt([ast.literal_eval(i['stem']) + c for c in i['pairs']], prompt_type=prompt_id, cot=cot) for i in dataset]
    elif data_name in ["Pairs_Cardillo_set", "Pairs_Jankowiac_set"]:
        dataset_prompt = [prompt(i['sentences'], is_sentence=True, prompt_type=prompt_id, cot=cot) for i in dataset]
    else:
        raise ValueError(f"unknown dataset {data_name}")
    # get scores
    scores = {"answer": dataset['answer'], "labels": dataset['labels']}
    if prompt_id == "3":
        output_list = []
        for i in dataset_prompt:
            output_list.append(get_reply(i[0]))
        scores["mixed"] = [{"input": x[0], "output": p} for x, p in zip(dataset_prompt, output_list)]
    return scores


#if __name__ == '__main__':



model_id = "/lustre/projects/cardiff/llms/Llama-2-13b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_id)
pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)




os.makedirs('metaphor_results/deterministic-byset', exist_ok=True)
# compute perplexity
for target_model in [model_id.split("/")[-1]]: #, 'gpt-4']:
    for target_data, target_data_name, target_split in dataset_list:
        for _prompt in ["3"]:
            for trial in [1]:#, 2, 3, 4, 5]:
                scores_file = f"metaphor_results/deterministic-byset/{target_model}.{os.path.basename(target_data)}_{target_data_name}_{target_split}.{_prompt}.{trial}.json"
                if not os.path.exists(scores_file):
                    logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data}/{target_data_name}/{target_split}`")
                    scores_dict = get_chat(target_model, target_data, target_data_name, target_split, prompt_id=_prompt, cot=False)
                    with open(scores_file, 'w') as f:
                        json.dump(scores_dict, f)

              