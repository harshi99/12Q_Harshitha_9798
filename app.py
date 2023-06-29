from flask import Flask, render_template, request
import re

app = Flask(__name__)

def remove_word(text, word):
    pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
    return pattern.sub('', text)

def find_words(text, word1, word2):
    pattern = re.compile(r'(\b{}\b\s+\b{}\b|\b{}\b\s+\b{}\b)'.format(re.escape(word1), re.escape(word2), re.escape(word2), re.escape(word1)), re.IGNORECASE)
    return pattern.findall(text)

def process_text(text, option, word=None, word1=None, word2=None):
    if option == 'RM':
        modified_text = remove_word(text, word)
    elif option == 'F':
        occurrences = find_words(text, word1, word2)
        modified_text = highlight_words(text, occurrences)
    else:
        modified_text = text
    return modified_text

def highlight_words(text, occurrences):
    for occurrence in occurrences:
        text = text.replace(occurrence, '<span class="highlight">{}</span>'.format(occurrence))
    return text

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        option = request.form['option']
        if option == 'RM':
            word = request.form['single_word']
            modified_text = process_text(text, option, word=word)
        elif option == 'F':
            word1 = request.form['word1']
            word2 = request.form['word2']
            modified_text = process_text(text, option, word1=word1, word2=word2)
        else:
            modified_text = text
        return render_template('index.html', modified_text=modified_text, text=text)
    return render_template('index.html', modified_text=None)

if __name__ == '__main__':
    app.run()
