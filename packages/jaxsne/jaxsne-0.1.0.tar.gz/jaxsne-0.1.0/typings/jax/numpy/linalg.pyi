from jax import Array

def norm(arr: Array, ord: int = 2, axis: int = -1) -> Array: ...  # noqa: A002
def eig(arr: Array) -> tuple[Array, Array]: ...
