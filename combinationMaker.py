import json

json_files_train = [
    "Bali/data/train/bali-indo_entries_train.json",
    "Minang/data/train/minang-indo_entries_train.json",
    "Sunda/data/train/sunda-indo_entries_train.json",
]
json_files_eval = [
    "Bali/data/eval/bali-indo_entries_eval.json",
    "Minang/data/eval/minang-indo_entries_eval.json",
    "Sunda/data/eval/sunda-indo_entries_eval.json",
]

combined_json_file_train = "Combination/data/train/combination_train.json"
combined_json_file_eval = "Combination/data/eval/combination_eval.json"

def load_json(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def combine_json_files(file_paths):
    combined_data = []
    for file_path in file_paths:
        data = load_json(file_path)
        combined_data.extend(data)
    return combined_data

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')
            
combined_data_train = combine_json_files(json_files_train)
combined_data_eval = combine_json_files(json_files_eval)
save_json(combined_data_train, combined_json_file_train)
save_json(combined_data_eval, combined_json_file_eval)

print("Done")

