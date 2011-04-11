//-----------------------------------------------------------------------------
// Python interface for patching arrays of the same size
//-----------------------------------------------------------------------------

#include <Python.h>
// #include <bzlib.h>
// 
// static void read_data_gz(char* fileName, char* buffer, int len) {
//         FILE * f;
//         BZFILE * pfbz2;
//         int bz2err;
//         
//         /* Open patch file */
//         if ((f = fopen(fileName, "r")) == NULL)
//                 /* error */;
//         
//         pfbz2 = BZ2_bzReadOpen(&bz2err, f, 0, 0, NULL, 0);
//         
//         BZ2_bzRead(&bz2err, pfbz2, buffer, len);
//         
//         BZ2_bzReadClose(&bz2err, pfbz2);
//         
//         fclose(f);
// }
// 
// static void read_data_bz(char* fileName, char* buffer, int len) {
//     int length, bufsize=0, res=SZ_OK;
//     
//     if (!PyArg_ParseTuple(args, "|i", &bufsize))
//         return NULL;
// 
//     while (!bufsize || self->outStream.size < (size_t) bufsize)
//     {
//         Py_BEGIN_ALLOW_THREADS
//         res = LzmaEnc_CodeOneBlock(self->encoder, False, 0, 0);
//         Py_END_ALLOW_THREADS
//         if (res != SZ_OK || LzmaEnc_IsFinished(self->encoder)) {
//             break;
//         }
//     }
//     
//     if (LzmaEnc_IsFinished(self->encoder)) {
//         LzmaEnc_Finish(self->encoder);
//     }
//     
//     if (bufsize)
//         length = min((size_t) bufsize, self->outStream.size);
//     else
//         length = self->outStream.size;
//     
//     result = PyString_FromStringAndSize((const char *)self->outStream.data, length);
//     if (result == NULL) {
//         PyErr_NoMemory();
//         goto exit;
//     }
//     
//     MemoryOutStreamDiscard(&self->outStream, length);
// 
// exit:
// 
//     return result;
// }
/*
//-----------------------------------------------------------------------------
// Patch()
//   Takes the original array and the patch filename and returns the new data.
//-----------------------------------------------------------------------------
static PyObject* patch_bz(
    PyObject* self,			// passthrough argument
    PyObject* args)			// arguments to function
{
    char *origData, *newData, *fileName;
    int dataLength;
    PyObject *results;
    int i;
    
    // parse arguments: s# is the buffer an its length, s stands from the filename string
    if (!PyArg_ParseTuple(args, "s#s", &origData, &dataLength, &fileName))
        return NULL;

    // allocate the memory for the new data
    newData = PyMem_Malloc(dataLength);
    if (!newData)
        return PyErr_NoMemory();

    read_data(fileName, newData, dataLength);
    // now newData has the diff data, after adding the old data it will have the real new data
    
    for (i = 0; i < dataLength; i++) {
        newData[i] = (char) (origData[i] + newData[i]);
    }
    
    results = PyString_FromStringAndSize(newData, dataLength);
    PyMem_Free(newData);
    return results;
}*/

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
    
    for (i = 0; i < dataLength; i++) {
        newData[i] = (char) (origData[i] + newData[i]);
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
