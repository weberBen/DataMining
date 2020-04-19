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
    ma = request.form["matrice"]
    mode = request.form["contact"]
    processed_text = text.upper()
    tmp=recherche(processed_text, ma, mode)
    print(tmp)
    return render_template("resultat.html" , len = len(tmp), tmp = tmp )


def recherche(input,ma,mode):
    L=[]
    info = Env.Info()
    env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
    database = env_obj.Database
    wordsBag = env_obj.WordsBag
    Freq = env_obj.Frequency
    matrix = ma
    r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
    if mode==1:
        r.load(matrix,k=400)
        response = r.searchSVD(input, 10)
    else:
        r.load(matrix)
        response = r.search(input, 10)
    res = response.results
    if len(res)==0:
            return("None","0")

    for movie_id, score in res:
        movie = database.getMovie(movie_id)
        L.append((movie.title,round(score,4)))

    return L

@app.route('/about')
def about():
    return render_template("about.html")

            
if __name__ == '__main__':
    app.run()