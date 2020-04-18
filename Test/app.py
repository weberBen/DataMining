from flask import Flask
from flask import request
from flask import render_template
import environment as Env
import sys, os
#import Frequency.SummaryWordFrequency as Freq
#from nltk.stem.porter import *
from querySystem.matrixOp import *
import time



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text']
    processed_text = text.upper()
    tmp=recherche(processed_text)
    print(tmp)

    return render_template("resultat.html" , message = tmp )


def recherche(input):
    info = Env.Info()
    env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
    database = env_obj.Database
    wordsBag = env_obj.WordsBag
    Freq = env_obj.Frequency
    matrix = "matrix_"+"all"
    r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
    r.load(matrix)

    response = r.search(input, 1)
    res = response.results
    movie_id, score  = res[0]
    movie = database.getMovie(movie_id)
    print("\ntitre du film\n"+movie.title)
    return movie.title


if __name__ == '__main__':
    app.run()