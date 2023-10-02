# A Replication Package to the Submission "Prompt Engineering or Fine Tuning: An Empirical Assessment of Large Language Models in Automated Software Engineering Tasks"

This is the replication package from the submission, "Prompt Engineering or Fine Tuning: An Empirical Assessment of Large Language Models in Automated Software Engineering Tasks".

In here, we 

## 0. Online Appendix
Here, we provide all the data from our surveys.
The information includes:

1. Example survey to show all the lists of questions we surveyed.
2. The task samples the surveyors queried 

## 1. Dataset
Datasets can be easily obtained from GitHub and Hugging Face. Here are the links to each datasets:

- Comment Generation (CSN from CodeXGLUE) in [GitHub](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text) and [HuggingFace](https://huggingface.co/datasets/code_x_glue_ct_code_to_text).
- Code Generation (HumanEval) in [GitHub](https://github.com/openai/human-eval) and [HuggingFace](https://huggingface.co/datasets/openai_humaneval).
- Code Generation (MBPP) in [Github](https://github.com/google-research/google-research/tree/master/mbpp) and in [HuggingFace](https://huggingface.co/datasets/mbpp).
- Code Translation (CT in CodeXGLUE) in [GitHub](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans) and [HuggingFace](https://huggingface.co/datasets/code_x_glue_cc_code_to_code_trans).



### If you want to run the minig script:

```
$ cd dataset/mining_atlas
$ python get_my_atlas.py
$ python utils.py
```

## 2. How to run our scripts
### 2.1 Comment Generation
1. cd into task folder.
2. run python script with specifying mode [basic|icl|ts]. 

basic for basic prompting, icl for incontext learning, ts for tast-specific prompting.
```
$ cd automated_prompting/comment_generation

$ python code2text.py [basic|icl|ts]
```

### 2.2 Code Generation
1. There are two benchmarks for this: HumanEval and MBPP.
2. cd into either benchmarks.
3. run the choice of prompting techinque of Jupyter notebooks.

```
$ cd automated_prompting/code_generattion/[humaneval|mbpp]
```
'run all' by opening the jupyter notebooks.