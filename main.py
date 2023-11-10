import tkinter as tk
from tkinter import ttk
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



user_input = ""


def add_search_term():
    global user_input
    term = entry.get()
    if user_input:
        user_input += " " + term
    else:
        user_input = term
    entry.delete(0, tk.END)
    result_text.insert(tk.END, term + " ")


def detect_stop_words(text):
    # Get the list of stop words

    stop_words = set(stopwords.words('portuguese'))

    # Tokenize the text into individual words
    words = word_tokenize(text)

    # Detect stop words
    detected_stop_words = [word for word in words if word.lower() not in stop_words]

    return detected_stop_words


def clear_results():
    result_text.delete("1.0", tk.END)


def search(event=None):
    global user_input
    query = entry.get().lower()
    word_count = len(query.split())  # Count the number of terms
    if user_input:
        query += " " + user_input
    user_input = ""
    folder_path = r'E:\Projects\trabalho_Ori'
    matching_results = []
    partial_results = []

    if query == "":
        result_text.insert(tk.END, "Nada foi inserido")
        return 0

    detected_stop_words = detect_stop_words(query)
    query_words = detected_stop_words  # Tokenize the query into individual words
    num_search_terms = len(query_words)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".html", ".htm")):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='ISO-8859-1') as f:
                    content = f.read().lower()
                    non_stop_words = detect_stop_words(content)
                    occurrences = {word: non_stop_words.count(word) for word in query_words}
                    total_occurrences = sum(occurrences.values())
                    if total_occurrences > 0:
                        if set(query_words).issubset(set(occurrences.keys())):
                            weight = 1
                            for term, count in occurrences.items():
                                weight *= count if count > 0 else 0.01

                            matching_results.append((file_path, occurrences, total_occurrences, weight))
                        else:
                            partial_results.append((file_path, occurrences, total_occurrences))

    clear_results()

    sorted_results = sorted(matching_results, key=lambda x: x[3], reverse=True) + sorted(partial_results, key=lambda x: (len(x[1]), x[2]), reverse=True)

    if sorted_results:
        result_text.insert(tk.END, f"Você pesquisou {word_count} term(s): {query}\nExibindo arquivos recuperados:\n")
        for index, (file_path, occurrences, total_occurrences, weight) in enumerate(sorted_results, start=1):
            result_text.insert(tk.END, f"Arquivo {index}: {file_path}\n")
            result_text.insert(tk.END, f"Total de ocorrências no arquivo: {total_occurrences}\n")
            result_text.insert(tk.END, f"Peso: {weight}\n")
            result_text.insert(tk.END, "Termos encontrados:\n")
            for term, count in occurrences.items():
                result_text.insert(tk.END, f"- {term}: {count} vezes\n")
            result_text.insert(tk.END, "\n")
    else:
        result_text.insert(tk.END, "No matches found for the specified word in the HTML files.")

    entry.delete(0, tk.END)

root = tk.Tk()
root.title("File Searcher")

# Configure the root window size
window_width = 700
window_height = 560
root.geometry(f"{window_width}x{window_height}")
root.minsize(window_width, window_height)
root.maxsize(window_width, window_height)


# Disable window resizing
root.resizable(False, False)

# Set colors
primary_color = "#4285F4"  # Google Blue
secondary_color = "#ffffff"  # White

# Create a custom font for the widgets
font_style = ("Arial", 20)


# Create the search entry field
entry = ttk.Entry(root, width=60)
entry_label_text = "File searcher"
entry_label = tk.Label(root, text=entry_label_text, font=font_style, foreground="black",bg="lightsteelblue")
entry_label.pack()
entry.pack(pady=20)


# Create the search button
search_button = tk.Button(root, text="Pesquisar", height=2, width=20)
search_button.configure(background="cornflowerblue", highlightcolor="blue")  # Set the background color indirectly
search_button.configure(command=search)  # Set the command for the button
search_button.pack()

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack()



# Bind the <Return> event to the search function
entry.bind("<Return>", search)

# Create a text widget to display the search results
result_text = tk.Text(root, font=font_style, bg=secondary_color, height=10)
result_text.configure(bg="lightsteelblue")
result_text.pack(fill=tk.BOTH, padx=20, pady=20)


# Configure the root window background color
root.configure(bg=secondary_color)
root.configure(background="lightsteelblue")

root.mainloop()