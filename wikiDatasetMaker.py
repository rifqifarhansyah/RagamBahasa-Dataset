import random
import pandas as pd
import os
import json

substitutions = {
    'o': '0', 'O': '0', 's': '5', 'S': '5', 'g': '9', 'G': '9', 
    'A': '4', 'z': '2', 'Z': '2', 'l': '1', 'I': '1', 'B': '8', 
    'e': 'c', 'a': 'o', 'E': 'C', 'u': 'v', 'm': 'rn', 'rn': 'm',
}

def mask_character(char):
    random_choice = random.random()
    if random_choice < 0.80 and char in substitutions:
        return substitutions[char]
    elif random_choice < 0.90:
        return random.choice([' '] + list(chr(i) for i in range(65, 91)) + list(chr(i) for i in range(97, 123)))
    else:
        return char

def generate_variations(word):
    variations = set()
    word_length = len(word)
    
    for i in range(word_length):
        if random.random() < 0.85:
            variation = list(word)
            variation[i] = mask_character(word[i])
            variations.add(''.join(variation))
    
    if len(word) > 1 and random.random() < 0.4 and '-' not in word:
        split_index = random.randint(1, len(word) - 1)
        hyphenated_word = word[:split_index] + "-\n" + word[split_index:]
        variations.add(hyphenated_word)
            
    if '-' in word and random.random() < 0.4:
        variations.add(word.replace('-', '-\n'))

    return list(variations)

def create_dataset_from_txt(input_dir, train_ratio):
    dataset = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(input_dir, filename)
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                lines = txt_file.readlines()
                corrected_texts = [line.strip() for line in lines if line.strip()]

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

    output_train_path = os.path.join(input_dir, "train.json")
    output_eval_path = os.path.join(input_dir, "eval.json")

    with open(output_train_path, 'w', encoding='utf-8') as train_file:
        for item in train_data:
            train_file.write(json.dumps(item, ensure_ascii=False) + '\n')

    with open(output_eval_path, 'w', encoding='utf-8') as eval_file:
        for item in eval_data:
            eval_file.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"Training data created and saved to {output_train_path}")
    print(f"Evaluation data created and saved to {output_eval_path}")

if __name__ == "__main__":
    while True:
        try:
            lang_id = int(input("Enter the idx (1=Bali, 2=Minang, 3=Sunda, 4=Jawa): "))
            if lang_id == 1:
                input_dir = "Bali/data/wiki/ban-wikipedia-filtering"
            elif lang_id == 2:
                input_dir = "Jawa/data/wiki/jv-wikipedia-filtering"
            elif lang_id == 3:
                input_dir = "Minang/data/wiki/min-wikipedia-filtering"
            elif lang_id == 4:
                input_dir = "Sunda/data/wiki/su-wikipedia-filtering"
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                continue
            
            train_ratio = 0.8
            create_dataset_from_txt(input_dir, train_ratio)
            break
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
