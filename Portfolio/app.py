from flask import Flask, render_template, jsonify

app = Flask(__name__)

PROJECTS = [
    {
        "id":1,
        "title":'FlaskCRUD ',
        'content': "Simple Website Using Flask",
    },
     {
        "id":2,
        "title":'Medicine Recommendation System',
        'content': "Healthcare Website Using Flask and Machine Learning",
    },
    {
        "id":3,
        "title":'Streamlit and Machine Learning',
        'content': "Classification and Analysis of Different Datasets Using Streamlit and Machine Learning",
    },
     {
        "id":4,
        "title":'Software Developer Salary Prediction ',
        'content': "Software Developer Salary Prediction Using Flask and Machine Learning",
    },

]

@app.route('/')
def home():
    return render_template("home.html",projects=PROJECTS)




if __name__ == "__main__":
    app.run(debug=True)