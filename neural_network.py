import numpy as np


class NeuralNetwork:
    def __init__(self, l_0, l_1, l_2, l_3):
        self.l_0 = l_0
        self.l_1 = l_1
        self.l_2 = l_2
        self.l_3 = l_3
        self.w_0_1 = None
        self.w_1_2 = None
        self.w_2_3 = None
        self.relu = lambda x: (x > 0) * x

    # загрузка весовых коэффицентов
    def load_weights(self, weights):
        self.w_0_1 = np.reshape(weights[:self.l_0 * self.l_1], (-1, self.l_0))
        self.w_1_2 = np.reshape(weights[self.l_0 * self.l_1:self.l_1 * (self.l_2 + self.l_0)], (-1, self.l_1))
        self.w_2_3 = np.reshape(weights[self.l_1 * (self.l_2 + self.l_0):], (-1, self.l_2))

    # опрос нейронной сети
    def query(self, inputs_list):
        # преобразовать список входных значений в двумерный массив
        inputs = np.array(inputs_list, ndmin=2).T

        # рассчитать входящие сигналы для скрытого слоя
        layer_1 = self.relu(np.dot(self.w_0_1, inputs))

        layer_2 = self.relu(np.dot(self.w_1_2, layer_1))

        return np.dot(self.w_2_3, layer_2)

