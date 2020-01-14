//-----------------------------------------------------------------------------
// Python interface for patching arrays of the same size
//-----------------------------------------------------------------------------

#include <Python.h>

//-----------------------------------------------------------------------------
// Patch()
//   Takes the original array and the patch array and returns the new data.
//-----------------------------------------------------------------------------
static PyObject* patch(
    PyObject* self,                     // passthrough argument
    PyObject* args)                     // arguments to function
{
    char *origData, *newData, *diffData;
    int dataLength, diffLength;
    PyObject *results;
    int i;
    
    // parse arguments: s# is the buffer an its length, s stands from the filename string
    if (!PyArg_ParseTuple(args, "s#s#", &origData, &dataLength, &diffData, &diffLength))
        return NULL;

    // allocate the memory for the new data
    newData = PyMem_Malloc(dataLength);
    if (!newData)
        return PyErr_NoMemory();

    // int round
    int *origDataInt = (int*)origData;
    int *newDataInt = (int*)newData;
    int *diffDataInt = (int*)diffData;
    int intLength = dataLength/4;
    for (i = 0; i < intLength; i++) {
        newDataInt[i] = origDataInt[i] ^ diffDataInt[i]; // Patch with XOR
    }

    // byte round (rest of the int round)
    int byteRest = dataLength - intLength*4;
    for (i = 0; i < byteRest; i++) {
        newData[i] = origData[i] ^ diffData[i]; // Patch with XOR
    }
    
    results = PyString_FromStringAndSize(newData, dataLength);
    PyMem_Free(newData);
    return results;
}

//-----------------------------------------------------------------------------
//   Declaration of methods supported by this module
//-----------------------------------------------------------------------------
static PyMethodDef g_ModuleMethods[] = {
    { "patch", patch, METH_VARARGS },
    { NULL, NULL }
};

//-----------------------------------------------------------------------------
// initbsdiff()
//   Initialization routine for the shared libary.
//-----------------------------------------------------------------------------
void initimagepatch(void)
{
    PyObject *module, *moduleDict;

    // initialize module and retrieve the dictionary
    module = Py_InitModule("imagepatch", g_ModuleMethods);
    if (!module)
        return;
    moduleDict = PyModule_GetDict(module);
    if (!moduleDict)
        return;

    // set version for easier support
    if (PyDict_SetItemString(moduleDict, "version",
            PyString_FromString("1.0")) < 0)
        return;
}
