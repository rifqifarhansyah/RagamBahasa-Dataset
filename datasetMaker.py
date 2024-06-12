import random
import pandas as pd
import os
import json
from itertools import product

def scramble_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def generate_uncorrected_text(corrected_text):
    def get_substitution_combinations(word, i, j):
        substitutions = {
            'o': '0', 'O': '0', 's': '5', 'S': '5', 'g': '9', 'G': '9', 
            'A': '4', 'z': '2', 'Z': '2', 'l': '1', 'I': '1', 'B': '8', 
            'e': 'c', 'a': 'o', 'E': 'C', 'u': 'v', 'm': 'rn', 'rn': 'm'
        }

        if i == j:
            if word[i] in substitutions:
                substituted_word = word[:i] + substitutions[word[i]] + word[i+1:]
            else:
                substituted_word = word[:i] + " " + word[i+1:]
            return [substituted_word]

        if word[i] in substitutions:
            if word[j] in substitutions:
                substituted_word = (
                    word[:i] + substitutions[word[i]] + word[i + 1:j] + substitutions[word[j]] + word[j + 1:]
                )
            else:
                substituted_word = word[:i] + substitutions[word[i]] + word[i + 1:]
            return [substituted_word]
        else:
            if word[j] in substitutions:
                substituted_word = word[:i] + " " + word[i + 1:j] + substitutions[word[j]] + word[j + 1:]
            else:
                substituted_word = word[:i] + " " + word[i + 1:j] + " " + word[j + 1:]
            return [substituted_word]

    a = 0
    text = []
    for word in corrected_text.split():
        for i in range(len(word)):
            for j in range(i, len(word)):
                uncorrected_words = get_substitution_combinations(word, i, j)
                text.extend(uncorrected_words)
    text = "{{--}}".join(text)
    return text

def create_dataset(corrected_file_path, train_ratio):
    df = pd.read_excel(corrected_file_path)
    corrected_text = ' '.join(df.iloc[:, 0].dropna().astype(str).tolist())

    dataset = []
    for line in corrected_text.split(' '):
        corrected_word = line.strip()
        combinations = generate_uncorrected_text(corrected_word).split('{{--}}')
        for combination in combinations:
            pair = {"input": combination, "output": corrected_word}
            dataset.append(pair)

    random.shuffle(dataset)

    num_samples = len(dataset)
    num_train_samples = int(num_samples * train_ratio)
    train_data = dataset[:num_train_samples]
    eval_data = dataset[num_train_samples:]

    base_path, file_name = os.path.split(corrected_file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    output_train_path = os.path.join(base_path, "train", f"{file_name_without_ext}_train.json")
    output_eval_path = os.path.join(base_path, "eval", f"{file_name_without_ext}_eval.json")

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
            corrected_file_path_idx = int(input("Enter the idx (1=Bali, 2=Minang, 3=Sunda): "))
            if corrected_file_path_idx == 1:
                corrected_file_path = "Bali/data/bali-indo_entries.xlsx"
                break
            elif corrected_file_path_idx == 2:
                corrected_file_path = "Minang/data/minang-indo_entries.xlsx"
                break
            elif corrected_file_path_idx == 3:
                corrected_file_path = "Sunda/data/sunda-indo_entries.xlsx"
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    train_ratio = 0.8

    create_dataset(corrected_file_path, train_ratio)
