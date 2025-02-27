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


cdef void do_nothing(Model model)  noexcept nogil:
    pass

cpdef get_wrapper():
    cdef CallbackWrapper wrapper = CallbackWrapper()
    wrapper.callback = do_nothing
    return wrapper

@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class ReceiverSequences:
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "waterlevel":
            self.waterlevel = pointer.p_value
    cpdef get_value(self, str name):
        cdef numpy.int64_t idx
        if name == "waterlevel":
            return self.waterlevel[0]
    cpdef set_value(self, str name, value):
        if name == "waterlevel":
            self.waterlevel[0] = value
@cython.final
cdef class Model(masterinterface.MasterInterface):
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.run()
    cpdef void reset_reuseflags(self) noexcept nogil:
        pass
    cpdef inline void run(self) noexcept nogil:
        pass
    cpdef inline void update_inlets(self) noexcept nogil:
        pass
    cpdef inline void update_outlets(self) noexcept nogil:
        pass
    cpdef inline void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.get_waterlevel_v1()
    cpdef inline void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        pass
    cpdef double get_waterlevel_v1(self) noexcept nogil:
        return self.sequences.receivers.waterlevel[0]
    cpdef double get_waterlevel(self) noexcept nogil:
        return self.sequences.receivers.waterlevel[0]
