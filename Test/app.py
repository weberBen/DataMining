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
    processed_text = text.upper()
    tmp=recherche(processed_text,ma)
    print(tmp)
    Pokemons =["Pikachu", "Charizard", "Squirtle", "Jigglypuff",  
           "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"] 
  

    return render_template("resultat.html" , len = len(tmp), tmp = tmp )


def recherche(input,ma):
    L=[]
    info = Env.Info()
    env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
    database = env_obj.Database
    wordsBag = env_obj.WordsBag
    Freq = env_obj.Frequency
    matrix = ma
    r = Request(database, wordsBag, Freq, env_obj.getMatrixFolder())
    r.load(matrix)

    response = r.search(input, 10)
    res = response.results
    if len(res)==0:
            return("None","0")
            

    for movie_id, score in res:
        movie = database.getMovie(movie_id)
        L.append((movie.title,round(score,2)))

            
    movie_id, score  = res[0]
    movie = database.getMovie(movie_id)
    print("\ntitre du film\n"+movie.title)

    return L

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()