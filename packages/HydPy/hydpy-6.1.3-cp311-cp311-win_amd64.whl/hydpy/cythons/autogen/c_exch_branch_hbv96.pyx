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
cdef class Parameters:
    pass
@cython.final
cdef class ControlParameters:
    pass
@cython.final
cdef class DerivedParameters:
    pass
@cython.final
cdef class Sequences:
    pass
@cython.final
cdef class InletSequences:
    cpdef inline alloc(self, name, numpy.int64_t length):
        if name == "total":
            self._total_length_0 = length
            self._total_ready = numpy.full(length, 0, dtype=numpy.int64)
            self.total = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "total":
            PyMem_Free(self.total)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "total":
            self.total[idx] = pointer.p_value
            self._total_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef numpy.int64_t idx
        if name == "total":
            values = numpy.empty(self.len_total)
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                values[idx] = self.total[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "total":
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                self.total[idx][0] = value[idx]
@cython.final
cdef class FluxSequences:
    cpdef inline void load_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._originalinput_diskflag_reading:
            self.originalinput = self._originalinput_ncarray[0]
        elif self._originalinput_ramflag:
            self.originalinput = self._originalinput_array[idx]
        if self._adjustedinput_diskflag_reading:
            self.adjustedinput = self._adjustedinput_ncarray[0]
        elif self._adjustedinput_ramflag:
            self.adjustedinput = self._adjustedinput_array[idx]
        if self._outputs_diskflag_reading:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_ncarray[k]
                k += 1
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_array[idx, jdx0]
    cpdef inline void save_data(self, numpy.int64_t idx)  noexcept nogil:
        cdef numpy.int64_t jdx0
        cdef numpy.int64_t k
        if self._originalinput_diskflag_writing:
            self._originalinput_ncarray[0] = self.originalinput
        if self._originalinput_ramflag:
            self._originalinput_array[idx] = self.originalinput
        if self._adjustedinput_diskflag_writing:
            self._adjustedinput_ncarray[0] = self.adjustedinput
        if self._adjustedinput_ramflag:
            self._adjustedinput_array[idx] = self.adjustedinput
        if self._outputs_diskflag_writing:
            k = 0
            for jdx0 in range(self._outputs_length_0):
                self._outputs_ncarray[k] = self.outputs[jdx0]
                k += 1
        if self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "originalinput":
            self._originalinput_outputpointer = value.p_value
        if name == "adjustedinput":
            self._adjustedinput_outputpointer = value.p_value
    cpdef inline void update_outputs(self) noexcept nogil:
        if self._originalinput_outputflag:
            self._originalinput_outputpointer[0] = self.originalinput
        if self._adjustedinput_outputflag:
            self._adjustedinput_outputpointer[0] = self.adjustedinput
@cython.final
cdef class OutletSequences:
    cpdef inline alloc(self, name, numpy.int64_t length):
        if name == "branched":
            self._branched_length_0 = length
            self._branched_ready = numpy.full(length, 0, dtype=numpy.int64)
            self.branched = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "branched":
            PyMem_Free(self.branched)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, numpy.int64_t idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "branched":
            self.branched[idx] = pointer.p_value
            self._branched_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef numpy.int64_t idx
        if name == "branched":
            values = numpy.empty(self.len_branched)
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                values[idx] = self.branched[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "branched":
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                self.branched[idx][0] = value[idx]
@cython.final
cdef class Model:
    cpdef inline void simulate(self, numpy.int64_t idx)  noexcept nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.update_outlets()
        self.update_outputs()
    cpdef void reset_reuseflags(self) noexcept nogil:
        pass
    cpdef void save_data(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        self.sequences.fluxes.save_data(idx)
    cpdef inline void run(self) noexcept nogil:
        self.calc_adjustedinput_v1()
        self.calc_outputs_v1()
    cpdef inline void update_inlets(self) noexcept nogil:
        self.pick_originalinput_v1()
    cpdef inline void update_outlets(self) noexcept nogil:
        self.pass_outputs_v1()
    cpdef inline void update_receivers(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, numpy.int64_t idx) noexcept nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) noexcept nogil:
        self.sequences.fluxes.update_outputs()
    cpdef inline void pick_originalinput_v1(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.originalinput = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.originalinput = self.sequences.fluxes.originalinput + (self.sequences.inlets.total[idx][0])
    cpdef inline void calc_adjustedinput_v1(self) noexcept nogil:
        self.sequences.fluxes.adjustedinput = self.sequences.fluxes.originalinput + self.parameters.control.delta[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.adjustedinput = max(self.sequences.fluxes.adjustedinput, self.parameters.control.minimum)
    cpdef inline void calc_outputs_v1(self) noexcept nogil:
        cdef double d_dy
        cdef double d_y0
        cdef double d_dx
        cdef double d_x0
        cdef numpy.int64_t bdx
        cdef double d_x
        cdef numpy.int64_t pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.adjustedinput:
                break
        d_x = self.sequences.fluxes.adjustedinput
        for bdx in range(self.parameters.derived.nmbbranches):
            d_x0 = self.parameters.control.xpoints[pdx - 1]
            d_dx = self.parameters.control.xpoints[pdx] - d_x0
            d_y0 = self.parameters.control.ypoints[bdx, pdx - 1]
            d_dy = self.parameters.control.ypoints[bdx, pdx] - d_y0
            self.sequences.fluxes.outputs[bdx] = (d_x - d_x0) * d_dy / d_dx + d_y0
    cpdef inline void pass_outputs_v1(self) noexcept nogil:
        cdef numpy.int64_t bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
    cpdef inline void pick_originalinput(self) noexcept nogil:
        cdef numpy.int64_t idx
        self.sequences.fluxes.originalinput = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.originalinput = self.sequences.fluxes.originalinput + (self.sequences.inlets.total[idx][0])
    cpdef inline void calc_adjustedinput(self) noexcept nogil:
        self.sequences.fluxes.adjustedinput = self.sequences.fluxes.originalinput + self.parameters.control.delta[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.adjustedinput = max(self.sequences.fluxes.adjustedinput, self.parameters.control.minimum)
    cpdef inline void calc_outputs(self) noexcept nogil:
        cdef double d_dy
        cdef double d_y0
        cdef double d_dx
        cdef double d_x0
        cdef numpy.int64_t bdx
        cdef double d_x
        cdef numpy.int64_t pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.adjustedinput:
                break
        d_x = self.sequences.fluxes.adjustedinput
        for bdx in range(self.parameters.derived.nmbbranches):
            d_x0 = self.parameters.control.xpoints[pdx - 1]
            d_dx = self.parameters.control.xpoints[pdx] - d_x0
            d_y0 = self.parameters.control.ypoints[bdx, pdx - 1]
            d_dy = self.parameters.control.ypoints[bdx, pdx] - d_y0
            self.sequences.fluxes.outputs[bdx] = (d_x - d_x0) * d_dy / d_dx + d_y0
    cpdef inline void pass_outputs(self) noexcept nogil:
        cdef numpy.int64_t bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
