# FOUILLE

## Dépendances 

Les modules suivants doivent être installés au préalable :

* anytree
* nltk
* num2words

Puis exécuter les commandes ci-dessous dans la console (ou terminal, intepréteur de commandes..) :
 ```python
 nltk.download()
 nltk.download('stopwords')
 nltk.download('punkt')
```

N.B. : Il est possible d'avoir une erreur "SSL : Certificate verify failed" lors de l'éxécution des commandes susmentionnées, dans ce cas, nous vous renvoyons vers les liens suivants :
https://github.com/nltk/nltk/issues/2029 et https://bugs.python.org/issue28150

## Jeu de données

Nous appuyons nos tests sur une version modifiée du corpus de résumés de film disponible [ici](http://www.cs.cmu.edu/~ark/personas/)


Chaque résumé de film a été fusionné avec ses informations (comme l'idenfitiant du film, son titre, etc) et inséré dans une base de donnée SQL pour accélérer le recherche d'un film par son identifiant.

D'autres part, les résumés de films, étant issus de la base *Wikipedia*, contiennent des marqueurs qui ont dû être supprimés dans notre base de données. Il s'avère également que certains résumés ne comporte aucune information sur le film en lui même (seulement la distribution des rôles par exemple); sur ce point ne nous pas jugé utile de les modifier étant donnée la charge de travail necéssaire.

Finnalement, certains résumés de film n'ont pas de correspondances dans la base de données originales. En d'autres mots, il est impossible de rélier certains résumés à des films. Ces derniers n'ont donc pas été ajoutés à notre base de données. C'est le cas des résumés dont l'identifiant est :

```
2862137 - 33334420 - 16758721 - 23217064 - 2746943 - 26541865 - 35760160 - 33353596 - 20736730 - 33222661 - 22172813 - 3949692 - 31723265 - 1857955 - 21859037 - 10083650 - 13255982 - 4136530 - 7483495 - 3196252 - 29528984 - 25903651 - 10873999 - 9553464 - 32396789 - 12651534 - 28278467 - 21366668 - 31642366 - 16803295 - 18771923 - 25054414 - 27905296 - 29345692 - 22277628 - 8249681 - 33401605 - 9286652 - 27108314 - 4795131 - 24082320 - 30339234 - 34176513 - 18142186 - 23832810 - 845974 - 32583077 - 31033813 - 26638643 - 36080533 - 18491946 - 21075859 - 33743875 - 18503404 - 34561181 - 761788 - 33891030 - 14481527 - 23103066 - 2849218 - 33335392 - 33507904 - 34098133 - 28692407 - 24158389 - 23880 - 10153756 - 25095660 - 4749539 - 9264334 - 24044720 - 927401 - 30045041 - 20841547 - 26591591 - 2405253 - 30212553 - 29529427 - 28291797 - 26163584 - 32293582 - 18993404 - 21724488 - 8152043 - 18557380 - 31025139 - 22415226 - 32920723 - 17228796 - 491329 - 14851642 - 34187700 - 3791628 - 26294680 - 35607003 - 32942181 - 133671 - 34076714 - 8030673
```


