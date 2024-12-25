import numpy as np

class InformationTheory:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)
        self.total = self.matrix.sum()

    def calculate_entropy(self, probabilities):
        """Вычисление энтропии из вероятностей."""
        return -np.sum(probabilities * np.log2(probabilities + np.finfo(float).eps))

    def compute_joint_probabilities(self):
        """Вычисление совместных вероятностей."""
        return self.matrix / self.total

    def marginal_probabilities(self, joint_probs):
        """Вычисление маргинальных вероятностей для X и Y."""
        p_y = joint_probs.sum(axis=1)
        p_x = joint_probs.sum(axis=0)
        return p_x, p_y

    def conditional_entropy(self, joint_probs, p_y):
        """Вычисление условной энтропии H(Y|X)."""
        cond_probs = joint_probs / p_y[:, np.newaxis]
        cond_entropy = np.sum(p_y * np.array([self.calculate_entropy(cond_probs[i]) for i in range(len(joint_probs))]))
        return cond_entropy

    def mutual_information(self, p_x, p_y, cond_h):
        """Вычисление взаимной информации I(X;Y)."""
        h_x = self.calculate_entropy(p_x)
        return h_x - cond_h

    def process(self):
        joint_probs = self.compute_joint_probabilities()
        p_x, p_y = self.marginal_probabilities(joint_probs)
        
        h_y = self.calculate_entropy(p_y)
        cond_h = self.conditional_entropy(joint_probs, p_y)
        info = self.mutual_information(p_x, p_y, cond_h)
        
        h_xy_sum = h_y + cond_h
        
        print(f"Информация:          {info:.3f}")
        print(f"Совместная энтропия: {h_xy_sum:.3f}")

test_matrix = [[20, 15, 10, 5],
               [30, 20, 15, 10],
               [25, 25, 20, 15],
               [20, 20, 25, 20],
               [15, 15, 30, 25]]

info_theory = InformationTheory(test_matrix)
info_theory.process()
