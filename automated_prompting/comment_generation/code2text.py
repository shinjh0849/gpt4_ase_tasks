import backoff
import json
import openai
import os
from tqdm import tqdm
from datasets import load_dataset
import sys
import random

openai.organization = ''
openai.api_key = ''


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.APIError, openai.error.Timeout, openai.error.ServiceUnavailableError))
def get_completion(prompt, code, lang, max_token, engine='gpt-4'):
    try:
        response = openai.ChatCompletion.create(
            model=engine,
            messages=prompt,
            temperature=0, # this is the degree of randomness of the model's output
        )
        # print(response)
        return response['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError:
        max_token -= 5
        code = ' '.join(code.split()[:max_token]).strip()
        prompt = [{"role": "system", "content": f"You are a {lang} code summarizer."},
                    {"role": "user", "content": f"""Given a {lang} code snippet surrounded in ???,
                     generate one line of semantic focused and abstract summarization ???{code}???"""}]
        response = get_completion(prompt, code, lang, max_token)
        


def gen_comments(lang, num):
    max_token = 500
    dataset = load_dataset("code_x_glue_ct_code_to_text", lang)
    test_dict = dataset['test']

    os.makedirs('output/basic_prompt', exist_ok=True)    
    generated_comments_f = open(f'output/basic_prompt/{lang}_generated_{num}.txt', 'w')
    ground_truth_f = open(f'output/basic_prompt/{lang}_grount_truth_{num}.txt', 'w')
    for cnt, test in enumerate(tqdm(test_dict, total=len(test_dict))):
        if cnt < num: continue
        code = test['code']
        if len(code.split()) > max_token:
            code = ' '.join(code.split()[:max_token]).strip()
        prompt = [{"role": "system", "content": f"You are a {lang} code summarizer."},
                    {"role": "user", "content": f"""Given a {lang} code snippet surrounded in ???, \
                    generate one line of semantic focused and abstract summarization ???{code}???"""}]
        response = get_completion(prompt, code, lang, max_token)
        if not response:
            response = 'no_gen'
        if len(response.splitlines()) > 1:
            response = ' '.join(response.splitlines()).strip()
        assert len(response.splitlines()) == 1
        generated_comments_f.write(response + '\n')
        ground_truth = ' '.join(test['docstring_tokens']).strip()
        ground_truth_f.write(ground_truth + '\n')
    generated_comments_f.close()
    ground_truth_f.close()    
    
    
    
def gen_comments_ts(lang, num):
    max_token = 500
    dataset = load_dataset("code_x_glue_ct_code_to_text", lang)
    test_gt = dataset['test']
    with open (f'output/with_sim_ex/{lang}.jsonl') as f:
        json_list = list(f)
    test_dict = []
    for json_str in json_list:
        result = json.loads(json_str)
        test_dict.append(result)
        
    percentage = 10
    k = len(test_dict) * percentage // 100
    indicies = random.sample(range(len(test_dict)), k)
    samples = [test_dict[i] for i in indicies]
    samples_gt = [test_gt[i] for i in indicies]
    
    os.makedirs('output/ts', exist_ok=True)    
    generated_comments_f = open(f'output/ts/{lang}_generated_{num}.txt', 'w')
    ground_truth_f = open(f'output/ts/{lang}_ground_truth_{num}.txt', 'w')
    for cnt, (test, ground_truth) in enumerate(tqdm(zip(samples, samples_gt), total=len(samples))):
        if cnt < num: continue
        code = test['test_code']
        code1 = test['sim_codes'][0]
        code2 = test['sim_codes'][1]
        code3 = test['sim_codes'][2]
        nl1 = test['sim_nls'][0]
        nl2 = test['sim_nls'][1]
        nl3 = test['sim_nls'][2]

        if len(code.split()) > max_token:
            code = ' '.join(code.split()[:max_token]).strip()
        prompt = [{"role": "system", "content": f"You are a {lang} code summarizer."},
                  {"role": "user", "content": f""""Generate one line of semantic focused and abstract summarization \
                    of the code surrounded by ???. Compose the summarization by naturalizing the identifier of \
                    variables and function names in the code as keywords. The summarization should be very \
                    concise, with a approximate limitation of around 15 token length. Here are three examples \
                    summary followed by its code. Summary 1: {nl1} Code 1: {code1}. Summary 2: {nl2} Code 2: {code2}. \
                    Summary 3:  {nl3} Code 3: {code3}. ???{code}???"""}]
        response = get_completion(prompt, code, lang, max_token)
        if not response:
            response = 'no_gen'
        if len(response.splitlines()) > 1:
            response = ' '.join(response.splitlines()).strip()
        assert len(response.splitlines()) == 1
        generated_comments_f.write(response + '\n')
        ground_truth_f.write(' '.join(ground_truth['docstring_tokens']).strip() + '\n')
    generated_comments_f.close()
    ground_truth_f.close()
            
            
            
def gen_comments_icl(lang, num):
    max_token = 500
    with open (f'output/with_sim_ex/{lang}.jsonl') as f:
        json_list = list(f)
    test_dict = []
    for json_str in json_list:
        result = json.loads(json_str)
        test_dict.append(result)
        
    os.makedirs('output/icl', exist_ok=True)    
    generated_comments_f = open(f'output/icl/{lang}_generated_{num}.txt', 'w')
    for cnt, test in enumerate(tqdm(test_dict, total=len(test_dict))):
        if cnt < num: continue
        code = test['test_code']
        code1 = test['sim_codes'][0]
        code2 = test['sim_codes'][1]
        code3 = test['sim_codes'][2]
        nl1 = test['sim_nls'][0]
        nl2 = test['sim_nls'][1]
        nl3 = test['sim_nls'][2]

        if len(code.split()) > max_token:
            code = ' '.join(code.split()[:max_token]).strip()
        prompt = [{"role": "system", "content": f"You are a {lang} code summarizer."},
                  {"role": "user", "content": f""""Given three examples of natural language and {lang} code pairs, \
                    generate one line of semantic focused and abstract summarization of the code surrounded by ???. \
                    Natural language 1: {nl1} Code 1: {code1} Natural language 2: {nl2} Code 2: {code2} \
                    Natural language 3:  {nl3} Code 3: {code3} ???{code}???"""}]
        response = get_completion(prompt, code, lang, max_token)
        if not response:
            response = 'no_gen'
        if len(response.splitlines()) > 1:
            response = ' '.join(response.splitlines()).strip()
        assert len(response.splitlines()) == 1
        generated_comments_f.write(response + '\n')
    generated_comments_f.close()
    


lang = sys.argv[1]
mode = sys.argv[2]

if mode == 'basic':
    gen_comments(lang, 0)
elif mode == 'icl': # in-context-learning
    gen_comments_icl(lang, 0)
elif mode == 'ts': # task-specific
    gen_comments_ts(lang, 0)
else:
    print('invalid mode!')