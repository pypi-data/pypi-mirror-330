#include <stdbool.h>
#include <stdlib.h>

#include <Python.h>
#include <numpy/arrayobject.h>

#include "mis.h"


static PyObject* max_independent_set(PyObject *self, PyObject *args) {
    PyArrayObject *matrix;
    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &matrix)) {
        return NULL;
    }

    int n;
    int **adj = parse_numpy_matrix(matrix, &n);

    if (adj == NULL) {
        return PyErr_NoMemory();
    }


    bool *independent_set = calloc(n, sizeof(bool));

    simulated_annealing_mis(adj, n, independent_set);

    // Convert result to a Python list
    PyObject *result = PyList_New(0);
    for (int i = 0; i < n; i++) {
        if (independent_set[i]) {
            PyList_Append(result, PyLong_FromLong(i));
        }
    }

    free(independent_set);
    free(adj);
    return result;
}

static PyMethodDef MISMethods[] = {
    {"max_independent_set", max_independent_set, METH_VARARGS, "Find a Maximum Independent Set"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mis_module = {
    PyModuleDef_HEAD_INIT, "_mis_finder_core", NULL, -1, MISMethods
};

PyMODINIT_FUNC PyInit__mis_finder_core() {
    import_array();  // Initialize NumPy C API
    return PyModule_Create(&mis_module);
}
