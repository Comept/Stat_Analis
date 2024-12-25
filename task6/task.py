import json


class FuzzySystem:
    def __init__(self, temperatures, regulator, transitions):
        self.temperatures = temperatures
        self.regulator = regulator
        self.transitions = transitions

    def calculate_membership(self, value, points):
        for i in range(len(points) - 1):
            x0, mu0 = points[i]
            x1, mu1 = points[i + 1]
            if x0 <= value <= x1:
                if mu0 == mu1:
                    return mu0
                return mu0 + (mu1 - mu0) * (value - x0) / (x1 - x0)
        return 0

    def fuzzify(self, value, fuzzy_set):
        return {term: round(self.calculate_membership(value, points), 2)
                for term, points in fuzzy_set.items()}

    def map_to_regulator(self, temp_mu_vals):
        reg_mu_vals = {}
        for temp_term, temp_mu in temp_mu_vals.items():
            reg_term = self.transitions.get(temp_term)
            if reg_term:
                reg_mu_vals[reg_term] = max(reg_mu_vals.get(reg_term, 0), temp_mu)
        return reg_mu_vals

    def defuzzify(self, reg_mu_vals):
        max_mu = max(reg_mu_vals.values())
        x_vals = []

        for term, mu in reg_mu_vals.items():
            if mu == max_mu:
                for (x0, mu0), (x1, mu1) in zip(self.regulator[term][:-1], self.regulator[term][1:]):
                    if min(mu0, mu1) <= max_mu <= max(mu0, mu1):
                        x = x0 + (x1 - x0) * (max_mu - mu0) / (mu1 - mu0)
                        x_vals.append(x)

        return sum(x_vals) / len(x_vals) if x_vals else 0

    def process(self, temperature):
        temp_mu_vals = self.fuzzify(temperature, self.temperatures)
        reg_mu_vals = self.map_to_regulator(temp_mu_vals)
        return self.defuzzify(reg_mu_vals)


def main(temps_json, reg_json, trans_json, temp_input):
    temperatures = json.loads(temps_json)
    regulator = json.loads(reg_json)
    transitions = json.loads(trans_json)

    fuzzy_system = FuzzySystem(temperatures, regulator, transitions)
    result = fuzzy_system.process(temp_input)

    print(f"Результат дефаззификации: {result}")


temperatures = '''{
    "холодно": [[0,1],[16,1],[20,0],[50,0]],
    "комфортно": [[16,0],[20,1],[22,1],[26,0]],
    "жарко": [[0,0],[22,0],[26,1],[50,1]]
}'''

regulator = '''{
    "слабо": [[0,1],[6,1],[10,0],[20,0]],
    "умеренно": [[6,0],[10,1],[12,1],[16,0]],
    "интенсивно": [[0,0],[12,0],[16,1],[20,1]]
}'''

transition = '''{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}'''

main(temperatures, regulator, transition, 25)
