from Modele import *
import numpy as np

class Simplexe:
    def __init__(self, modele):
        self.tableau = modele.a
        self.coefficient = [0.0 for _ in modele.c]
        self.coefficientPhase2 = modele.c
        self.bj = modele.b
        self.base = []
        self.n = modele.n + modele.m
        self.m = modele.m
        self.zi = [0.0 for _ in range(self.n)]
        self.sens = modele.sens
        self.besoinPhase1 = False

        if not modele.maximisation:
            self.coefficientPhase2 = [-1.0 * i for i in modele.c]
            self.bj = [-1.0 * i for i in modele.b]

        self.coefficientPhase2.extend([0.0 for _ in range(modele.m)])
        self.coefficient.extend([0.0 for _ in range(modele.m)])
        self.base.extend([modele.n + i + 1 for i in range(modele.m)])  

        nb_Artificielle = 0
        for i in range(modele.m):
            for j in range(modele.m):
                self.tableau[j].append(0.0 if i!=j else 1.0 * (-1 if self.sens[i] else 1))

        for i in range(modele.m):
            if self.sens[i]:
                self.besoinPhase1 = True
                self.coefficient.append(-1.0)
                for j in range(modele.m):
                    self.tableau[j].append(0.0 if i!=j else 1.0)
                self.n += 1
                self.zi.append(0.0)
                self.base[i] = modele.n + modele.m + 1 + nb_Artificielle
                nb_Artificielle += 1

        #calculer zi
        self.zi = [0.0 for i in range(self.n)]
        self.cizi = [0.0 for i in range(self.n)]
        if(self.besoinPhase1):
            for j in range(self.n):
                for i in range(self.m):
                    self.zi[j] +=  self.coefficient[self.base[i] - 1] * self.tableau[i][j]
                    self.cizi[j] = self.coefficient[j] - self.zi[j]
        else:
            self.coefficient = self.coefficientPhase2
            for j in range(self.n):
                for i in range(self.m):
                    self.zi[j] +=  self.base[i] * self.tableau[i][j]
                    self.cizi[j] = self.coefficient[j] - self.zi[j]
        #calculer ci-zi 


    def iteration(self, pivot):
        #set les colonnes de la base à 0 et 1 sur les lignes qui correspondent
        pivotValue = self.tableau[pivot[0]][pivot[1]]

        #les autres cases sont egales à la valeur de la case - la valeur de la case de la ligne du pivot * la valeur de la case de la colonne du pivot / la valeur du pivot
        for i in range(self.m):
            for j in range(self.n):
                if i!=pivot[0] and j!=pivot[1]:
                    self.tableau[i][j] -= self.tableau[i][pivot[1]] * self.tableau[pivot[0]][j] / pivotValue
            if i!=pivot[0]:
                self.bj[i] -= self.tableau[i][pivot[1]] * self.bj[pivot[0]] / pivotValue
        
        self.tableau[pivot[0]] = [i / pivotValue for i in self.tableau[pivot[0]]]
        self.bj[pivot[0]] /= pivotValue

        #met la colonne du pivot à 0 sauf la case du pivot
        for i in range(self.m):
            if i!=pivot[0]:
                self.tableau[i][pivot[1]] = 0.0

        
        self.zi = [0.0 for i in range(self.n)]
        for j in range(self.n):
            for i in range(self.m):
                self.zi[j] +=  self.coefficient[self.base[i]-1] * self.tableau[i][j]
            self.cizi[j] = self.coefficient[j] - self.zi[j]
        self.print()


    def optimisation(self):
        if self.besoinPhase1:
            self.premierePhase()
        self.print()
        while(self.cizi[np.argmax(self.cizi)] > 0):
            
            #trouver la plus grande valeur de ci-zi
            colonnePivot = np.argmax(self.cizi)     

            #trouver la plus petite valeur de chaque ligne sur la colonne du pivot divisé par la valeur de bj
            lignePivot = np.argmin([(self.bj[i]/self.tableau[i][colonnePivot] if self.tableau[i][colonnePivot] > 0 else float('inf')  ) for i in range(self.m)])
            #remove the 0 from the list
            print(lignePivot)
            #mettre à jour la base
            print("pivot : " + str(lignePivot) + " " + str(colonnePivot))
            self.base[lignePivot] = colonnePivot + 1
            self.iteration([lignePivot, colonnePivot])
        
        print("La solution optimale est :")
        for i in range(self.m):
            print("x" + str(self.base[i]) + " = " + str(self.bj[i]))
        print("z = " + str(np.sum(self.zi)))


    def print(self):
        print("\n     Ci :    |", end=" ")
        for i in self.coefficient:
            print(i, end=" ")

        print("\nCoeff | Base ", end="")
        for i in range(self.n):
            print("| x" + str(i+1), end=" ")
        print("| bj")

        for i in range(self.m):
            print("\n  " + str(self.coefficient[self.base[i]-1]) + " | B" + str(self.base[i]) +"   | " + str(self.tableau[i]) + " | " + str(self.bj[i]), end="")
        
        print("\n      z      | ", end="")
        
        for j in range(self.n):
            print(" " + str(self.zi[j]), end=" ")

        print(" | ", np.sum(self.bj[i] * self.coefficient[self.base[i]-1] for i in range(self.m)), end=" ")
        print("\n   ci - zi   | ", end="")
        for i in self.cizi:
            print(" " + str(i) , end=" ")
        print("\n\n")

    def premierePhase(self):
        self.print()

        while(self.cizi[np.argmax(self.cizi)] > 0):
            colonnePivot = np.argmax(self.cizi) 
            lignePivot = np.argmin([(self.bj[i]/self.tableau[i][colonnePivot] if self.tableau[i][colonnePivot] else float('inf')) for i in range(self.m)])
            self.base[lignePivot] = colonnePivot + 1
            self.iteration([lignePivot, colonnePivot])
            #self.print()
            #input()

        self.n = self.n - self.sens.count(True)
        self.coefficient = self.coefficientPhase2[:self.n]
        self.tableau = [self.tableau[i][:self.n] for i in range(self.m)]
        #calculer zi et cizi 
        self.zi = [0.0 for i in range(self.n)]
        self.cizi = [0.0 for i in range(self.n)]
        for j in range(self.n):
            for i in range(self.m):
                self.zi[j] +=  self.coefficient[self.base[i]-1] * self.tableau[i][j]
            self.cizi[j] = self.coefficient[j] - self.zi[j]

        print("Fin de la phase 1")