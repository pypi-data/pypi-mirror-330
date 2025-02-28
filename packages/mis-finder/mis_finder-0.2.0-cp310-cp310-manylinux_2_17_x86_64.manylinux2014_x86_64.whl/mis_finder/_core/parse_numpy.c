#include <numpy/arrayobject.h>


// Function to parse NumPy array input
int** parse_numpy_matrix(PyArrayObject *matrix, int *n) {
    *n = PyArray_DIM(matrix, 0);  // Get matrix size
    int **adj = malloc(*n * sizeof(int*));

    if (adj == NULL) {
        return NULL;
    }

    for (int i = 0; i < *n; i++) {
        adj[i] = (int*) PyArray_GETPTR2(matrix, i, 0);
    }

    return adj;
}
