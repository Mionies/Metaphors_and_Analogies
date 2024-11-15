import json
import logging
import os
from tqdm import tqdm
from time import sleep
from typing import List
from statistics import mean
import pandas as pd
import openai
from datasets import load_dataset

openai.api_key = "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"

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
all_datasets = [
    'sat_full',
    # 'u2', 'u4', 'google', 'bats',
    # 't_rex_relational_similarity', 'conceptnet_relational_similarity', 'nell_relational_similarity', 'scan'
]

def get_reply(model, text):
    while True:
        try:
            reply = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": text}])
            break
        except Exception:
            print('Rate limit exceeded. Waiting for 10 seconds.')
            sleep(10)
    o = reply['choices'][0]['message']['content']
    print(o)
    return o


def get_input(options: List, query: List):
    q_h, q_t = query
    prompt_set = []
    for n, (h, t) in enumerate(options):
        tmp = "Answer the following question in one word :\nIs the relation between <1> and <2> analogous to the relation between <3> and <4>? \nAnswer:".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
        #tmp += "\nAnswer in whith the word \"true\" or with the word \"false\". Answer:\n"
        prompt_set.append(tmp)
    return prompt_set


def get_chat(model, data_name):
    dataset = load_dataset("relbert/analogy_questions_private", data_name, split="test")
    dataset_prompt = [get_input(query=x['stem'], options=x['choice']) for x in dataset]
    output_list = []
    answer = dataset['answer']
    for m,one_set in enumerate(dataset_prompt):
        for n, i in tqdm(enumerate(one_set)):
            reply = get_reply(model,i)
            print(answer[m]==n)
            output_list.append({"reply": reply, "input": i, "model": model, "answer": answer[m]==n})
    return output_list


if __name__ == '__main__':
    os.makedirs('results/chat', exist_ok=True)
    result = []
    for target_model in ['gpt-4','gpt-3.5-turbo']:
        for target_data_name in all_datasets:
            scores_file = f"results/chat/{target_model}.{target_data_name}.json"
            logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data_name}")
            if not os.path.exists(scores_file):
                scores_dict = get_chat(target_model, target_data_name)
                with open(scores_file, 'w') as f:
                    json.dump(scores_dict, f)
 