import torch
from bpexts.utils import set_seeds
from bpexts.gradient import extend
from .test_problem import TestProblem

TEST_SETTINGS = {
    "in_features": 20,
    "out_features": 10,
    "bias": True,
    "batch": 13,
    "rtol": 1e-5,
    "atol": 1e-5
}

ACTIVATIONS = {
    'ReLU': extend(torch.nn.ReLU()),
    'Sigmoid': extend(torch.nn.Sigmoid()),
    'Tanh': extend(torch.nn.Tanh())
}

set_seeds(0)
linearlayer = extend(
    torch.nn.Linear(
        in_features=TEST_SETTINGS["in_features"],
        out_features=TEST_SETTINGS["out_features"],
        bias=TEST_SETTINGS["bias"],
    ))
summationLinearLayer = extend(
    torch.nn.Linear(
        in_features=TEST_SETTINGS["out_features"], out_features=1, bias=True))

input_size = (TEST_SETTINGS["batch"], TEST_SETTINGS["in_features"])
X = torch.randn(size=input_size)


def make_regression_problem(activation):
    model = torch.nn.Sequential(linearlayer, activation, summationLinearLayer)

    Y = torch.randn(size=(model(X).shape[0], 1))

    lossfunc = extend(torch.nn.MSELoss())

    return TestProblem(X, Y, model, lossfunc)


def make_classification_problem(activation):
    class To2D(torch.nn.Module):
        def __init__(self):
            super().__init__()

        def forward(self, input):
            return input.view(input.shape[0], -1)

    model = torch.nn.Sequential(linearlayer, activation, To2D())

    Y = torch.randint(high=model(X).shape[1], size=(X.shape[0], ))

    lossfunc = extend(torch.nn.CrossEntropyLoss())

    return TestProblem(X, Y, model, lossfunc)


TEST_PROBLEMS = {}
for act_name, act in ACTIVATIONS.items():
    TEST_PROBLEMS["linear{}-regression".format(
        act_name)] = make_regression_problem(act)
    TEST_PROBLEMS["linear{}-classification".format(
        act_name)] = make_classification_problem(act)
