from flask import Flask, render_template, request, jsonify
from utils import summarize_from_url, get_article_text, summarize_from_pdf, generate_answer

app = Flask(__name__)

conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['user_input2']
    if url.endswith(".pdf"):
        result = summarize_from_pdf(url)
    else:
        result = summarize_from_url(url)
    return result

@app.route('/query', methods=['POST'])
def query():
    global conversation_history
    user_question = request.form['user_input3']  # Get the user's question from the form
    article_url = request.form['user_input2']  # Get the article URL from the form

    conversation_history.append({"role": "user", "message": user_question})

    article_text = get_article_text(article_url)

    if article_text is None:
        return "Failed to retrieve article text."

    answer = generate_answer(user_question, article_text, conversation_history)
    conversation_history.append({"role": "system", "message": answer})

    return jsonify(conversation_history)

@app.route('/refresh', methods=['POST'])
def refresh():
    global conversation_history
    conversation_history.clear()
    return ('', 204)  # Return an empty response with a status code 204 (No Content)

if __name__ == '__main__':
    app.run()