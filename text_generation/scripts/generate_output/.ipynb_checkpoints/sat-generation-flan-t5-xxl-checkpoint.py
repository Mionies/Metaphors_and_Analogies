import json
import logging
import os
from tqdm import tqdm
from time import sleep
from typing import List
from statistics import mean
import pandas as pd

from datasets import load_dataset

#openai.api_key = os.getenv("OPENAI_API_KEY", None)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
all_datasets = [
    'sat_full',
    # 'u2', 'u4', 'google', 'bats',
    # 't_rex_relational_similarity', 'conceptnet_relational_similarity', 'nell_relational_similarity', 'scan'
]

def get_reply(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100,do_sample=False)
    o = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    print(o)
    return o


def get_input(options: List, query: List, prompt_type: str = "1"):
    q_h, q_t = query
    if prompt_type == '1':
        prefix = "Answer the question by choosing the correct option. Which of the following is an analogy?\n"
        for n, (h, t) in enumerate(options):
            tmp = "<1> is to <2> what <3> is to <4>".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    elif prompt_type == "2":
        prefix = "Answer the question by choosing the correct option. Which of the following is analogous to <1> and <2>?\n".replace("<1>", q_h).replace("<2>", q_t)
        for n, (h, t) in enumerate(options):
            tmp = "<3> and <4>".replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    elif prompt_type == "3":
        prefix = "Only one of the following statements is correct. Please answer by choosing the correct option.\n"
        for n, (h, t) in enumerate(options):
            tmp = "The relation between <1> and <2> is analogous to the relation between <3> and <4>.".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    else:
        raise ValueError("unknown prompt type")
    prefix += "The answer is"
    return prefix


def get_chat(model, data_name, prompt_id):
    dataset = load_dataset("relbert/analogy_questions_private", data_name, split="test")
    dataset_prompt = [get_input(query=x['stem'], options=x['choice'], prompt_type=prompt_id) for x in dataset]
    output_list = []
    answer = dataset['answer']
    for n, i in tqdm(enumerate(dataset_prompt)):
        reply = get_reply(i)
        output_list.append({"reply": reply, "input": i, "model": model, "answer": answer[n]})
    return output_list


#if __name__ == '__main__':
os.makedirs('results/chat', exist_ok=True)
result = []
for target_model in ['flan-t5-xxl']:
    for target_data_name in all_datasets:
        for _prompt in ["1", "3"]:
            scores_file = f"results/chat/{target_model}.{target_data_name}.{_prompt}.json"
            logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data_name}`, prompt: `{_prompt}`")
            if not os.path.exists(scores_file):
                scores_dict = get_chat(target_model, target_data_name, prompt_id=_prompt)
                with open(scores_file, 'w') as f:
                    json.dump(scores_dict, f)


with open(scores_file) as f:
    scores_dict = json.load(f)

result = []
accuracy = []
for s in a1:#scores_dict:
    out = s['input'].split("\n")[1:-1]
    if s['reply'][0] in ['1', '2', '3', '4', '5']:
        pred = int(s['reply'][0]) - 1
    elif s['reply'].replace("option ", "").replace("Option ", "").replace(": ", "")[0] in ['1', '2', '3', '4', '5']:
        pred = int(s['reply'].replace("option ", "").replace("Option ", "").replace(": ", "")[0]) - 1
    elif any(s['reply'][:-1].lower() in o.lower() for o in out):
        pred = int([o for o in out if s['reply'][:-1].lower() in o.lower()][0][0]) - 1
    else:
        print()
        print(out)
        print(s['reply'])
        print()
        raise ValueError("unknown reply")
    accuracy.append(int(int(s['answer']) == pred))
    result.append(pred)




result.append({"accuracy": mean(accuracy), "model": target_model, "data": target_data_name, "prompt": _prompt})
df = pd.DataFrame(result)
print(df)


    ================================

    def get_reply(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)#,min_length=25, max_length=100,do_sample=False)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)


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

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer



model_name = "/lustre/projects/cardiff/llms/flan-t5-xxl"
#model_name = "/lustre/projects/cardiff/llms/flan-ul2"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)




os.makedirs('metaphor_results/chatdefault-1by1', exist_ok=True)
# compute perplexity
for target_model in [model_name.split("/")[-1]]: #, 'gpt-4']:
    for target_data, target_data_name, target_split in dataset_list:
        for _prompt in ["3"]:
            for trial in [1, 2, 3, 4, 5]:
                scores_file = f"metaphor_results/chatdefault-1by1/{target_model}.{os.path.basename(target_data)}_{target_data_name}_{target_split}.{_prompt}.{trial}.json"
                if not os.path.exists(scores_file):
                    logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data}/{target_data_name}/{target_split}`")
                    scores_dict = get_chat(target_model, target_data, target_data_name, target_split, prompt_id=_prompt, cot=False)
                    with open(scores_file, 'w') as f:
                        json.dump(scores_dict, f)




sat possible labels      1),2),3),4),5)
true label distribution :63, 91, 82, 71, 67
prompt 1 :124, 95, 67, 32, 56
prompt 2 :141, 66, 42, 30, 95

flan-t5-xxl generation acccuracies 0.39 and 0.4