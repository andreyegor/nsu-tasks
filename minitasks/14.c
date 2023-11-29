#define PY_SSIZE_T_CLEAN

#include <Python.h>


PyObject *foreign_matrix_power(PyObject *self, PyObject *args) {
    PyObject *in_matrix;
    if (!PyArg_ParseTuple(args, "O", &in_matrix)) {
        PyErr_SetString(PyExc_Exception, "1");
        return NULL;
    }

    int matrix_size = PyObject_Length(in_matrix);

    int degree = 2;
//    if (!PyArg_ParseTuple(args, "n", &degree)) {
//        PyErr_SetString(PyExc_Exception, "2");
//        return NULL;
//    }

    PyObject *deepCopy = PyObject_GetAttrString(PyImport_ImportModule("copy"), "deepcopy");
    if (!deepCopy) {
        PyErr_SetString(PyExc_Exception, "3");
        return NULL;
    }

    PyObject *out_matrix = PyObject_CallFunctionObjArgs(deepCopy, in_matrix, NULL);

    double c_matrix[matrix_size][matrix_size];
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            c_matrix[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(in_matrix, i), j));
        }
    }

    for (int n = 1; n < degree; n++) {
        for (int i = 0; i < matrix_size; i++) {
            for (int j = 0; i < matrix_size; i++) {
                double ij = 0;
                for (int q = 0; q < matrix_size; q++) {
                    ij += c_matrix[i][q] * c_matrix[q][j];
                }
                PyList_SetItem(PyList_GetItem(out_matrix, i), j, PyFloat_FromDouble(ij));
            }
        }
    }
    return out_matrix;
}

static PyMethodDef ForeignMethods[] = {
        {"foreign_matrix_power",
                foreign_matrix_power, METH_VARARGS,
                ""
        },
        {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef foreignmodule = {
        PyModuleDef_HEAD_INIT,
        "foreign", /* name of module */
        NULL, /* module documentation, may be NULL */
        -1, /* size of per-interpreter state of the module,
or -1 if the module keeps state in global variables. */
        ForeignMethods
};

PyMODINIT_FUNC PyInit_foreign(void) {
    return PyModule_Create(&foreignmodule);
}

int main() {

    return 0;
}