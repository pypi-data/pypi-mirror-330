import turtle
import math

class Courbe:
    """
    Classe représentant une courbe sur le graphique.
    Elle gère le tracé progressif de points et stocke les données.
    """
    def __init__(self, nom, couleur='red', epaisseur=2):
        self.nom = nom
        self.couleur = couleur
        print(f"Couleur définie : {self.couleur}")  # Debug
        self.epaisseur = epaisseur
        # Création d'un objet turtle dédié à cette courbe
        self.tortue = turtle.Turtle()
        self.tortue.hideturtle()
        self.tortue.speed(0)  # Vitesse maximale
        self.tortue.penup()
        self.tortue.color(self.couleur)
        self.tortue.pensize(self.epaisseur)
        self.data = []  # Stocke les points sous forme (x, y)

    def ajouter_point(self, x, y):
        """
        Ajoute un point à la courbe et trace le segment correspondant.
        """
        if not self.data:
            # Pour le premier point, on se déplace sans tracer
            self.tortue.goto(x, y)
            self.tortue.pendown()
        else:
            # Pour les points suivants, on trace une ligne depuis le dernier point
            self.tortue.goto(x, y)
        self.data.append((x, y))


class GraphiqueTempsReel:
    """
    Classe principale pour la gestion d'un graphique dynamique avec turtle.
    
    Caractéristiques :
    - Possibilité d'ajouter plusieurs courbes
    - Mise à jour en continu sans redessiner toute la scène
    - Auto-mise à l'échelle optionnelle (les axes s'ajustent si une donnée sort du cadre)
    - Gestion de la pause/reprise de l'animation (touche 'p')
    """
    def __init__(self, largeur=800, hauteur=600, auto_scale=True, x_range=(0, 100), y_range=(-1, 1)):

        self.screen = turtle.Screen()
        self.screen.setup(largeur, hauteur)
        self.auto_scale = auto_scale
        # On stocke les bornes sous forme de liste pour pouvoir les modifier
        self.x_range = list(x_range)
        self.y_range = list(y_range)
        # Si auto_scale est désactivé, on fixe le repère
        if not auto_scale:
            self.screen.setworldcoordinates(self.x_range[0], self.y_range[0], self.x_range[1], self.y_range[1])
        # Désactivation du tracer automatique pour améliorer les performances
        turtle.tracer(0, 0)
        self.courbes = {}  # Dictionnaire pour stocker les courbes ajoutées
        self.paused = False

        # Liaison de la touche 'p' pour basculer entre pause et reprise
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.listen()

    def ajouter_courbe(self, nom, couleur='black', epaisseur=2):
        """
        Ajoute une nouvelle courbe au graphique.
        """
        if nom in self.courbes:
            print(f"La courbe {nom} existe déjà.")
            return
        self.courbes[nom] = Courbe(nom, couleur, epaisseur)

    def mettre_a_jour_courbe(self, nom, x, y):
        """
        Met à jour la courbe identifiée par 'nom' en ajoutant un nouveau point (x, y).
        Si l'animation est en pause, l'update est ignorée.
        """
        if self.paused:
            return
        if nom not in self.courbes:
            print(f"La courbe {nom} n'existe pas.")
            return
        courbe = self.courbes[nom]
        courbe.ajouter_point(x, y)
        # Si l'auto-mise à l'échelle est activée, on vérifie que le nouveau point est dans le cadre
        if self.auto_scale:
            self.verifier_redimensionnement(x, y)
        # On force la mise à jour de l'écran
        turtle.update()

    def verifier_redimensionnement(self, x, y):
        """
        Vérifie si le nouveau point (x, y) sort du cadre actuel.
        Si oui, ajuste les bornes (avec une marge) et met à jour les coordonnées mondiales.
        """
        redim = False
        marge = 10  # Marge en unités
        if x < self.x_range[0]:
            self.x_range[0] = x - marge
            redim = True
        if x > self.x_range[1]:
            self.x_range[1] = x + marge
            redim = True
        if y < self.y_range[0]:
            self.y_range[0] = y - marge
            redim = True
        if y > self.y_range[1]:
            self.y_range[1] = y + marge
            redim = True
        if redim:
            # Mise à jour du repère du screen
            self.screen.setworldcoordinates(self.x_range[0], self.y_range[0], self.x_range[1], self.y_range[1])
            turtle.update()

    def toggle_pause(self):
        """
        Bascule l'état de l'animation entre pause et reprise.
        Appuyer sur la touche 'p' permet d'interrompre ou de relancer la mise à jour.
        """
        self.paused = not self.paused
        if self.paused:
            print("Animation en pause.")
        else:
            print("Animation reprise.")

    def run(self):
        """
        Lance la boucle principale de turtle.
        """
        turtle.mainloop()


# ============================================================
# Exemple d'utilisation : Tracé d'une onde sinusoïdale dynamique
# ============================================================

if __name__ == '__main__':
    import time

    # Création d'un graphique avec auto-mise à l'échelle activée
    graph = GraphiqueTempsReel(auto_scale=True, x_range=(0, 100), y_range=(-2, 2))
    # Ajout d'une courbe nommée "sinus", tracée en bleu
    graph.ajouter_courbe("sinus", couleur="blue", epaisseur=2)

    x = 0  # Abscisse initiale

    def update():
        """
        Fonction récursive appelée périodiquement pour ajouter des points à la courbe.
        Elle simule l'évolution d'une onde sinusoïdale.
        """
        global x
        if not graph.paused:
            # Calcul de la valeur sinus (conversion de x en radians)
            y = math.sin(math.radians(x))
            graph.mettre_a_jour_courbe("sinus", x, y)
            x += 5  # Incrément en x pour le prochain point
        # Planifie l'appel suivant de 'update' dans 100 ms
        graph.screen.ontimer(update, 100)

    # Démarrer la mise à jour de l'animation
    update()
    # Lancer la boucle principale de turtle (cette ligne bloque)
    graph.run()
