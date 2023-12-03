class Modele:
    def __init__(self):
        self.maximisation = False #sens de l'objectif
        self.n = 0 #nombre de variables
        self.m = 0 #nombre de contraintes
        self.c = [] #pour chaque variable X_i, le coefficient dans l'objectif c_i
        self.a = [] #pour chaque contrainte j et chaque variable X_i, le coefficient de X_i dans j a[j][i]
        self.b = [] #pour chaque contrainte j, la constante à droite de l'inégalité
        self.sens = [] #pour chaque contrainte j, le sens de la contrainte (Vrai si >=, Faux si <=)

    def loadFromFile(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()

        #récupération de la taille de l'instance
        print(lines[0])
        print(lines[1])
        self.n, self.m = int(lines[0].split()[0]), int(lines[0].split()[1])
        #lecture de l'objectif
        ligne = lines[1].split()
        self.maximisation = ligne[0].lower()=="max"

        for i in range(0, self.n):
            self.c.append(0.)
        k = 1
        if ligne[1]!="-":
            try:
                self.c[int(ligne[k + 1][1:]) - 1] = float(ligne[k])
                k = 3
            except:
                self.c[int(ligne[k][1:]) - 1] = 1.
                k = 2

        while k<len(ligne):
            if ligne[k] != "-":
                try:
                    self.c[int(ligne[k+2][1:]) - 1] = float(ligne[k+1])
                    k += 3
                except:
                    self.c[int(ligne[k + 1][1:]) - 1] = 1.
                    k += 2
            else:
                try:
                    self.c[int(ligne[k+2][1:]) - 1] = float(ligne[k+1])*-1
                    k += 3
                except:
                    self.c[int(ligne[k + 1][1:]) - 1] = -1.
                    k += 2
        aDupliquer = []
        #lecture des contraintes
        for j in range(0, self.m):
            ligne = lines[j+2].split()
            print(ligne)
            self.a.append([0.]*self.n)

            if ligne[0] != "-":
                try:
                    self.a[j][int(ligne[1][1:]) - 1] = float(ligne[0])
                    k = 2
                except:
                    self.a[j][int(ligne[0][1:]) - 1] = 1.
                    k = 1

            while ligne[k]!=">=" and ligne[k]!="<=" and ligne[k]!="=":
                if ligne[k] != "-":
                    try:
                        self.a[j][int(ligne[k + 2][1:]) - 1] = float(ligne[k + 1])
                        k += 3
                    except:
                        self.a[j][int(ligne[k + 1][1:]) - 1] = 1.
                        k += 2
                else:
                    try:
                        self.a[j][int(ligne[k + 2][1:]) - 1] = float(ligne[k + 1]) * -1
                        k += 3
                    except:
                        self.a[j][int(ligne[k + 1][1:]) - 1] = -1.
                        k += 2
            if ligne[k]=="=":
                aDupliquer.append(j)
            self.sens.append(ligne[k]==">=" or ligne[k]=="=")
            self.b.append(float(ligne[k+1]))

        for j in aDupliquer:
            self.a.append(self.a[j][:])
            self.b.append(self.b[j])
            self.sens.append(False)
            self.m+=1

    def print(self):
        print(self.c)
        print(self.a)
        print(self.b)
        print(self.sens)
        ligne = ""
        if self.maximisation:
            ligne+="Maximiser "
        else:
            ligne+="Minimiser "
        debut = True
        for i in range(0, self.n):
            if self.c[i]!=0:
                if debut or self.c[i]<0:
                    ligne += "{cout} X{indice}".format(cout=self.c[i], indice=i+1)
                else:
                    ligne += " + {cout} X{indice}".format(cout=self.c[i], indice=i+1)
                debut = False
        print(ligne)
        print("S.c :")
        for i in range(0, self.m):
            ligne = ""
            debut = True
            for j in range(0, self.n):
                if self.a[i][j] != 0:
                    if debut or self.a[i][j] < 0:
                        ligne += "{cout} X{indice}".format(cout=self.a[i][j], indice=j+1)
                    else:
                        ligne += " + {cout} X{indice}".format(cout=self.a[i][j], indice=j+1)
                    debut = False
            if self.sens[i]:
                ligne+=" >= "
            else:
                ligne+=" <= "
            ligne+=str(self.b[i])
            print(ligne)
