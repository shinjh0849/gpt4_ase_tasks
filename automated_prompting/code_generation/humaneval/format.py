import json
read_files = ["humaneval_basic.txt", "humaneval_in_context.txt", "humaneval_task_specific.txt"]
write_files = ["humaneval_basic.jsonl", "humaneval_in_context.jsonl", "humaneval_task_specific.jsonl"]
for read_file_name, write_file_name in zip(read_files, write_files):
    with open(write_file_name, "w") as write_file:
        with open(read_file_name) as read_file:
            lines = [line.rstrip() for line in read_file]
            for index, line in enumerate(lines):
                d = {"task_id": "HumanEval/" + str(index), "completion": line}
                json.dump(d, write_file)
                write_file.write("\n")