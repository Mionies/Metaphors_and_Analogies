logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
all_datasets = [
    'sat_full',
    # 'u2', 'u4', 'google', 'bats',
    # 't_rex_relational_similarity', 'conceptnet_relational_similarity', 'nell_relational_similarity', 'scan'
]


def get_input(options: List, query: List, answer: int ,prompt_type: str ,new_answer_id : int):
    q_h, q_t = query
    correct_opt = options[answer]
    other_opt = [options[i] for i in range(5) if i!=answer]
    other_opt.insert(new_answer_id,correct_opt)
    if prompt_type == '1':
        prefix = "<s> [INST] Answer the question by choosing the correct option. Which of the following is an analogy?\n"
        for n, (h, t) in enumerate(other_opt):
            tmp = "<1> is to <2> what <3> is to <4>".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    elif prompt_type == "3":
        prefix = "<s> [INST] Only one of the following statements is correct. Please answer by choosing the correct option.\n"
        for n, (h, t) in enumerate(other_opt):
            tmp = "The relation between <1> and <2> is analogous to the relation between <3> and <4>.".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    else:
        raise ValueError("unknown prompt type")
    prefix += "[/INST] The answer is"
    #print(prefix)
    return prefix

# llama2
def get_reply(text):
    sequences = pipeline(
        text,
        #do_sample=False,
        #top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=150,
    )  
    o = sequences[0]['generated_text']
    print(o)
    return o

#llama3
def get_reply(text):
    messages = [
    {"role": "system", "content": "You always anser in one line. You give the correct answer by outputing the sentence indice (for example \"1)\",\"2)\" or \"3)\")."},
    {"role": "user", "content": text }
    ]
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = inputs.to('cuda') 
    outputs = model.generate(**inputs,max_new_tokens=50,do_sample=True)
    reply = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0],
    print(reply[-50:])
    return reply

#llam3
def get_input(options: List, query: List, answer: int ,prompt_type: str ,new_answer_id : int):
    q_h, q_t = query
    correct_opt = options[answer]
    other_opt = [options[i] for i in range(5) if i!=answer]
    other_opt.insert(new_answer_id,correct_opt)
    if prompt_type == '1':
        prefix = "Answer the question by choosing the correct option. Which of the following is an analogy?\n"
        for n, (h, t) in enumerate(other_opt):
            tmp = "<1> is to <2> what <3> is to <4>".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    else:
        raise ValueError("unknown prompt type")
    return prefix

def get_input(options: List, query: List, answer: int ,prompt_type: str ,new_answer_id : int):
    q_h, q_t = query
    correct_opt = options[answer]
    other_opt = [options[i] for i in range(5) if i!=answer]
    other_opt.insert(new_answer_id,correct_opt)
    if prompt_type == '1':
        prefix = "Answer the question by choosing the correct option. Which of the following is an analogy?\n"
        for n, (h, t) in enumerate(other_opt):
            tmp = "<1> is to <2> what <3> is to <4>".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    elif prompt_type == "3":
        prefix = "Only one of the following statements is correct. Please answer by choosing the correct option.\n"
        for n, (h, t) in enumerate(other_opt):
            tmp = "The relation between <1> and <2> is analogous to the relation between <3> and <4>.".replace("<1>", q_h).replace("<2>", q_t).replace("<3>", h).replace("<4>", t)
            prefix += f"{n + 1}) {tmp}\n"
    else:
        raise ValueError("unknown prompt type")
    prefix += "The answer is"
    #print(prefix)
    return prefix


def get_chat(model, data_name, prompt_id, new_answer_id):
    dataset = load_dataset("relbert/analogy_questions_private", data_name, split="test")
    dataset_prompt = [get_input(query=x['stem'], options=x['choice'],answer=x["answer"], prompt_type=prompt_id, new_answer_id=new_answer_id) for x in dataset]
    output_list = []
    answer = dataset['answer']
    for n, i in tqdm(enumerate(dataset_prompt)):
        reply = get_reply(i)
        output_list.append({"reply": reply, "input": i, "model": model, "answer": new_answer_id})
    return output_list



if __name__ == '__main__':
    os.makedirs('results/permutation-mix', exist_ok=True)
    # compute perplexity
    result = []
    for target_model in ['mix24']:
        for target_data_name in all_datasets:
            for _prompt in ["1", "3"]:
                for new_answer_id in range(5):
                    scores_file = f"results/permutation-mix/{target_model}.{target_data_name}.{_prompt}.{new_answer_id}.json"
                    logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data_name}`, prompt: `{_prompt}`,answer_id:`{new_answer_id}`")
                    if not os.path.exists(scores_file):
                        scores_dict = get_chat(target_model, target_data_name, prompt_id=_prompt,new_answer_id=new_answer_id)
                        with open(scores_file, 'w') as f:
                            json.dump(scores_dict, f)
                   



os.makedirs('results/permutation-llama3-sat', exist_ok=True)
    # compute perplexity

result = []
for target_model in ['llama3']:
    for target_data_name in all_datasets:
        for _prompt in ["1"]:
            for new_answer_id in range(5):
                scores_file = f"results/permutation-llama3-sat/{target_model}.{target_data_name}.{_prompt}.{new_answer_id}.json"
                logging.info(f"[COMPUTING PERPLEXITY] model: `{target_model}`, data: `{target_data_name}`, prompt: `{_prompt}`,answer_id:`{new_answer_id}`")
                if not os.path.exists(scores_file):
                    scores_dict = get_chat(target_model, target_data_name, prompt_id=_prompt,new_answer_id=new_answer_id)
                    with open(scores_file, 'w') as f:
                        json.dump(scores_dict, f)





                            def prompt(options: List, answers, perm, is_sentence: bool = False):
                                options = Reorder(options,answers,perm)
                                if not is_sentence:
                                    assert all(len(i) == 4 for i in options), options
                                    statement = '\n'.join([f'{n+1}) {i[0]} is to {i[1]} what {i[2]} is to {i[3]}' for n, i in enumerate(options)])
                                else:
                                    statement = '\n'.join([f'{n+1}) {i}' for n, i in enumerate(options)])
                              #  __p = ["<s> [INST] I will give you three sentences and I would like you to tell me which one is \"anomalous\", which one is "
                              #          "\"literal\", and which one is a \"metaphor\". There is exactly one anomalous sentence, one metaphor, and one "
                              #          f"literal sentence among the three provided sentences. Here are the three sentences:\n{statement}\n\n"
                              #          "Please provide the answer in separate lines for each sentence.[/INST] Answer:\n\nSentence 1) is"]
                                __p = ["<s> [INST] I will give you two sentences and I would like you to tell me which one is "
                                   "\"literal\" and which one is a \"metaphor\". There is exactly one metaphor and one "
                                  f"literal sentence among the two provided sentences. Here are the two sentences:\n{statement}\n\n"
                                  "Please provide the answer in separate lines for each sentence.[/INST] Answer: Sentence 1) is"]
                                return __p

