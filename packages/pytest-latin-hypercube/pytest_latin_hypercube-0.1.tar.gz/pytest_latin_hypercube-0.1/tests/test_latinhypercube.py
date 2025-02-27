import pytest
from pytest_latin_hypercube import latin_hyperrectangle, LHparameterised
import inspect


@pytest.mark.parametrize("x", [{"x": [0, 1, 2]}, {"x": [0, 1, 2], "y": [0, 1, 2]}, {
                         "x": []}, {"x": [0, 1, 2, 4], 2: [0, 1, 2, 3], "z": [0, 2, 5, 1]}])
def test_latinproperty(x):
    argnames, argvalues = latin_hyperrectangle(x)
    for i, arg in enumerate(argnames):
        values = [val for val in x[arg]]
        values2 = [argvalues[j][i] for j in range(len(argvalues))]
        assert len(values2) == len(set(values2))
        assert len(values) == len(values2)
        values = sorted(values)
        values2 = sorted(values2)
        for i in range(len(values)):
            assert values[i] == values2[i]


@pytest.mark.parametrize("x", [{"x": [0, 1, 2]}, {"x": [0, 1], "y": [0, 1, 2]}, {"x": []}, {"x": [
                         0, 1, 2, 4], 2: [0, 1, 2, 3], "z": [0, 2, 5, 1]}, {"x": [0, 1, 2, 4], 2: [0, 1], "z": [0, 2, 5]}])
def test_lengths(x):
    M = len(x)
    N = len(next(iter(x.values()), []))
    for value in x.values():
        if len(value) > N:
            N = len(value)
    keys, values = latin_hyperrectangle(x)
    assert len(keys) == M
    assert len(values) == N
    if len(values) > 0:
        assert len(values[0]) == M


@pytest.mark.parametrize("seed", [847 + i for i in range(10)])
def test_seed(seed):
    x = {"x": [0, 1], "y": [0, 1, 2], "z": [0, 1, 2]}
    keys, values = latin_hyperrectangle(x, seed=seed)
    keys2, values2 = latin_hyperrectangle(x, seed=seed)
    assert keys == keys2
    assert values == values2


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_number_of_iterations(k):
    x = {"x": [0, 1, 2], "y": [0, 1, 2], "z": [0, 1, 2]}
    M = len(x)
    N = len(next(iter(x.values()), []))
    for value in x.values():
        if len(value) > N:
            N = len(value)
    keys, values = latin_hyperrectangle(
        x, number_of_iterations=k)
    assert len(keys) == M
    assert len(values) == N * k
    if len(values) > 0:
        assert len(values[0]) == M


@pytest.mark.parametrize(["func", "args"],
                         [[lambda x, y: x + y, [[1, 2, 3], [4, 5, 6]]]])
def test_output_is_valid_input(func, args):
    args_dict = inspect.getcallargs(func, *args)
    argnames, argvalues = latin_hyperrectangle(args_dict)
    try:
        pytest.mark.parametrize(argnames, argvalues)(func)
        assert True
    except KeyError:
        assert False

@pytest.mark.parametrize("x", [{"x": [0, 0, 0], "y": [0, 1, 1]}, {"x": [0], "y": [0, 1, 1], "z": [0, 1, 1]}])
def test_max_iteration_warning(x):
    with pytest.warns(UserWarning):
        latin_hyperrectangle(x, number_of_iterations=100, max_iteration_factor=60)

@LHparameterised(
    {"x": [0, 1, 2], "y": [0, 1, 2], "z": [0, 1, 2]}, seed=847)
def test_latinhypercube_parameterised(x, y, z):
    assert x in [0, 1, 2]
    assert y in [0, 1, 2]
