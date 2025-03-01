from libc cimport stdint
from libcpp cimport bool
from libc.string cimport memcpy
from typing import TypeAlias, Iterable, Mapping
from cpython.mem cimport PyMem_Calloc, PyMem_Free
import upgen.model.uphy as uphy_model
import rich.repr
import logging

from uphy.device.api cimport up_ecat_slot_t, up_ciaobject_t, up_ciapdo_t, up_ecat_module_t, up_ecat_device_t, MemoryHolder

ValueSingleType: TypeAlias = int | float | None
ValueArrayType: TypeAlias = list[int | None] | list[float | None]

LOG = logging.getLogger(__name__)

def version() -> str:
    return up_version().decode("utf-8")

cdef extern from "stdarg.h":
    ctypedef struct va_list:
        pass
    int vsnprintf (char * s, size_t n, const char * format, va_list arg ) nogil
    void va_start( va_list ap, const char * fmt ) nogil
    void va_end( va_list ap ) nogil

cdef extern from "osal_log.h":
    stdint.uint8_t LOG_LEVEL_DEBUG
    stdint.uint8_t LOG_LEVEL_INFO
    stdint.uint8_t LOG_LEVEL_WARNING
    stdint.uint8_t LOG_LEVEL_ERROR
    stdint.uint8_t LOG_LEVEL_FATAL
    stdint.uint8_t LOG_LEVEL_GET(stdint.uint8_t t)

cdef void os_log_python (stdint.uint8_t type, const char * fmt, ...) noexcept nogil:
    cdef va_list args
    cdef char[1024] buffer
    va_start (args, fmt)
    vsnprintf(buffer, sizeof(buffer), fmt, args)
    va_end (args)

    with gil:
        message = (<const char*>buffer).decode("utf-8").rstrip("\n")
        level = LOG_LEVEL_GET(type)

        if (level == LOG_LEVEL_DEBUG):
            LOG.debug(message)
        elif (level == LOG_LEVEL_INFO):
            LOG.info(message)
        elif (level == LOG_LEVEL_ERROR):
            LOG.error(message)
        elif (level == LOG_LEVEL_FATAL):
            LOG.critical(message)
        else:
            LOG.debug(message)


DTYPE_BITLEN = {
    up_dtype_t.UP_DTYPE_INT8: 8,
    up_dtype_t.UP_DTYPE_UINT8: 8,
    up_dtype_t.UP_DTYPE_INT16: 16,
    up_dtype_t.UP_DTYPE_UINT16: 16,
    up_dtype_t.UP_DTYPE_INT32: 32,
    up_dtype_t.UP_DTYPE_UINT32: 32,
    up_dtype_t.UP_DTYPE_REAL32: 32
}

def _rich_to_plain(obj) -> str:
    args = ", ".join(
        f"{name}={value!r}"
        for name, value in obj.__rich_repr__()
    )
    return f"{obj.__class__.__name__}({args})"


cdef _view_from_array(int bitlength, up_dtype_t datatype, void * value):
        count = bitlength // DTYPE_BITLEN[datatype]

        if datatype == up_dtype_t.UP_DTYPE_UINT8:
            return <stdint.uint8_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_UINT16:
            return <stdint.uint16_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_UINT32:
            return <stdint.uint32_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_INT8:
            return <stdint.int8_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_INT16:
            return <stdint.int16_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_INT32:
            return <stdint.int32_t[:count]>value
        elif datatype == up_dtype_t.UP_DTYPE_REAL32:
            return <float[:count]>value
        else:
            raise Exception("Unknown data type")

class ApiError(Exception):
    pass

cdef class Signal():
    """Data signal representation."""

    def __init__(self, model: uphy_model.Model, signal: uphy_model.Signal, frame_offset: int, ix: int = 0):

        self._name = signal.name.encode("utf-8")
        self._obj = up_signal_t(
            name=self._name,
            ix=ix,
            datatype=up_dtype_t[f"UP_DTYPE_{signal.datatype}"],
            bitlength=signal.bitlen,
            flags=up_signal_flags_t.UP_SIG_FLAG_IS_ARRAY if signal.is_array else 0,
            frame_offset=frame_offset,
            min_value=0,
            max_value=0,
            default_value=0,
        )
        self._value = PyMem_Calloc(1, signal.bitlen)
        self._status = <up_signal_status_t*>PyMem_Calloc(1, sizeof(up_signal_status_t))

    cdef up_signal_t * ptr(self):
        return <up_signal_t *> &self._obj

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        properties={
            p: getattr(self, p)
            for p in dir(self)
            if not p.startswith("_")
        }
        for key, value in properties.items():
            yield key, value

    @property
    def _value_view(self):
        return _view_from_array(self.bitlength, self.datatype, self._value)

    @property
    def values(self) -> ValueArrayType:

        if self._status[0] != up_signal_status_t.UP_STATUS_OK:
            return [None] * self.values_len

        return self._value_view

    @values.setter
    def values(self, values: ValueArrayType) -> None:

        if any(value is None for value in values):
            self._status[0] = <up_signal_status_t>0
            return

        self._status[0] = up_signal_status_t.UP_STATUS_OK

        data = self._value_view
        for ix, value in enumerate(values):
            data[ix] = value

    @property
    def values_len(self) -> int:
        return len(self._value_view)

    @property
    def name(self) -> str:
        if self._obj.name == NULL:
            return None

        return self._obj.name.decode("utf-8")

    @name.setter
    def name(self, value: str) -> None:
        if value is None:
            self._obj.name = NULL
            return

        self._name = value.encode("utf-8")
        self._obj.name = self._name

    @property
    def ix(self) -> int:
        return self._obj.ix

    @ix.setter
    def ix(self, value: int) -> None:
        self._obj.ix = value

    @property
    def flags(self) -> int:
        return self._obj.flags

    @flags.setter
    def flags(self, value: int) -> None:
        self._obj.flags = value

    @property
    def datatype(self) -> up_dtype_t:
        return self._obj.datatype

    @datatype.setter
    def datatype(self, value: up_dtype_t) -> None:
        self._obj.datatype = value

    @property
    def bitlength(self) -> int:
        return self._obj.bitlength

    @bitlength.setter
    def bitlength(self, value: int) -> None:
        self._obj.bitlength = value

    @property
    def frame_offset(self) -> int:
        return self._obj.frame_offset

    @frame_offset.setter
    def frame_offset(self, value: int) -> None:
        self._obj.frame_offset = value

    @property
    def default_value(self) -> stdint.uint64_t:
        return self._obj.default_value

    @default_value.setter
    def default_value(self, value: stdint.uint64_t) -> None:
        self._obj.default_value = value

    @property
    def min_value(self) -> stdint.uint64_t:
        return self._obj.min_value

    @min_value.setter
    def min_value(self, value: stdint.uint64_t) -> None:
        self._obj.min_value = value

    @property
    def max_value(self) -> stdint.uint64_t:
        return self._obj.max_value

    @max_value.setter
    def max_value(self, value: stdint.uint64_t) -> None:
        self._obj.max_value = value


cdef class Param():

    def __init__(self, model: uphy_model.Model, param: uphy_model.Parameter, frame_offset: int, ix: int = 0):

        self._name = param.name.encode("utf-8")
        self._obj = up_param_t(
            name=self._name,
            ix=ix,
            datatype=up_dtype_t[f"UP_DTYPE_{param.datatype}"],
            bitlength=param.bitlen,
            flags=0,
            frame_offset=frame_offset,
            permissions=0, # TODO
            default_value=binary_t(
                data=NULL,
                dataLength=0
            ),
            min_value=binary_t(
                data=NULL,
                dataLength=0
            ),
            max_value=binary_t(
                data=NULL,
                dataLength=0
            ),
        )
        self._value = PyMem_Calloc(1, param.bitlen)

    cdef up_param_t * ptr(self):
        return <up_param_t *> &self._obj

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        properties={
            p: getattr(self, p)
            for p in dir(self)
            if not p.startswith("_")
        }
        for key, value in properties.items():
            yield key, value

    @property
    def _value_view(self):
        return _view_from_array(self.bitlength, self.datatype, self._value)

    @property
    def values(self) -> ValueArrayType | None:
        return self._value_view

    @values.setter
    def values(self, values: ValueArrayType) -> None:

        if any(value is None for value in values):
            raise ValueError("Parameter can't be none")

        data = self._value_view
        for ix, value in enumerate(value):
            data[ix] = value

    @property
    def values_len(self) -> int:
        return len(self._value_view)

    @property
    def name(self):
        if self._obj.name == NULL:
            return None

        return self._obj.name.decode("utf-8")

    @name.setter
    def name(self, value: str) -> None:
        if value is None:
            self._name = None
            self._obj.name = NULL
            return

        self._name = value.encode("utf-8")
        self._obj.name = self._name

    @property
    def ix(self) -> int:
        return self._obj.ix

    @ix.setter
    def ix(self, value: int) -> None:
        self._obj.ix = value

    @property
    def flags(self) -> int:
        return self._obj.flags

    @flags.setter
    def flags(self, value: int) -> None:
        self._obj.flags = value

    @property
    def datatype(self) -> up_dtype_t:
        return self._obj.datatype

    @datatype.setter
    def datatype(self, value: up_dtype_t) -> None:
        self._obj.datatype = value

    @property
    def bitlength(self) -> int:
        return self._obj.bitlength

    @bitlength.setter
    def bitlength(self, value: int) -> None:
        self._obj.bitlength = value

    @property
    def frame_offset(self) -> int:
        return self._obj.frame_offset

    @frame_offset.setter
    def frame_offset(self, value: int) -> None:
        self._obj.frame_offset = value

    @property
    def permissions(self) -> int:
        return self._obj.permissions

    @permissions.setter
    def permissions(self, value: int) -> None:
        self._obj.permissions = value

    # @property
    # def default_value(self) -> Binary:
    #     return self._obj.default_value

    # @default_value.setter
    # def default_value(self, value: Binary) -> None:
    #     self._obj.default_value = value

    # @property
    # def min_value(self) -> Binary
    #     return self._obj.min_value

    # @min_value.setter
    # def min_value(self, value: Binary) -> None:
    #     self._obj.min_value = value

    # @property
    # def max_value(self) -> Binary:
    #     return self._obj.max_value

    # @max_value.setter
    # def max_value(self, value: Binary) -> None:
    #     self._obj.max_value = value


    @property
    def is_array(self) -> bool:
        return self._obj.flags & up_signal_flags_t.UP_SIG_FLAG_IS_ARRAY

    @is_array.setter
    def is_array(self, is_array: bool) -> bool:
        if is_array:
            self._obj.flags |= up_signal_flags_t.UP_SIG_FLAG_IS_ARRAY
        else:
            self._obj.flags &= ~up_signal_flags_t.UP_SIG_FLAG_IS_ARRAY


cdef class SignalInfo:

    cdef up_signal_info_t * ptr(self):
        return &self._obj

    @staticmethod
    def from_signal(Signal signal) -> SignalInfo:
        obj: SignalInfo = <SignalInfo>SignalInfo.__new__(SignalInfo)
        obj._obj.value = <stdint.uint8_t*>signal._value
        obj._obj.status = signal._status
        return obj

    @staticmethod
    def from_param(Param param) -> SignalInfo:
        obj: SignalInfo = <SignalInfo>SignalInfo.__new__(SignalInfo)
        obj._obj.value = <stdint.uint8_t*>param._value
        obj._obj.status = NULL
        return obj


cdef class SignalInfos():
    cdef up_signal_info_t * ptr(self):
        if self._ptr:
            return self._ptr

        self._own = True
        self._ptr = <up_signal_info_t*>PyMem_Calloc(len(self._infos), sizeof(up_signal_info_t))
        if self._ptr == NULL:
            raise MemoryError()

        for ix, slot in enumerate(self._infos):
            self._ptr[ix] = (<SignalInfo>slot).ptr()[0]
        return self._ptr

    def __init__(self, infos: list[SignalInfo] | None = None) -> None:
        self._infos = infos or []

    def __dealloc__(self):
        if self._own:
            PyMem_Free(self._ptr)

    @staticmethod
    def from_slots(slots: Iterable[Slot]) -> SignalInfos:
        obj: SignalInfos = SignalInfos.__new__(SignalInfos)

        fields: list[Signal | Param] = []
        for slot in slots:
            fields.extend(slot.inputs.values())
            fields.extend(slot.outputs.values())
            fields.extend(slot.params.values())

        def info_from_value(value):
            if isinstance(value, Signal):
                return SignalInfo.from_signal(value)
            if isinstance(value, Param):
                return SignalInfo.from_param(value)
            raise ValueError("Unexpected type")

        obj._infos = list(info_from_value(x) for x in fields)
        for ix, field in enumerate(fields):
            field.ix = ix
        return obj

    def __len__(self):
        return len(self._infos)

    def __getitem__(self, ix) -> SignalInfo:
        return self._infos[ix]

cdef class Slot:
    """A slot on a u-phy device."""
    def __cinit__(self, *args, **kwargs):
        self._inputs_mem = MemoryHolder(sizeof(up_signal_t))
        self._outputs_mem = MemoryHolder(sizeof(up_signal_t))
        self._params_mem = MemoryHolder(sizeof(up_param_t))

    def __init__(self, model: uphy_model.Root, slot: uphy_model.Slot, input_offset=0, output_offset=0, parameter_offset=0):
        module = model.get_module(slot.module)

        def _signal_with_offset(signals: list[uphy_model.Signal], bit_offset: int):
            for signal in signals:
                yield Signal(model, signal, frame_offset=bit_offset // 8)
                bit_offset += signal.bitlen

        def _param_with_offset(params: list[uphy_model.Parameter], bit_offset: int):
            for param in params:
                yield Param(model, param, frame_offset=bit_offset // 8)
                bit_offset += param.bitlen

        self._name = slot.name.encode("utf-8")
        self._inputs = {
            signal.name: signal
            for signal in _signal_with_offset(module.inputs, input_offset)
        }

        self._outputs = {
            signal.name: signal
            for signal in _signal_with_offset(module.outputs, output_offset)
        }

        self._params = {
            param.name: param
            for param in _param_with_offset(module.parameters, parameter_offset)
        }

        self._inputs_mem.reserve(len(self._inputs))
        self._outputs_mem.reserve(len(self._outputs))
        self._params_mem.reserve(len(self._params))

        self._obj = up_slot_t(
            name=self._name,
            inputs=<up_signal_t*>self._inputs_mem.ptr(),
            n_inputs = len(self._inputs),
            input_bitlength=module.inputs_bitlen,
            outputs=<up_signal_t*>self._outputs_mem.ptr(),
            n_outputs=len(self._outputs),
            output_bitlength=module.outputs_bitlen,
            n_params=len(self._params),
            params=<up_param_t*>self._params_mem.ptr(),
        )

    cdef up_slot_t * ptr(self):
        cdef up_signal_t * signals
        cdef up_param_t * params

        signals = self._obj.inputs
        for ix, signal in enumerate(self._inputs.values()):
            signals[ix] = (<Signal>signal).ptr()[0]

        signals = self._obj.outputs
        for ix, signal in enumerate(self._outputs.values()):
            signals[ix] = (<Signal>signal).ptr()[0]

        params = self._obj.params
        for ix, param in enumerate(self._params.values()):
            params[ix] = (<Param>param).ptr()[0]

        self._obj.name = self._name
        return & self._obj

    @property
    def name(self):
        return self._name.decode("utf-8")

    @property
    def inputs(self) -> Mapping[str, Signal]:
        return self._inputs

    @property
    def outputs(self) -> Mapping[str, Signal]:
        return self._outputs

    @property
    def params(self) -> Mapping[str, Param]:
        return self._params

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self.name
        if self._inputs:
            yield "input", self._inputs
        if self._outputs:
            yield "outputs", self.outputs
        if self._params:
            yield "params", self.params

cdef class MemoryHolder:
    def __cinit__(self, size_t size = 1) -> None:
        self._ptr  = NULL
        self._own  = False
        self._size = size
        self._count = 0

    cdef void reserve(self, size_t count):
        if self._own:
            PyMem_Free(self._ptr)
        self._ptr   = NULL
        self._own   = False
        self._count = count


    cdef void borrow(self, void * ptr, size_t count):
        self._ptr  = ptr
        self._own  = False
        self._count = count

    cdef void * ptr(self):
        if self._ptr:
            return self._ptr

        if self._count == 0:
            return NULL

        self._own = True
        self._ptr = <up_slot_t*>PyMem_Calloc(self._count, self._size)
        if self._ptr == NULL:
            raise MemoryError()

        return self._ptr

    def __dealloc__(self):
        if self._own:
            PyMem_Free(self._ptr)

cdef class ProfinetParam():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_pn_param_t))

    def __init__(self, model: uphy_model.Root, parameter: uphy_model.Parameter) -> ProfinetParam:
        assert parameter.profinet

        self._mem.reserve(1)
        self._ptr = <up_pn_param_t*>self._mem.ptr()

        self._ptr[0] = up_pn_param_t(
            pn_index=int(parameter.profinet.index, 0)
        )

    cdef up_pn_param_t *    ptr(self):
        return self._ptr

    @property
    def pn_index(self) -> stdint.uint32_t:
        return self._ptr.pn_index

    @pn_index.setter
    def pn_index(self, value: stdint.uint32_t):
        self._ptr.pn_index = value

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "pn_index", self.pn_index


cdef class ProfinetSlot():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_pn_slot_t))

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device, slot: uphy_model.Slot) -> None:
        module = model.get_module(slot.module)
        module_ix = device.get_used_module_index(slot.module, model)

        assert module.profinet

        self._mem.reserve(1)
        self._ptr = <up_pn_slot_t*>self._mem.ptr()
        self._ptr[0] = up_pn_slot_t(
            module_ix=module_ix
        )

    cdef up_pn_slot_t * ptr(self):
        return self._ptr

    @property
    def module_ix(self) -> stdint.uint32_t:
        return self._ptr.module_ix

    @module_ix.setter
    def module_ix(self, value: stdint.uint32_t):
        self._ptr.module_ix = value

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "module_ix", self.module_ix

cdef class BusConfig():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_busconf_t))
        self._bustype = up_bustype_t.UP_BUSTYPE_MOCK

    cdef up_busconf_t * ptr(self):
        return <up_busconf_t *>self._mem.ptr()

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "bustype", self._bustype

    @property
    def bustype(self) -> up_bustype_t:
        return self._bustype

cdef class ProfinetModule():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_pn_module_t))
        self._params_mem = MemoryHolder(sizeof(up_pn_param_t))

    def __init__(self, model: uphy_model.Root, module: uphy_model.Module) -> None:
        assert module.profinet

        self._mem.reserve(1)
        self._ptr = <up_pn_module_t*>self._mem.ptr()

        self._params = [ProfinetParam(model, param) for param in module.parameters]
        self._params_mem.reserve(len(self._params))

        self._ptr[0] = up_pn_module_t(
            module_id=int(module.profinet.module_id, 0),
            submodule_id=int(module.profinet.submodule_id, 0),
            params = NULL,
            n_params = 0
        )

    cdef up_pn_module_t * ptr(self):
        cdef ProfinetParam param
        self._ptr.params = <up_pn_param_t*>self._params_mem.ptr()
        self._ptr.n_params = len(self._params)
        for ix in range(len(self._params)):
            param = self._params[ix]
            self._ptr.params[ix] = param.ptr()[0]

        return self._ptr

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "module_id", self.module_id
        yield "submodule_id", self.submodule_id
        yield "params", self.params

    @property
    def module_id(self) -> stdint.uint32_t:
        return self._ptr.module_id

    @module_id.setter
    def module_id(self, value: stdint.uint32_t):
        self._ptr.module_id = value

    @property
    def submodule_id(self) -> stdint.uint32_t:
        return self._ptr.submodule_id

    @submodule_id.setter
    def submodule_id(self, value: stdint.uint32_t):
        self._ptr.submodule_id = value

    @property
    def params(self) -> list[ProfinetParam]:
        return self._params

    @params.setter
    def params(self, value: list[ProfinetParam]):
        self._params = value
        self._params_mem.reserve(len(value))

cdef class ProfinetConfig(BusConfig):

    def __cinit__(self, *args, **kwargs):
        self._modules_mem = MemoryHolder(sizeof(up_pn_module_t))
        self._slots_mem = MemoryHolder(sizeof(up_pn_slot_t))
        self._bustype = up_bustype_t.UP_BUSTYPE_PROFINET

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device) -> None:

        assert model.profinet
        assert device.profinet

        self._mem.reserve(1)
        self._ptr = <up_profinet_config_t*>self._mem.ptr()

        modules = [
            ProfinetModule(model, module)
            for module in device.get_used_modules(model)
        ]
        slots = [
            ProfinetSlot(model, device, slot)
            for slot in device.slots
        ]

        self._modules_mem.reserve(len(modules))
        self._modules = modules

        self._slots_mem.reserve(len(slots))
        self._slots = slots

        self._default_stationname = device.profinet.default_stationname.encode("utf-8")
        self._order_id = device.profinet.order_id.encode("utf-8")

        self._ptr[0] = up_profinet_config_t(
            vendor_id=int(model.profinet.vendor_id, 0),
            device_id=int(model.profinet.device_id, 0),
            dap_module_id=int(device.profinet.dap_module_id, 0),
            dap_identity_submodule_id=int(device.profinet.dap_identity_submodule_id, 0),
            dap_interface_submodule_id=int(device.profinet.dap_interface_submodule_id, 0),
            dap_port_1_submodule_id=int(device.profinet.dap_port_1_submodule_id, 0),
            dap_port_2_submodule_id=int(device.profinet.dap_port_1_submodule_id, 0),
            profile_id=int(device.profinet.dap_port_1_submodule_id, 0),
            profile_specific_type=int(device.profinet.profile_specific_type, 0),
            min_device_interval=int(device.profinet.min_device_interval, 0),
            default_stationname=self._default_stationname,
            order_id=self._order_id,
            hw_revision=int(device.profinet.hw_revision, 0),
            sw_revision_prefix=ord(device.profinet.sw_revision_prefix),
            sw_revision_functional_enhancement=int(
                device.profinet.sw_revision_functional_enhancement, 0
            ),
            sw_revision_bug_fix=int(device.profinet.sw_revision_bug_fix, 0),
            sw_revision_internal_change=int(device.profinet.sw_revision_internal_change, 0),
            revision_counter=int(device.profinet.revision_counter, 0),
            modules=NULL,
            n_modules=0,
            slots=NULL,
            n_slots=0
        )

    cdef up_busconf_t * ptr(self):
        self._ptr.modules = <up_pn_module_t*>self._modules_mem.ptr()
        self._ptr.n_modules = len(self._modules)

        self._ptr.slots = <up_pn_slot_t*>self._slots_mem.ptr()
        self._ptr.n_slots = len(self._slots)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._modules):
            if &self._ptr.modules[ix] != (<ProfinetModule>element).ptr():
                self._ptr.modules[ix] = (<ProfinetModule>element).ptr()[0]

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._slots):
            if &self._ptr.slots[ix] != (<ProfinetSlot>element).ptr():
                self._ptr.slots[ix] = (<ProfinetSlot>element).ptr()[0]

        return BusConfig.ptr(self)

    @property
    def vendor_id(self) -> stdint.uint16_t:
        return self._ptr.vendor_id

    @vendor_id.setter
    def vendor_id(self, value: stdint.uint16_t):
        self._ptr.vendor_id = value

    @property
    def device_id(self) -> stdint.uint16_t:
        return self._ptr.device_id

    @device_id.setter
    def device_id(self, value: stdint.uint16_t):
        self._ptr.device_id = value

    @property
    def dap_module_id(self) -> stdint.uint32_t:
        return self._ptr.dap_module_id

    @dap_module_id.setter
    def dap_module_id(self, value: stdint.uint32_t):
        self._ptr.dap_module_id = value

    @property
    def dap_identity_submodule_id(self) -> stdint.uint32_t:
        return self._ptr.dap_identity_submodule_id

    @dap_identity_submodule_id.setter
    def dap_identity_submodule_id(self, value: stdint.uint32_t):
        self._ptr.dap_identity_submodule_id = value

    @property
    def dap_interface_submodule_id(self) -> stdint.uint32_t:
        return self._ptr.dap_interface_submodule_id

    @dap_interface_submodule_id.setter
    def dap_interface_submodule_id(self, value: stdint.uint32_t):
        self._ptr.dap_interface_submodule_id = value

    @property
    def dap_port_1_submodule_id(self) -> stdint.uint32_t:
        return self._ptr.dap_port_1_submodule_id

    @dap_port_1_submodule_id.setter
    def dap_port_1_submodule_id(self, value: stdint.uint32_t):
        self._ptr.dap_port_1_submodule_id = value

    @property
    def dap_port_2_submodule_id(self) -> stdint.uint32_t:
        return self._ptr.dap_port_2_submodule_id

    @dap_port_2_submodule_id.setter
    def dap_port_2_submodule_id(self, value: stdint.uint32_t):
        self._ptr.dap_port_2_submodule_id = value

    @property
    def profile_id(self) -> stdint.uint16_t:
        return self._ptr.profile_id

    @profile_id.setter
    def profile_id(self, value: stdint.uint16_t):
        self._ptr.profile_id = value

    @property
    def profile_specific_type(self) -> stdint.uint16_t:
        return self._ptr.profile_specific_type

    @profile_specific_type.setter
    def profile_specific_type(self, value: stdint.uint16_t):
        self._ptr.profile_specific_type = value

    @property
    def min_device_interval(self) -> stdint.uint16_t:
        return self._ptr.min_device_interval

    @min_device_interval.setter
    def min_device_interval(self, value: stdint.uint16_t):
        self._ptr.min_device_interval = value

    @property
    def default_stationname(self) -> str | None:
        if self._ptr.default_stationname == NULL:
            return None
        return self._ptr.default_stationname.decode("utf-8")

    @default_stationname.setter
    def default_stationname(self, value: str):
        self._default_stationname = value.encode("utf-8")
        self._ptr.default_stationname = self._default_stationname

    @property
    def order_id(self) -> str | None:
        if self._ptr.order_id == NULL:
            return None
        return self._ptr.order_id

    @order_id.setter
    def order_id(self, value: str):
        self._order_id = value.encode("utf-8")
        self._ptr.order_id = self._order_id

    @property
    def hw_revision(self) -> stdint.uint16_t:
        return self._ptr.hw_revision

    @hw_revision.setter
    def hw_revision(self, value: stdint.uint16_t):
        self._ptr.hw_revision = value

    @property
    def sw_revision_prefix(self) -> stdint.uint8_t:
        return self._ptr.sw_revision_prefix

    @sw_revision_prefix.setter
    def sw_revision_prefix(self, value: stdint.uint8_t):
        self._ptr.sw_revision_prefix = value

    @property
    def sw_revision_functional_enhancement(self) -> stdint.uint8_t:
        return self._ptr.sw_revision_functional_enhancement

    @sw_revision_functional_enhancement.setter
    def sw_revision_functional_enhancement(self, value: stdint.uint8_t):
        self._ptr.sw_revision_functional_enhancement = value

    @property
    def sw_revision_bug_fix(self) -> stdint.uint8_t:
        return self._ptr.sw_revision_bug_fix

    @sw_revision_bug_fix.setter
    def sw_revision_bug_fix(self, value: stdint.uint8_t):
        self._ptr.sw_revision_bug_fix = value

    @property
    def sw_revision_internal_change(self) -> stdint.uint8_t:
        return self._ptr.sw_revision_internal_change

    @sw_revision_internal_change.setter
    def sw_revision_internal_change(self, value: stdint.uint8_t):
        self._ptr.sw_revision_internal_change = value

    @property
    def revision_counter(self) -> stdint.uint16_t:
        return self._ptr.revision_counter

    @revision_counter.setter
    def revision_counter(self, value: stdint.uint16_t):
        self._ptr.revision_counter = value

    @property
    def modules(self) -> list[ProfinetModule]:
        return self._modules

    @modules.setter
    def modules(self, value: list[ProfinetModule]):
        self._modules = value
        self._modules_mem.reserve(len(value))

    @property
    def slots(self) -> list[ProfinetSlot]:
        return self._slots

    @slots.setter
    def slots(self, value: list[ProfinetSlot]):
        self._slots = value
        self._slots_mem.reserve(len(value))

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield from super().__rich_repr__()
        yield "vendor_id", self.vendor_id
        yield "device_id", self.device_id
        yield "dap_module_id", self.dap_module_id
        yield "dap_identity_submodule_id", self.dap_identity_submodule_id
        yield "dap_interface_submodule_id", self.dap_interface_submodule_id
        yield "dap_port_1_submodule_id", self.dap_port_1_submodule_id
        yield "dap_port_2_submodule_id", self.dap_port_2_submodule_id
        yield "profile_id", self.profile_id
        yield "profile_specific_type", self.profile_specific_type
        yield "min_device_interval", self.min_device_interval
        yield "default_stationname", self.default_stationname
        yield "order_id", self.order_id
        yield "hw_revision", self.hw_revision
        yield "sw_revision_prefix", self.sw_revision_prefix
        yield "sw_revision_functional_enhancement", self.sw_revision_functional_enhancement
        yield "sw_revision_bug_fix", self.sw_revision_bug_fix
        yield "sw_revision_internal_change", self.sw_revision_internal_change
        yield "revision_counter", self.revision_counter
        yield "modules", self.modules
        yield "slots", self.slots

cdef class Device:

    def __cinit__(self, *args, **kwargs):
        self._slots_mem = MemoryHolder(sizeof(up_slot_t))

    cdef up_device_t * ptr(self):
        self._ptr.n_slots = len(self._slots)
        self._slots_mem.reserve(self._ptr.n_slots)
        self._ptr.slots = <up_slot_t*>self._slots_mem.ptr()
        for ix, slot in enumerate(self._slots.values()):
            memcpy(&self._ptr.slots[ix], (<Slot>slot).ptr(), sizeof(up_slot_t))

        self._ptr.name = self._name
        self._ptr.cfg.serial_number = self._serial_number
        self._ptr.cfg.webgui_enable = self._webgui_enable
        return self._ptr

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device) -> None:
        self._own = True
        self._ptr = <up_device_t*>PyMem_Calloc(1, sizeof(up_device_t))
        if self._ptr == NULL:
            raise MemoryError()

        self._name = device.name.encode("utf-8") if device.name else "".encode("utf-8")
        self._serial_number = device.serial.encode("utf-8") if device.serial else "".encode("utf-8")
        self._webgui_enable = device.webgui_enable

        def _slots():
            input_offset = 0
            output_offset = 0
            for slot in device.slots:
                module = model.get_module(slot.module)
                yield Slot(model, slot, input_offset=input_offset, output_offset=output_offset)
                input_offset += module.inputs_bitlen
                output_offset += module.outputs_bitlen

        self._slots = {
            slot.name: slot
            for slot in _slots()
        }
        self._ptr[0] = up_device_t(
            name=self._name,
            cfg=up_local_config_t(
                serial_number=self._serial_number,
                webgui_enable=self._webgui_enable,
            ),
            slots=NULL,
            n_slots=0,
            bustype=up_bustype_t.UP_BUSTYPE_MOCK
        )

    @property
    def name(self) -> str:
        return self._name.decode("utf-8")

    @property
    def serial_number(self) -> str:
        return self._serial_number.decode("utf-8")

    @property
    def webgui_enable(self) -> bool:
        return self._webgui_enable

    @property
    def slots(self) -> dict[str, Slot]:
        return self._slots

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self.name
        yield "serial_number", self.serial_number
        if self.slots:
            yield "slots", self.slots

cdef void _c_avail (up_t * _c_up, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._avail()
        except BaseException as exception:
            up._up_worker_error = exception

@staticmethod
cdef void _c_error_ind (up_t * _c_up, up_error_t error, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._error_ind(error)
        except BaseException as exception:
            up._up_worker_error = exception

@staticmethod
cdef void _c_sync (up_t * _c_up, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._sync()
        except BaseException as exception:
            up._up_worker_error = exception

@staticmethod
cdef void _c_status_ind (up_t * _c_up, stdint.uint32_t status, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._status_ind(status)
        except BaseException as exception:
            up._up_worker_error = exception

@staticmethod
cdef void _c_profinet_signal_led_ind (up_t * _c_up, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._profinet_signal_led_ind()
        except BaseException as exception:
            up._up_worker_error = exception


@staticmethod
cdef void _c_poll_ind (up_t * _c_up, void * user_arg) noexcept nogil:
    with gil:
        up: Up = <Up>user_arg
        try:
            up._poll_ind()
        except BaseException as exception:
            up._up_worker_error = exception

cdef class Up:
    """Connection to U.Phy server."""

    cdef up_t * _c_up
    cdef up_cfg_t _c_cfg

    def _avail(self):
        pass

    def _sync(self):
        pass

    def _status_ind(self, status: int) -> None:
        pass

    def _error_ind(self):
        pass

    def _profinet_signal_led_ind(self):
        pass

    def _poll_ind(self):
        pass

    _busconf: BusConfig
    _device: Device
    _vars: SignalInfos
    _transport: bytes
    _up_worker_error: BaseException | None

    cdef up_t * ptr(self):
        return self._c_up

    def __init__(
            self,
            device: Device,
            vars: SignalInfos,
            busconf: BusConfig,
        ):
        global os_log
        os_log = os_log_python
        self._device = device
        self._vars = vars
        self._busconf = busconf
        self._up_worker_error = None
        self._c_cfg.device = device.ptr()
        self._c_cfg.device[0].bustype = busconf.bustype
        self._c_cfg.busconf = busconf.ptr()
        self._c_cfg.vars = vars.ptr()
        self._c_cfg.sync = _c_avail
        self._c_cfg.error_ind = _c_error_ind
        self._c_cfg.sync = _c_sync
        self._c_cfg.status_ind = _c_status_ind
        self._c_cfg.profinet_signal_led_ind = _c_profinet_signal_led_ind
        self._c_cfg.poll_ind = _c_poll_ind
        self._c_cfg.cb_arg = <void*>self
        self._c_up = up_init(&self._c_cfg)
        if self._c_up is NULL:
            raise MemoryError()

    @property
    def device(self) -> Device:
        return self._device

    def serial_transport_init (self, name: str):
        self._transport = name.encode("utf-8")
        cdef const char * transport = self._transport
        with nogil:
            if up_serial_transport_init(self._c_up, transport) != 0:
                raise ApiError("Failed to start transport")

    def tcp_transport_init(self, ip: str, port: int):
        self._transport = ip.encode("utf-8")
        cdef const char * transport = self._transport
        cdef int _port = port
        with nogil:
            if up_tcp_transport_init(self._c_up, transport, _port) != 0:
                raise ApiError("Failed to start transport")

    def rpc_init(self):
        with nogil:
            if up_rpc_init (self._c_up) != 0:
                raise ApiError("Failed to init rpc")

    def rpc_start(self, reset_core: bool = True):
        with nogil:
            if up_rpc_start (self._c_up, reset_core) != 0:
                raise ApiError("Failed to start rpc")

    def init_device(self):
        with nogil:
            if up_init_device (self._c_up) != 0:
                raise ApiError("Failed to initialize device")

    def enable_watchdog(self, enable: bool):
        with nogil:
            if up_enable_watchdog (self._c_up, enable) != 0:
                raise ApiError("Failed to enable watchdog")

    def write_inputs(self):
        with nogil:
            up_write_inputs (self._c_up)

    def read_outputs(self):
        with nogil:
            up_read_outputs (self._c_up)

    def start_device(self):
        with nogil:
            if up_start_device (self._c_up) != 0:
                raise ApiError("Failed to start device")

    def worker(self) -> bool:
        cdef bool res
        with nogil:
            res = up_worker (self._c_up)
        if (error := self._up_worker_error):
            self._up_worker_error = None
            raise error
        return res


cdef class Util:
    def __cinit__ (self):
        pass

    def init (self, device: Device, up: Up, signal_infos: SignalInfos) -> None:
        if up_util_init (device.ptr(), up.ptr(), signal_infos.ptr()) != 0:
            raise ApiError("Failed initialize variables")


cdef class EthercatSlot():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_ecat_slot_t))

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device, slot: uphy_model.Slot):
        module = model.get_module(slot.module)
        module_ix = device.get_used_module_index(slot.module, model)

        assert module.ethercat

        self._mem.reserve(1)
        self._ptr = <up_ecat_slot_t*>self._mem.ptr()
        self._ptr[0] = up_ecat_slot_t(
            module_ix=module_ix
        )

    cdef up_ecat_slot_t * ptr(self):
        return self._ptr

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "module_ix", self._ptr.module_ix


cdef class CiaObject():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_ciaobject_t))

    def __init__(self, model: uphy_model.Root, object: uphy_model.CiAObject, is_signal: bool, signal_or_param_ix: int):

        self._mem.reserve(1)
        self._ptr = <up_ciaobject_t*>self._mem.ptr()
        self._ptr[0] = up_ciaobject_t(
            index=int(object.index.replace("#", "0"), 0),
            subindex=int(object.subindex, 0),
            is_signal=is_signal,
            signal_or_param_ix=signal_or_param_ix
        )

    cdef up_ciaobject_t * ptr(self):
        return self._ptr

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "index", self._ptr.index
        yield "subindex", self._ptr.subindex
        yield "is_signal", self._ptr.is_signal
        yield "signal_or_param_ix", self._ptr.signal_or_param_ix


cdef class CiaPdo():

    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_ciapdo_t))
        self._entries_mem = MemoryHolder(sizeof(up_ciaobject_t))

    def __init__(self, model: uphy_model.Root, pdo: uphy_model.CiAPDO, index_base: int):

        self._name = pdo.name.encode("utf-8")
        self._mem.reserve(1)
        self._ptr = <up_ciapdo_t*>self._mem.ptr()
        self._ptr[0] = up_ciapdo_t(
            name=self._name,
            index=int(pdo.index.replace("#", "0"), 0),
            n_entries=0,
            entries=NULL
        )
        self._entries_mem.reserve(len(pdo.entries))
        self._entries = [
            CiaObject(model, entry, True, index_base + ix)
            for ix, entry in enumerate(pdo.entries)
        ]

    cdef up_ciapdo_t * ptr(self):
        self._ptr.entries = <up_ciaobject_t*>self._entries_mem.ptr()
        self._ptr.n_entries = len(self._entries)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._entries):
            if &self._ptr.entries[ix] != (<CiaObject>element).ptr():
                self._ptr.entries[ix] = (<CiaObject>element).ptr()[0]

        return self._ptr

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self._ptr.name.decode("utf-8")
        yield "index", self._ptr.index
        yield "entries", self._entries


cdef class EthercatModule():
    def __cinit__(self, *args, **kwargs):
        self._mem = MemoryHolder(sizeof(up_ecat_module_t))
        self._rxpdos_mem = MemoryHolder(sizeof(up_ciapdo_t))
        self._txpdos_mem = MemoryHolder(sizeof(up_ciapdo_t))
        self._objects_mem = MemoryHolder(sizeof(up_ciaobject_t))

    def __init__(self, model: uphy_model.Root, module: uphy_model.Module):

        assert module.ethercat

        self._mem.reserve(1)
        self._ptr = <up_ecat_module_t*>self._mem.ptr()
        self._ptr[0] = up_ecat_module_t(
            profile=int(module.ethercat.profile, 0),
            n_rxpdos = 0,
            n_txpdos = 0,
            n_objects = 0,
            rxpdos = NULL,
            txpdos = NULL,
            objects = NULL,
        )

        def accumulate(pdos: list[uphy_model.CiAPDO]) -> tuple[int, uphy_model.CiAPDO]:
            ix = 0
            for pdo in pdos:
                yield ix, pdo
                ix += len(pdo.entries)

        self._rxpdos_mem.reserve(len(module.ethercat.rxpdo))
        self._rxpdos = [
            CiaPdo(model, pdo, ix)
            for ix, pdo in accumulate(module.ethercat.rxpdo)
        ]

        self._txpdos_mem.reserve(len(module.ethercat.txpdo))
        self._txpdos = [
            CiaPdo(model, pdo, ix)
            for ix, pdo in accumulate(module.ethercat.txpdo)
        ]

        self._objects_mem.reserve(len(module.ethercat.objects))
        self._objects = [
            CiaObject(model, object, False, ix)
            for ix, object in enumerate(module.ethercat.objects)
        ]

    cdef up_ecat_module_t * ptr(self):
        self._ptr.rxpdos = <up_ciapdo_t*>self._rxpdos_mem.ptr()
        self._ptr.n_rxpdos = len(self._rxpdos)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._rxpdos):
            if &self._ptr.rxpdos[ix] != (<CiaPdo>element).ptr():
                self._ptr.rxpdos[ix] = (<CiaPdo>element).ptr()[0]


        self._ptr.txpdos = <up_ciapdo_t*>self._txpdos_mem.ptr()
        self._ptr.n_txpdos = len(self._txpdos)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._txpdos):
            if &self._ptr.txpdos[ix] != (<CiaPdo>element).ptr():
                self._ptr.txpdos[ix] = (<CiaPdo>element).ptr()[0]


        self._ptr.objects = <up_ciaobject_t*>self._objects_mem.ptr()
        self._ptr.n_objects = len(self._objects)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._objects):
            if &self._ptr.objects[ix] != (<CiaObject>element).ptr():
                self._ptr.objects[ix] = (<CiaObject>element).ptr()[0]

        return self._ptr

    def __repr__(self) -> str:
        return _rich_to_plain(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield "profile", self._ptr.profile
        yield "rxpdos", self._rxpdos
        yield "txpdos", self._txpdos
        yield "objects", self._objects


cdef class EthercatDevice(BusConfig):

    def __cinit__(self, *args, **kwargs):
        self._modules_mem = MemoryHolder(sizeof(up_ecat_module_t))
        self._slots_mem = MemoryHolder(sizeof(up_ecat_slot_t))
        self._bustype = up_bustype_t.UP_BUSTYPE_ECAT

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device):

        assert model.ethercat
        assert device.ethercat

        self._hw_rew = device.ethercat.revision.encode("utf-8")
        self._sw_rew = device.ethercat.revision.encode("utf-8")

        self._modules = [
            EthercatModule(model, module)
            for module in device.get_used_modules(model)
        ]
        self._modules_mem.reserve(len(self._modules))

        self._slots = [
            EthercatSlot(model, device, slot)
            for slot in device.slots
        ]
        self._slots_mem.reserve(len(self._slots))

        self._mem.reserve(1)
        self._ptr = &BusConfig.ptr(self).ecat
        self._ptr[0] = up_ecat_device_t(
            profile=int(device.ethercat.profile.replace("#", "0"), 0),
            vendor=int(model.ethercat.vendor_id.replace("#", "0"), 0),
            productcode=int(device.ethercat.product_code.replace("#", "0"), 0),
            revision=int(device.ethercat.revision.replace("#", "0"), 0),
            serial=1,
            hw_rev=self._hw_rew,
            sw_rev=self._sw_rew,
            pdo_increment=16, # TODO
            index_increment=0x0100, # TODO
            n_modules=0,
            n_slots=0,
            modules=NULL,
            slots=NULL,
        )

    cdef up_busconf_t * ptr(self):

        self._ptr.modules = <up_ecat_module_t*>self._modules_mem.ptr()
        self._ptr.n_modules = len(self._modules)

        self._ptr.slots = <up_ecat_slot_t*>self._slots_mem.ptr()
        self._ptr.n_slots = len(self._slots)

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._modules):
            if &self._ptr.modules[ix] != (<EthercatModule>element).ptr():
                self._ptr.modules[ix] = (<EthercatModule>element).ptr()[0]

        # if not based on same ptr, copy data
        for ix, element in enumerate(self._slots):
            if &self._ptr.slots[ix] != (<EthercatSlot>element).ptr():
                self._ptr.slots[ix] = (<EthercatSlot>element).ptr()[0]

        return BusConfig.ptr(self)

    def __rich_repr__(self) -> rich.repr.Result:
        yield from super().__rich_repr__()
        yield "profile", self._ptr.profile
        yield "vendor", self._ptr.vendor
        yield "productcode", self._ptr.productcode
        yield "revision", self._ptr.revision
        yield "serial", self._ptr.serial
        yield "hw_rev", self._ptr.hw_rev.decode("utf-8")
        yield "sw_rew", self._ptr.sw_rev.decode("utf-8")
        yield "pdo_increment", self._ptr.pdo_increment
        yield "index_increment", self._ptr.index_increment
        yield "modules", self._modules
        yield "slots", self._slots



cdef class ModbusDevice(BusConfig):
    DEFAULT_MODBUS_PORT = 502

    def __cinit__(self, *args, **kwargs):
        self._bustype = up_bustype_t.UP_BUSTYPE_MODBUS

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device):

        port = self.DEFAULT_MODBUS_PORT
        if device.modbus and device.modbus.port:
            port = int(device.modbus.port, 0)

        self._mem.reserve(1)

        self._ptr = &BusConfig.ptr(self).modbus
        self._ptr[0] = up_modbus_config_t(
            id=0,
            port=port
        )

    def __rich_repr__(self) -> rich.repr.Result:
        yield from super().__rich_repr__()
        yield "id", self._ptr.id
        yield "port", self._ptr.port


cdef class EthernetIPConfig(BusConfig):

    def __cinit__(self, *args, **kwargs):
        self._bustype = up_bustype_t.UP_BUSTYPE_ETHERNETIP

    def __init__(self, model: uphy_model.Root, device: uphy_model.Device):

        self._mem.reserve(1)

        self._ptr = &BusConfig.ptr(self).ethernetip
        self._ptr[0] = up_ethernetip_config_t(
            vendor_id = int(model.ethernetip.vendor_id, 0),
            device_type = int(device.ethernetip.device_type, 0),
            product_code = int(device.ethernetip.product_code, 0),
            major_revision = int(device.ethernetip.revision.split('.')[0], 0),
            minor_revision = int(device.ethernetip.revision.split('.')[1], 0),
            min_data_interval = int(device.ethernetip.min_data_interval, 0),
            default_data_interval = int(device.ethernetip.default_data_interval, 0),
            input_assembly_id = 100,
            output_assembly_id = 101,
            config_assembly_id = 102,
            input_only_heartbeat_assembly_id = 103,
            listen_only_heartbeat_assembly_id = 104,
       )

    def __rich_repr__(self) -> rich.repr.Result:
         yield "vendor_id", self._ptr.vendor_id
         yield "device_type", self._ptr.device_type
         yield "product_code", self._ptr.product_code
         yield "major_revision", self._ptr.major_revision
         yield "minor_revision", self._ptr.minor_revision
         yield "min_data_interval", self._ptr.min_data_interval
         yield "default_data_interval", self._ptr.default_data_interval
         yield "input_assembly_id", self._ptr.input_assembly_id
         yield "output_assembly_id", self._ptr.output_assembly_id
         yield "config_assembly_id", self._ptr.config_assembly_id
         yield "input_only_heartbeat_assembly_id", self._ptr.input_only_heartbeat_assembly_id
         yield "listen_only_heartbeat_assembly_id", self._ptr.listen_only_heartbeat_assembly_id
