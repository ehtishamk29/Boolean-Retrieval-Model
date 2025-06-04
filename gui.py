import os
import tkinter as tk
from tkinter import messagebox
from main import load_stopwords, build_indexes, boolean_query_processing

class BooleanRetrievalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Boolean Retrieval Model")

        self.label = tk.Label(root, text="Enter Boolean Query:")
        self.label.pack()

        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.process_query)
        self.search_button.pack()

        self.result_label = tk.Label(root, text="Results:")
        self.result_label.pack()

        self.results_box = tk.Text(root, height=10, width=50)
        self.results_box.pack()

        self.stopwords = load_stopwords(r"C:\Users\ehtis\Downloads\Boolean_Retrieval_Model_Complete\data\Stopword-List.txt")
        self.abstracts_folder = r"C:\Users\ehtis\Downloads\Boolean_Retrieval_Model_Complete\data\Abstracts"

        self.inverted_index, _ = build_indexes(self.abstracts_folder, self.stopwords)
        self.total_docs = len(os.listdir(self.abstracts_folder))

    def process_query(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showerror("Error", "Query cannot be empty!")
            return

        results = boolean_query_processing(query, self.inverted_index, self.total_docs)
        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, f"Relevant Documents: {results}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BooleanRetrievalGUI(root)
    root.mainloop()
