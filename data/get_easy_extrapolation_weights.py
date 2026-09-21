import ast
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def get_ex_weights(filename):
    file_path = os.path.join(_THIS_DIR, filename) 

    eval_weights = []
    train_weights_10 = []
    train_weights_20 = []
    train_weights_30 = []

    with open(file_path, "r") as file:
        if filename == "easy_extrapolation_train_weights_10.txt":
            for line in file:
                line = line.strip()
                train_weights_10.append(ast.literal_eval(line))
            return train_weights_10

        elif filename == "easy_extrapolation_train_weights_20.txt":
            for line in file:
                line = line.strip()
                train_weights_20.append(ast.literal_eval(line))
            return train_weights_20

        elif filename == "easy_extrapolation_train_weights_30.txt":
            for line in file:
                line = line.strip()
                train_weights_30.append(ast.literal_eval(line))
            return train_weights_30

        elif filename == "easy_extrapolation_evaluation_weights.txt":
            for line in file:
                line = line.strip()
                eval_weights.append(ast.literal_eval(line))
            return eval_weights
