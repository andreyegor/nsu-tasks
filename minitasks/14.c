#define PY_SSIZE_T_CLEAN

#include <Python.h>

PyObject *foreign_matrix_power(PyObject *self, PyObject *args) {
    PyObject *in_matrix;
    PyObject *in_degree;
    if (!PyArg_UnpackTuple(args, "тут вроде что-то для эксепшнсов должно быть", 1, 2, &in_matrix, &in_degree)) {
        PyErr_SetString(PyExc_Exception, "1");
        return NULL;
    }
    long degree = PyLong_AsLong(in_degree);
    long matrix_size = PyObject_Length(in_matrix);

    PyObject *deepCopy = PyObject_GetAttrString(PyImport_ImportModule("copy"), "deepcopy");
    if (!deepCopy) {
        PyErr_SetString(PyExc_Exception, "3");
        return NULL;
    }

    double c_matrix[matrix_size][matrix_size];
    double other_c_matrix[matrix_size][matrix_size];
    double third_c_matrix[matrix_size][matrix_size];
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            c_matrix[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(in_matrix, i), j));
            other_c_matrix[i][j] = c_matrix[i][j];
            third_c_matrix[i][j] = c_matrix[i][j];
        }
    }
    for (long n = 1; n < degree; n++) {
        for (long i = 0; i < matrix_size; i++) {
            for (long j = 0; j < matrix_size; j++) {
                double ij = 0;
                for (long q = 0; q < matrix_size; q++) {
                    printf("%f*%f=%f ", other_c_matrix[i][q], c_matrix[q][j], other_c_matrix[i][q] * c_matrix[q][j]);
                    ij += other_c_matrix[i][q] * c_matrix[q][j];
                }
                printf("\n");
                third_c_matrix[i][j] = ij;
            }
        }
        for (int i = 0; i < matrix_size; i++)
            for (int j = 0; j < matrix_size; j++)
                other_c_matrix[i][j] = third_c_matrix[i][j];
    }
    PyObject *out_matrix = PyList_New(matrix_size);
    for (long i = 0; i < matrix_size; i++) {
        PyObject *line = PyList_New(matrix_size);
        for (long j = 0; j < matrix_size; j++) {
            PyList_SetItem(line, j, PyFloat_FromDouble(other_c_matrix[i][j]));
        }
        PyList_SetItem(out_matrix, i, line);
    }

    return out_matrix;
}

static PyMethodDef ForeignMethods[] = {
        {"foreign_matrix_power", foreign_matrix_power, METH_VARARGS, ""},
        {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef foreignmodule = {PyModuleDef_HEAD_INIT, "foreign", NULL, -1, ForeignMethods};

PyMODINIT_FUNC PyInit_foreign(void) { return PyModule_Create(&foreignmodule); }

int main() { return 0; }