import json


def calculate_mu(x, points):
    for i in range(len(points) - 1):
        x0, mu0 = points[i]
        x1, mu1 = points[i + 1]
        if x0 <= x <= x1:
            return mu0 if mu0 == mu1 else mu0 + (mu1 - mu0) * (x - x0) / (x1 - x0)      
    return 0


def map_to_regulator(temp_mu_vals, transition_map):
    reg_mu_vals = {}
    for temp_term, temp_mu in temp_mu_vals.items():
        reg_term = transition_map[temp_term]
        reg_mu_vals[reg_term] = max(reg_mu_vals.get(reg_term, 0), temp_mu)
    
    print(f"Проекция на нечеткое множество положений регулятора: {reg_mu_vals}\n")
    return reg_mu_vals


def fuzz(value, fuzzy_set):
    mu_vals = {term: round(calculate_mu(value, points), 2) 
               for term, points in fuzzy_set.items()}
    print(f"Фаззификация температуры {value}: {mu_vals}\n")
    return mu_vals


def defuzz_meanmax(reg_mu_vals, fuzzy_set):
    max_mu = max(reg_mu_vals.values())
    x_vals = []

    for term, mu in reg_mu_vals.items():
        if mu == max_mu:
            for i in range(len(fuzzy_set[term]) - 1):
                x0, mu0 = fuzzy_set[term][i]
                x1, mu1 = fuzzy_set[term][i + 1]
                
                if min(mu0, mu1) <= max_mu <= max(mu0, mu1):
                    x = x0 if mu0 == mu1 else x0 + (x1 - x0) * (max_mu - mu0) / (mu1 - mu0)
                    x_vals.append(x)
                        
    return sum(x_vals) / len(x_vals) if x_vals else 0


def main(temps_json, reg_json, trans_json, temp_input):
    temps_set = json.loads(temps_json)
    reg_set = json.loads(reg_json)
    trans_map = json.loads(trans_json)

    temp_mu_vals = fuzz(temp_input, temps_set)
    reg_mu_vals = map_to_regulator(temp_mu_vals, trans_map)
    mean_max = defuzz_meanmax(reg_mu_vals, reg_set)

    print(f"Дефаззифицированное положение регулятора: {mean_max}\n")

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