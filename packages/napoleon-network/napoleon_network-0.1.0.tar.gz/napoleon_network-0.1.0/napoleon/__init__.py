# Copyright (c) 2025 Matheo
# Licensed under the MIT License (see LICENSE.txt for details)


import random
from . import module
class Napoleon():
    def __init__(self,tree,dataset,learn,epoch=10000):
        self.section = tree
        self.dataset = dataset
        self.learn = learn
        self.epoch = epoch
        self.weights = []
        self.biases = []

    def train(self):

        for i in range(len(self.section) - 1):
            # Les poids reliant la couche i à la couche i+1
            w_layer = [[random.uniform(-1, 1) for _ in range(self.section[i])]
                    for _ in range(self.section[i + 1])]
            self.weights.append(w_layer)
            # Biais pour la couche i+1
            b_layer = [random.uniform(-1, 1) for _ in range(self.section[i + 1])]
            self.biases.append(b_layer)

        num_layers = len(self.section) - 1  # Nombre de couches de poids (couches cachées + sortie)

        # Boucle d'entraînement
        for epoch in range(self.epoch):
            for data in self.dataset:
                # Extraction des entrées et valeurs attendues
                input_vals = list(data[:self.section[0]])
                expected = list(data[self.section[0]:])
                
                # --- Propagation avant ---
                activations = []  # Stockera l'activation de chaque couche
                activation = input_vals
                activations.append(activation)
                # Pour chaque couche du réseau
                for l in range(num_layers):
                    new_activation = []
                    for i in range(self.section[l + 1]):
                        # Calcul de la somme pondérée + biais
                        s = sum(activation[j] * self.weights[l][i][j] for j in range(self.section[l]))
                        s += self.biases[l][i]
                        new_activation.append(module.sigmoid(s))
                    activation = new_activation
                    activations.append(activation)
                
                # --- Rétropropagation ---
                # Calcul des deltas pour chaque couche (on en aura num_layers au total)
                deltas = [None] * num_layers
                # Couche de sortie (dernière couche d'activations)
                output = activations[-1]
                delta_out = []
                for i in range(self.section[-1]):
                    error = expected[i] - output[i]
                    delta_out.append(error * module.sigmoid_derive(output[i]))
                deltas[-1] = delta_out
                
                # Calcul des deltas pour les couches cachées (de l'avant-dernière à la première)
                for l in range(num_layers - 2, -1, -1):
                    delta_layer = []
                    for i in range(self.section[l + 1]):  # Pour chaque neurone de la couche
                        error = 0.0
                        for j in range(self.section[l + 2]):  # Parcours de la couche l+2
                            error += self.weights[l + 1][j][i] * deltas[l + 1][j]
                        # Multiplication par la dérivée de la sigmoïde pour la couche courante
                        delta_layer.append(error * module.sigmoid_derive(activations[l + 1][i]))
                    deltas[l] = delta_layer
                
                # --- Mise à jour des poids et biais ---
                for l in range(num_layers):
                    for i in range(self.section[l + 1]):
                        for j in range(self.section[l]):
                            self.weights[l][i][j] += self.learn * deltas[l][i] * activations[l][j]
                        self.biases[l][i] += self.learn * deltas[l][i]
    def try_network(self):
        num_layers = len(self.section) - 1
        for data in self.dataset:
            input_vals = list(data[:self.section[0]])
            expected = list(data[self.section[0]:])
            
            activation = input_vals
            # Propagation avant pour obtenir la sortie
            for l in range(num_layers):
                new_activation = []
                for i in range(self.section[l + 1]):
                    s = sum(activation[j] * self.weights[l][i][j] for j in range(self.section[l]))
                    s += self.biases[l][i]
                    new_activation.append(module.sigmoid(s))
                activation = new_activation
            output = activation
            print(f"Entrée: {input_vals} -> Sortie calculée: {[round(x) for x in output]} (attendue: {expected})")
