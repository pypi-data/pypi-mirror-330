__all__ = ["max_independent_set", "is_independent_set"]

from typing import TYPE_CHECKING, Annotated, Literal, Iterable, Callable, ParamSpec, TypeVar
from typing_extensions import Doc

from _mis_finder_core import max_independent_set as _max_independent_set

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

    ArrayNxN = Annotated[NDArray[np.int64], Literal["N", "N"], Doc(
        "Numpy Square matrix (N x N) of type `numpy.int64`."
    )]


Param = ParamSpec("Param")
RetType = TypeVar("RetType")


def validate_shape(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
    def wrapper(adj_matrix: "ArrayNxN", *args: Param.args, **kwargs: Param.kwargs) -> RetType:
        if not hasattr(adj_matrix, "shape"):
            raise TypeError(f"Adjacency matrix should be a numpy array. Got: {type(adj_matrix)}")

        shape = adj_matrix.shape

        if len(shape) != 2 or shape[0] != shape[1]:
            raise TypeError(f"Adjacency matrix not square. Passed shape: {shape}")

        return func(adj_matrix, *args, **kwargs)

    return wrapper


@validate_shape
def max_independent_set(adj_matrix: "ArrayNxN") -> list[int]:
    return _max_independent_set(adj_matrix)


@validate_shape
def is_independent_set(adj_matrix: "ArrayNxN", chosen_nodes: Iterable[int]) -> bool:
    import numpy as np
    return not np.any(adj_matrix[np.ix_(chosen_nodes, chosen_nodes)])
