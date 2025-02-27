import pytest
from numpy.random import default_rng
import warnings


def LHparameterised(args: dict, seed: int = 847):
    """Decorator that allows for Latin Hypercube sampling of parameters.

    Parameters
    ----------
    args : dict
        A dictionary with keys, which is all of the parameters and values, a
        list of the values that each parameter can take.
    seed : int
        The seed for the random number generator used to generate samples.

    Returns
    -------
    wrapper : function
        The test function, decorated with the pytest.mark.parametrize
        decorator so that the test function is collected by pytest with the
        Latin Hypercube sampling of the parameters.
    """
    def wrapper(test_func):
        argnames, argvalues = latin_hyperrectangle(args, seed=seed)
        return pytest.mark.parametrize(argnames, argvalues)(test_func)
    return wrapper


def latin_hyperrectangle(args: dict,
                         seed: int = 847,
                         number_of_iterations: int = 1,
                         max_iteration_factor: int = 10) -> tuple[list, list]:
    """
    Given a dictionary containing the identifiers of parameters and a list of
    values each parameter can take, this returns a lists of samples of each
    parameter, of length equal to the length of the longest list of values a
    parameter can take. This has the Latin property, that no value of a
    parameter is sampled until all the possible values which the parameter can
    take have been used.

    This has been designed to be used with the pytest.mark.parametrize,
    i.e. that pytest.mark.parametrize(*latin_hyperrectangle(args))(test_func)
    returns a test function that is parameterised by the Latin Hypercube
    sample.

    Parameters
    ----------
    args: dict
        A dictionary with keys, which are that are identifiers of the
        parameters, and values, a list of the values that that parameter can
        take.
    seed: int
        The seed for the random number generator used to generate samples.
    number_of_iterations: int
        The number of iterations to perform. The number of samples returned is
        this multiplied by the length of the longest parameter space.
    max_iteration_factor: int
        The maximum number of iterations to perform before returning a partial
        sample is given by the product of the length of the longest parameter
        space, the number of iterations and this factor.

    Returns
    -------
    key : list
        A list containing each parameter name - the keys of the args parameter.
    samples : list[list]
        A list of lists containing the Latin Hypercube samples. Each list has
        the same length as the number of parameters and the number of samples
        is equal to the product of the length of the longest parameter space
        and the number of iterations.
    """
    keys = []
    longest_parameter_space = 0
    rng = default_rng(seed)
    for key, value in args.items():
        keys.append(key)
        if len(value) > longest_parameter_space:
            longest_parameter_space = len(value)
    samples = []
    shuffled_args = {key: list(rng.permutation(value * number_of_iterations))
                     for key, value in args.items()}
    iter = 0
    while len(samples) < longest_parameter_space * number_of_iterations:
        iter += 1
        max_iter = max_iteration_factor * longest_parameter_space \
            * number_of_iterations
        sample = ([shuffled_args[key].pop() for key in keys])
        if sample not in samples:
            samples.append(sample)
        for key, value in args.items():
            if len(shuffled_args[key]) == 0:
                shuffled_args[key] = list(
                    rng.permutation(value * number_of_iterations))

        if iter > (max_iteration_factor * longest_parameter_space
                   * number_of_iterations):
            warnings.warn(
                "Maximum number of iterations"
                f"({(max_iter)}) reached. Returning partial sample.")
            break
    return keys, samples
