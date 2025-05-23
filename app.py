from flask import Flask, render_template, request
import os
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

app = Flask(__name__)
global Classifier
global Vectorizer

# Load data
data = pandas.read_csv('spam.csv', encoding='latin-1')
train_data = data[:4400]
test_data = data[4400:]

# Train model
Classifier = OneVsRestClassifier(SVC(kernel='linear', probability=True))
Vectorizer = TfidfVectorizer()
vectorize_text = Vectorizer.fit_transform(train_data.v2)
Classifier.fit(vectorize_text, train_data.v1)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    prediction = ''
    probability = ''
    error = ''

    if request.method == 'POST':
        message = request.form.get('message', '')
        try:
            vectorize_message = Vectorizer.transform([message])
            prediction = Classifier.predict(vectorize_message)[0]
            probability = Classifier.predict_proba(vectorize_message).tolist()[0]
            probability = [round(p * 100, 2) for p in probability]
            return render_template('index.html', message=message, prediction=prediction, probability=probability)
        except Exception as e:
            error = str(e)
            return render_template('index.html', message=message, error=error)

    return render_template('index.html', message='', prediction='', probability='', error='')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
