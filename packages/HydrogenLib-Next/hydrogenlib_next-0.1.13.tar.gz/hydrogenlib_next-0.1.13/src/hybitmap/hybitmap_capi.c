#include "hybitmap_source.c"

#define fix_index_error(i, size) \
    if (i < 0)i += size

bool check_and_error(ll index, ll start, ll end, ll size){
    if (index < 0)index += size;
    if (start < 0)start += size;
    if (end < 0)end += size;
    if (!check_index(index, start, end) || start < 0 || end < 0){
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        return true;
    }
    return false;
}

static PyObject* byte_get_bit(Byte_t *self, PyObject *args){
    int bit_index;
    if(!PyArg_ParseTuple(args, "i", &bit_index)){
        PyErr_BadArgument();
    }
    fix_index_error(bit_index, 8);
    check_and_error(bit_index, 0, 8, 8);
    return PyLong_FromLong(_byte_get_bit(self, bit_index));
}

static PyObject* byte_set_bit(Byte_t *self, PyObject *args, PyObject *kwds){
    int bit_index;
    bool value;
    static char* kwlist[] = {"bit_index", "value", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "ib", &bit_index, &value)){
        PyErr_BadArgument();
    }
    fix_index_error(bit_index, 8);
    check_and_error(bit_index, 0, 8, 8);
    _byte_set_bit(self, bit_index, value);
    Py_RETURN_NONE;
}


static PyObject* bitmap_to_bytes(BitmapObject *self) {
    char *bytes = new_array(char, self->size);
    // PyErr_SetString(PyExc_OverflowError, "Overflow error");
    long i = 0;
    for(; i < (self->size); i++){
        long ttemp = _byte_to_int(&self->data[i]);
        bytes[i] = (char)ttemp;
    }
    return PyBytes_FromStringAndSize(bytes, self->size);
}

static int bitmap_init(BitmapObject *self, PyObject *args, PyObject *kwds) {
    PyObject *size_or_bits_obj = NULL;
    static char *kwlist[] = {"size_or_bits", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &size_or_bits_obj)) {
        return -1;
    }

    if (PyLong_Check(size_or_bits_obj)) {
        // Initialize with an integer (size of the bitmap)
        self->size = (PyLong_AsUnsignedLongLong(size_or_bits_obj) + 7) / 8;
        if (PyErr_Occurred()) {
            return -1;  // If PyLong_AsLong failed, return -1
        }

        self->data = new_array(Byte_t, self->size);
        if (self->data == NULL) {
            PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for bitmap data");
            return -1;
        }

        for (int i = 0; i < self->size; i++) {
            init_byte(&self->data[i]);
        }
    } else if (PySequence_Check(size_or_bits_obj)) {
        // Initialize with a sequence of booleans
        Py_ssize_t seq_length = PySequence_Size(size_or_bits_obj);
        if (seq_length == -1) {
            return -1;  // If PySequence_Size failed, return -1
        }

        self->size = (seq_length + 7) / 8;  // Calculate the number of bytes needed
        self->data = new_array(Byte_t, self->size);
        if (self->data == NULL) {
            PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for bitmap data");
            return -1;
        }

        for (int i = 0; i < seq_length; i++) {
            PyObject *item = PySequence_GetItem(size_or_bits_obj, i);
            bool value = PyObject_IsTrue(item);
            _bitmap_set_bit(self, i, value);
            Py_DECREF(item);
        }
    } else {
        PyErr_SetString(PyExc_TypeError, "Expected an integer or a sequence of booleans");
        return -1;
    }

    return 0;  // Initialization successful
}




static PyObject* bitmap_set_bit(BitmapObject *self, PyObject *args) {
    printf("%d\n", (self == NULL));
    printf("%d\n", (self->data == NULL));
    ull index;
    bool value;
    if (!PyArg_ParseTuple(args, "Kb", &index, &value)) {
        return NULL;
    }
    check_and_error(index, 0, self->size, self->size);
    _bitmap_set_bit(self, index, value);
    Py_RETURN_NONE;
}

static PyObject* bitmap_set_bits(BitmapObject *self, PyObject *args) {
    ll start, end, step;
    bool on;
    if(!PyArg_ParseTuple(args, "kkkb", &start, &end, &step, &on)){
        PyErr_BadArgument();
    }
    if (step == 0)PyErr_SetString(PyExc_ValueError, "Step cannot be zero");
    if (end < 0)end += self->size;
    if (start < 0)start += self->size;

    if (step < 0 && start < end){
        PyErr_SetString(PyExc_ValueError, "Step cannot be negative when start is less than end");
    }
    if (step > 0 && start > end){
        PyErr_SetString(PyExc_ValueError, "Step cannot be positive when start is greater than end");
    }
    check_and_error(start, 0, self->size, self->size);
    for(ull i = start; i < end; i += step)_bitmap_set_bit(self, i, on);
}

static PyObject* bitmap_get_bit(BitmapObject *self, PyObject *args) {
    ll index;
    if (!PyArg_ParseTuple(args, "k", &index)) {
        return NULL;
    }
    fix_index_error(index, self->size);
    check_and_error(index, 0, self->size, self->size);
    bool value = _bitmap_get_bit(self, index);
    return PyBool_FromLong(value);
}

static PyObject* bitmap_get_size(BitmapObject *self) {
    return PyLong_FromLong(self->size);
}

static PyObject* bitmap_byte_at(BitmapObject *self, PyObject* args){
    ll indexl;
    if (!PyArg_ParseTuple(args, "k", &indexl)){
        return NULL;
    };
    if (indexl < 0){
        indexl = self->size + indexl;
    }
    if (indexl < 0 || indexl >= self->size){
        PyErr_SetString(PyExc_IndexError, "Index out of range");
    }
    PyObject* result = PyLong_FromLong(_byte_to_int(&self->data[indexl/8]));
    if (PyErr_Occurred()){
        return NULL;
    }
    return result;
}



static void bitmap_dealloc(BitmapObject *self) {
    free(self->data);
    Py_TYPE(self)->tp_free((PyObject *)self);
}



static PyMethodDef BitmapMethods[] = {
    {"_C_set_bit", (PyCFunction)bitmap_set_bit, METH_VARARGS, "Set a bit in the bitmap"},
    {"_C_get_bit", (PyCFunction)bitmap_get_bit, METH_VARARGS, "Get a bit from the bitmap"},
    {"_C_get_size", (PyCFunction)bitmap_get_size, METH_NOARGS, "Get the size of the bitmap"},
    {"_C_to_bytes", (PyCFunction)bitmap_to_bytes, METH_NOARGS, "Convert the bitmap to bytes"},
    {"_C_byte_at", (PyCFunction)bitmap_byte_at, METH_VARARGS, "Get a byte from the bitmap"},
    {NULL, NULL, 0, NULL}
};


static PyMethodDef ByteMethods[] = {
    {"_C_set_bit", (PyCFunction)byte_set_bit, METH_VARARGS, "Set a range of bits in the bitmap"},
    {"_C_get_bit", (PyCFunction)byte_get_bit, METH_VARARGS, "Get a range of bits from the bitmap"},
    {NULL, NULL, 0, NULL}
};



static PyTypeObject BitmapType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Bitmap",
    .tp_doc = "Bitmap objects",
    .tp_basicsize = sizeof(BitmapObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)bitmap_init,
    .tp_dealloc = (destructor)bitmap_dealloc,
    .tp_methods = BitmapMethods,
};



static struct PyModuleDef bitmapmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "bitmap",
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1,
    .m_methods = NULL,
    .m_slots = NULL,
    .m_traverse = NULL,
    .m_clear = NULL,
    .m_free = NULL,
};

#define MODULE_NAME hybitmap
#define MODULE_INIT(ModuleName) PyInit_##ModuleName

PyMODINIT_FUNC PyInit_hybitmap(void) {
    PyObject *m;
    if (PyType_Ready(&BitmapType) < 0) {
        return NULL;
    }
    m = PyModule_Create(&bitmapmodule);
    if (m == NULL) {
        return NULL;
    }
    Py_INCREF(&BitmapType);
    if (PyModule_AddObject(m, "Bitmap", (PyObject *)&BitmapType) < 0) {
        Py_DECREF(&BitmapType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}