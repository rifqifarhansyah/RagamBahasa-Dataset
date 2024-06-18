import json
import os

def process_language(lang_code, lang_short, input_path):
    output_directory = f"{lang_code}/data/wiki/{lang_short}-wikipedia-filtering"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    all_text = ""
    for filename in os.listdir(input_path):
        if filename.endswith(".json"):
            json_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(output_directory, f"{lang_short}-wikipedia-filtering" + ".txt")

            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                for line in json_file:
                    try:
                        data = json.loads(line.strip())
                        title = data.get('title', '')
                        text = data.get('text', '')
                        all_text += title + '. ' + text + '. '
                    except json.JSONDecodeError:
                        print(f"Error parsing JSON in file: {json_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(all_text.strip())

    print(f"Output file saved to: {output_file_path}")
    return
        

if __name__ == "__main__":
    while True:
        try:
            lang_id = int(input("Enter the idx (1=Bali, 2=Minang, 3=Sunda, 4=Jawa): "))
            lang_code = ""
            lang_short = ""
            input_path = ""
            if lang_id == 1:
                lang_code = 'Bali'
                lang_short = "ban"
                input_path = "Bali/data/wiki/ban-wikipedia-unfiltering"
            elif lang_id == 2:
                lang_code = 'Jawa'
                lang_short = "jv"
                input_path = "Jawa/data/wiki/jv-wikipedia-unfiltering"
            elif lang_id == 3:
                lang_code = 'Minang'
                lang_short = "min"
                input_path = "Minang/data/wiki/min-wikipedia-unfiltering"
            elif lang_id == 4:
                lang_code = 'Sunda'
                lang_short = "su"
                input_path = "Sunda/data/wiki/su-wikipedia-unfiltering"
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        print("tes")
        process_language(lang_code, lang_short, input_path)
