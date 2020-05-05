from flask import Flask, request, render_template
import environment as Env
import sys, os
from querySystem.matrixOp import *


info = Env.Info()
env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
database = env_obj.Database
wordsBag = env_obj.WordsBag
Freq = env_obj.Frequency
r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())

app = Flask(__name__)

@app.route('/')

def home():

    return render_template("home.html")

@app.route('/', methods=['GET','POST'])
def text_box():

    text = request.form['text']
    matrice = request.form["matrice"]
    mode = request.form["mode"]
    res=recherche(text, matrice, mode)
    return render_template("resultat.html" , number_res = len(res), tmp = res , search=text )

def recherche(input, matrix, mode):
    L=[]

    if mode=="1":
        r.load(matrix,k=400)
        response = r.searchSVD(input, 10)
    else:
        r.load(matrix,k=6)
        response = r.search(input, 10)
    res = response.results
    if len(res)==0:
            return [("None",0,"None")]
    for movie_id, score in res:
        movie = database.getMovie(movie_id)
        L.append((movie.title, round(score,4), movie.summary, movie_id))
    return L

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/<movie_id>')
def result_focused(movie_id):
    movie = database.getMovie(int(movie_id))

    return render_template("result_focused.html",movie=(movie.title, movie_id, movie.summary))

if __name__ == '__main__':
    app.run()