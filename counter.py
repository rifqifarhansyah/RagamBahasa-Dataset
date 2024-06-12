import csv

def count_words(text):
    words = text.split()
    word_counts = {}
    length = len(words)
    for word in words:
        word = word.strip(".,!?").lower()
        word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts, length

def main():
    filename1 = "./dictionary/jv-dictionary-output-txt/jav_column_values.txt"
    filename2 = "./wikipedia-dump/jv-wikipedia-output-txt/wiki_07.txt"

    try:
        with open(filename1, 'r', encoding='utf-8') as file1:
            text1 = file1.read()
    except FileNotFoundError:
        print(f"File not found: {filename1}")
        return

    try:
        with open(filename2, 'r', encoding='utf-8') as file2:
            text2 = file2.read()
    except FileNotFoundError:
        print(f"File not found: {filename2}")
        return

    word_counts1, file1Length = count_words(text1)
    print(f"Dictionary Word Count\t: {file1Length}")
    word_counts2, file2Length = count_words(text2)
    print(f"Wikipedia Word Count\t: {file2Length}")

    with open('word_counts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Word', 'dictionary', 'wikipedia']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for word in set(word_counts1) | set(word_counts2):
            writer.writerow({'Word': word, 'dictionary': word_counts1.get(word, 0), 'wikipedia': word_counts2.get(word, 0)})

    print("Word counts written to word_counts.csv")

if __name__ == "__main__":
    main()