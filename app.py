from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Define the questions and choices
questions = [
    "How did you hear about us?",
    "How satisfied are you with our customer service?",
    "How likely are you to recommend us to a friend?",
    "Overall, how would you rate your experience with us?"
]

choices = [
    ["Online ad", "Social media", "Word of mouth", "Other"],
    ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"],
    ["Very likely", "Likely", "Neutral", "Unlikely", "Very unlikely"],
    ["Excellent", "Good", "Neutral", "Poor", "Terrible"]
]

# Define the root route
@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        session['responses'] = []
        return redirect(url_for('index'))
    return render_template('start.html')

# Define the index route
@app.route('/index')
def index():
    survey_title = "Customer Satisfaction Survey"
    survey_instructions = "Please fill out a survey about your experience with us."
    return render_template('index.html', title=survey_title, instructions=survey_instructions)

# Define the question route
@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if 'responses' not in session:
        return redirect(url_for('start'))

    if question_id != len(session['responses']):
        flash('Invalid question!')
        return redirect(url_for('question', question_id=len(session['responses'])))

    # generate a random token
    csrf_token = secrets.token_hex(16)
    # store the token in the session
    session['csrf_token'] = csrf_token

    if request.method == 'POST':
        response = request.form['response']
        session['responses'].append(response)

        if len(session['responses']) == len(questions):
            return redirect(url_for('thankyou'))
        else:
            return redirect(url_for('question', question_id=len(session['responses'])))

    question = questions[question_id]
    choices_for_question = choices[question_id]
    return render_template('question.html', question=question, choices=choices_for_question, question_id=question_id, csrf_token=csrf_token)


# Define the thank you route
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
    print(session) # Print session variable to console


if __name__ == '__main__':
    app.run(debug=True)
