#!python
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
# cython: cpow=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
from typing import Optional
import numpy
cimport numpy
from libc.math cimport exp, fabs, log, sin, cos, tan, asin, acos, atan, isnan, isinf
from libc.math cimport NAN as nan
from libc.math cimport INFINITY as inf
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen cimport interfaceutils
from hydpy.cythons.autogen cimport interputils
from hydpy.cythons.autogen import pointerutils
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport quadutils
from hydpy.cythons.autogen cimport rootutils
from hydpy.cythons.autogen cimport smoothutils
from hydpy.cythons.autogen cimport masterinterface
ctypedef void (*CallbackType) (Model)  noexcept nogil
cdef class CallbackWrapper:
    cdef CallbackType callback
@cython.final
cdef class Sequences:
    cdef public ReceiverSequences receivers
@cython.final
cdef class ReceiverSequences:
    cdef double *waterlevel
    cdef public numpy.int64_t _waterlevel_ndim
    cdef public numpy.int64_t _waterlevel_length
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value)
    cpdef get_value(self, str name)
    cpdef set_value(self, str name, value)
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cdef public Sequences sequences
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil
    cpdef void reset_reuseflags(self) noexcept nogil
    cpdef inline void run(self) noexcept nogil
    cpdef inline void update_inlets(self) noexcept nogil
    cpdef inline void update_outlets(self) noexcept nogil
    cpdef inline void update_receivers(self, numpy.int64_t idx) noexcept nogil
    cpdef inline void update_senders(self, numpy.int64_t idx) noexcept nogil
    cpdef inline void update_outputs(self) noexcept nogil
    cpdef double get_waterlevel_v1(self) noexcept nogil
    cpdef double get_waterlevel(self) noexcept nogil
