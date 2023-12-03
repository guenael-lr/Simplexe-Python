from Modele import *
from Simplexe import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python main.py path_to_model_file")
    else:
        modele = Modele()
        modele.loadFromFile(sys.argv[1])
        modele.print()
        simplexe = Simplexe(modele)
        simplexe.optimisation()