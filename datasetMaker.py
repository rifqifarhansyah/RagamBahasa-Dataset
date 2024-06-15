import random
import pandas as pd
import os
import json

substitutions = {
    'o': '0', 'O': '0', 's': '5', 'S': '5', 'g': '9', 'G': '9', 
    'A': '4', 'z': '2', 'Z': '2', 'l': '1', 'I': '1', 'B': '8', 
    'e': 'c', 'a': 'o', 'E': 'C', 'u': 'v', 'm': 'rn', 'rn': 'm'
}

def mask_character(char):
    if char in substitutions:
        random_choice = random.random()
        if random_choice < 0.80:
            return substitutions[char]
        elif random_choice < 0.90:
            return chr(random.choice(list(range(65, 91)) + list(range(97, 123))))
        elif random_choice < 0.95:
            return ' '
        else:
            return char
    return char

def generate_variations(word):
    indices = [i for i, char in enumerate(word) if char in substitutions]
    if not indices:
        return [word]
    num_variations = max(1, int(0.15 * len(word)))

    variations = set()
    while len(variations) < num_variations:
        variation = list(word)
        random_index = random.choice(indices)
        variation[random_index] = mask_character(word[random_index])
        variations.add(''.join(variation))

    return list(variations)

def create_dataset(corrected_file_path, train_ratio, col_id):
    df = pd.read_excel(corrected_file_path)
    corrected_texts = df.iloc[:, col_id].dropna().astype(str).tolist()

    dataset = []
    for corrected_text in corrected_texts:
        pair = {"input": corrected_text, "output": corrected_text}
        dataset.append(pair)
        variations = generate_variations(corrected_text)
        for variation in variations:
            pair = {"input": variation, "output": corrected_text}
            dataset.append(pair)

    random.shuffle(dataset)

    num_samples = len(dataset)
    num_train_samples = int(num_samples * train_ratio)
    train_data = dataset[:num_train_samples]
    eval_data = dataset[num_train_samples:]
    
    base_path, file_name = os.path.split(corrected_file_path)
    base_path = os.path.dirname(os.path.dirname(base_path))
    data_directory = os.path.basename(os.path.dirname(corrected_file_path))
    file_name_without_ext = os.path.splitext(file_name)[0]
    output_train_path = os.path.join(base_path, "train", data_directory, f"{file_name_without_ext}_train.json")
    output_eval_path = os.path.join(base_path, "eval", data_directory, f"{file_name_without_ext}_eval.json")

    os.makedirs(os.path.dirname(output_train_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_eval_path), exist_ok=True)

    with open(output_train_path, 'w', encoding='utf-8') as train_file:
        for item in train_data:
            train_file.write(json.dumps(item, ensure_ascii=False) + '\n')

    with open(output_eval_path, 'w', encoding='utf-8') as eval_file:
        for item in eval_data:
            eval_file.write(json.dumps(item, ensure_ascii=False) + '\n')
            
    print(f"Training data created and saved to {output_train_path}")
    print(f"Evaluation data created and saved to {output_eval_path}")

if __name__ == "__main__":
    corrected_file_path = ""
    while True:
        try:
            corrected_file_path_idx = int(input("Enter the idx (1=Bali, 2=Minang, 3=Sunda, 4=Jawa): "))
            dataset_type_idx = int(input("Enter the type (1=dic_word, 2=dic_phrase):"))
            if (corrected_file_path_idx == 1 and (dataset_type_idx == 1 or dataset_type_idx == 2)):
                col_id = 0
                if dataset_type_idx == 1:
                    dataset_type = "Bali/data/dic-word/bali-indo_entries.xlsx"
                else:
                    dataset_type = "Bali/data/dic-phrase/bali-indo_phrases.xlsx"
                break
            elif  (corrected_file_path_idx == 2 and (dataset_type_idx == 1 or dataset_type_idx == 2)):
                col_id = 0
                if dataset_type_idx == 1:
                    dataset_type = "Minang/data/dic-word/minang-indo_entries.xlsx"
                else:
                    dataset_type = "Minang/data/dic-phrase/minang-indo_phrases.xlsx"
                break
            elif  (corrected_file_path_idx == 3 and (dataset_type_idx == 1 or dataset_type_idx == 2)):
                col_id = 0
                if dataset_type_idx == 1:
                    dataset_type = "Sunda/data/dic-word/sunda-indo_entries.xlsx"
                else:
                    dataset_type = "Sunda/data/dic-phrase/sunda-indo_phrases.xlsx"
                break
            elif  (corrected_file_path_idx == 4 and (dataset_type_idx == 1 or dataset_type_idx == 2)):
                col_id = 1
                if dataset_type_idx == 1:
                    dataset_type = "Jawa/data/dic-word/java-indo_entries.xlsx"
                else:
                    dataset_type = "Jawa/data/dic-phrase/java-indo_phrases.xlsx"
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    train_ratio = 0.8

    create_dataset(dataset_type, train_ratio, col_id)
