import os
import nltk
import re
from collections import defaultdict
from nltk.stem import PorterStemmer

nltk.download('punkt')

def load_stopwords(stopword_file):
    with open(stopword_file, 'r') as f:
        return set(f.read().splitlines())

def preprocess_text(text, stopwords):
    ps = PorterStemmer()
    tokens = nltk.word_tokenize(text.lower())
    return [ps.stem(word) for word in tokens if word.isalpha() and word not in stopwords]

def build_indexes(abstracts_folder, stopwords):
    from collections import defaultdict

    inverted_index = defaultdict(set)  
    positional_index = defaultdict(lambda: defaultdict(list))  

    for doc_id, filename in enumerate(sorted(os.listdir(abstracts_folder))):
        file_path = os.path.join(abstracts_folder, filename)

        try:
            with open(file_path, 'r', encoding='ISO-8859-1', errors="ignore") as file:
                text = file.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue  # Skip problematic files

        words = preprocess_text(text, stopwords)  # Make sure this is indented properly

        for pos, word in enumerate(words):
            inverted_index[word].add(doc_id)
            positional_index[word][doc_id].append(pos)

    return inverted_index, positional_index


def boolean_query_processing(query, inverted_index, total_docs):
    query = query.lower().split()
    result_docs = set(range(total_docs))
    operator = None
    current_set = set()

    for term in query:
        if term in {"and", "or", "not"}:
            operator = term
        else:
            term_docs = inverted_index.get(term, set())
            if operator == "not":
                term_docs = result_docs - term_docs
            elif operator == "or":
                current_set |= term_docs
            elif operator == "and":
                current_set &= term_docs
            else:
                current_set = term_docs
    
    return sorted(current_set)

def main():
    stopwords = load_stopwords(r"C:\Users\ehtis\Downloads\Boolean_Retrieval_Model_Complete\data\Stopword-List.txt")
    abstracts_folder = r"C:\Users\ehtis\Downloads\Boolean_Retrieval_Model_Complete\data\Abstracts"
    inverted_index, positional_index = build_indexes(abstracts_folder, stopwords)
    total_docs = len(os.listdir(abstracts_folder))

    while True:
        query = input("\nEnter Boolean Query (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break

        results = boolean_query_processing(query, inverted_index, total_docs)
        print("Relevant Documents:", results)

if __name__ == "__main__":
    main()
