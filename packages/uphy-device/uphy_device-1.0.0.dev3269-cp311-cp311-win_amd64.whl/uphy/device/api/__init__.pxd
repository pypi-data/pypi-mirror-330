from libc cimport stdint
from libc.stdint cimport uint8_t, uint32_t, int32_t, uint16_t, uint64_t
from libcpp cimport bool

# Generated mostly using autopxd
cdef extern from "up_api.h":

    cpdef enum up_dtype_t:
        UP_DTYPE_INT8
        UP_DTYPE_UINT8
        UP_DTYPE_INT16
        UP_DTYPE_UINT16
        UP_DTYPE_INT32
        UP_DTYPE_UINT32
        UP_DTYPE_REAL32

    cpdef enum up_core_status_t:
        UP_CORE_CONNECTED
        UP_CORE_CONFIGURED
        UP_CORE_RUNNING

    cpdef enum up_signal_status_t:
        UP_STATUS_OK

    cpdef enum up_error_t:
        UP_ERROR_NONE
        UP_ERROR_CORE_COMMUNICATION
        UP_ERROR_PARAMETER_WRITE
        UP_ERROR_PARAMETER_READ
        UP_ERROR_INVALID_PROFINET_MODULE_ID
        UP_ERROR_INVALID_PROFINET_SUBMODULE_ID
        UP_ERROR_INVALID_PROFINET_PARAMETER_INDEX

    cpdef enum up_transport_t:
        UP_TRANSPORT_SPI
        UP_TRANSPORT_UART
        UP_TRANSPORT_USB
        UP_TRANSPORT_TCP
        UP_TRANSPORT_INVALID

    cpdef enum up_event_t:
        UP_EVENT_AVAIL
        UP_EVENT_SYNC
        UP_EVENT_PARAM_WRITE_IND
        UP_EVENT_STATUS_IND
        UP_EVENT_MESSAGE_IND
        UP_EVENT_MASK_FREE_RUNNING_MODE
        UP_EVENT_MASK_SYNCHRONOUS_MODE
        UP_EVENT_ALL

    cpdef enum up_signal_flags_t:
        UP_SIG_FLAG_IS_ARRAY

    cpdef enum up_message_id_t:
        UP_MESSAGE_ID_ERROR
        UP_MESSAGE_ID_PROFINET_SIGNAL_LED

    cpdef enum up_perm_t:
        UP_PERM_RO
        UP_PERM_RW

    cpdef enum up_bustype_t:
        UP_BUSTYPE_MOCK
        UP_BUSTYPE_PROFINET
        UP_BUSTYPE_ECAT
        UP_BUSTYPE_ETHERNETIP
        UP_BUSTYPE_MODBUS

    cpdef enum up_alarm_level_t:
        UP_ALARM_ERROR
        UP_ALARM_WARNING
        UP_ALARM_INFO

    cdef struct list_uint8_1_t:
        uint8_t * elements
        uint32_t elementsCount

    cdef struct binary_t:
        uint8_t* data
        uint32_t dataLength

    cdef struct up_signal_info_t:
        uint8_t* value
        up_signal_status_t* status

    cdef union up_message_params_t:
        uint32_t error_code
        uint8_t dummy

    cdef struct up_message_t:
        int32_t id
        up_message_params_t params

    cdef struct up_signal_t:
        char* name
        uint16_t ix
        up_dtype_t datatype
        uint16_t bitlength
        uint16_t frame_offset
        uint32_t flags
        uint64_t default_value
        uint64_t min_value
        uint64_t max_value

    cdef struct up_frame_info_t:
        uint16_t total_size
        uint16_t status_offset

    cdef struct up_param_t:
        char* name
        uint16_t ix
        up_dtype_t datatype
        uint16_t bitlength
        uint16_t frame_offset
        uint32_t flags
        uint32_t permissions
        binary_t default_value
        binary_t min_value
        binary_t max_value

    cdef struct up_alarm_t:
        up_alarm_level_t level
        uint16_t error_code

    cdef struct up_slot_t:
        char* name
        uint16_t n_inputs
        up_signal_t* inputs
        uint16_t input_bitlength
        uint16_t n_outputs
        up_signal_t* outputs
        uint16_t output_bitlength
        uint16_t n_params
        up_param_t* params

    cdef struct up_slot_cfg_t:
        char* name
        uint16_t input_bitlength
        uint16_t output_bitlength
        uint16_t n_inputs
        uint16_t n_outputs
        uint16_t n_params

    cdef struct up_pn_param_t:
        uint32_t pn_index

    cdef struct up_pn_module_t:
        uint32_t module_id
        uint32_t submodule_id
        uint16_t n_params
        up_pn_param_t* params

    cdef struct up_pn_slot_t:
        uint16_t module_ix

    cdef struct up_profinet_config_t:
        uint16_t vendor_id
        uint16_t device_id
        uint32_t dap_module_id
        uint32_t dap_identity_submodule_id
        uint32_t dap_interface_submodule_id
        uint32_t dap_port_1_submodule_id
        uint32_t dap_port_2_submodule_id
        uint16_t profile_id
        uint16_t profile_specific_type
        uint16_t min_device_interval
        char* default_stationname
        char* order_id
        uint16_t hw_revision
        uint8_t sw_revision_prefix
        uint8_t sw_revision_functional_enhancement
        uint8_t sw_revision_bug_fix
        uint8_t sw_revision_internal_change
        uint16_t revision_counter
        uint16_t n_modules
        uint16_t n_slots
        up_pn_module_t* modules
        up_pn_slot_t* slots

    cdef struct up_ciaobject_t:
        uint16_t index
        uint8_t subindex
        bool is_signal
        uint16_t signal_or_param_ix

    cdef struct up_ciapdo_t:
        char* name
        uint16_t index
        uint8_t n_entries
        up_ciaobject_t* entries

    cdef struct up_ecat_module_t:
        uint32_t profile
        uint8_t n_rxpdos
        uint8_t n_txpdos
        uint8_t n_objects
        up_ciapdo_t* rxpdos
        up_ciapdo_t* txpdos
        up_ciaobject_t* objects

    cdef struct up_ecat_slot_t:
        uint8_t module_ix

    cdef struct up_ecat_device_t:
        uint32_t profile
        uint32_t vendor
        uint32_t productcode
        uint32_t revision
        uint32_t serial
        char* hw_rev
        char* sw_rev
        uint16_t pdo_increment
        uint16_t index_increment
        uint8_t n_modules
        uint8_t n_slots
        up_ecat_module_t* modules
        up_ecat_slot_t* slots

    cdef struct up_mockadapter_config_t:
        uint8_t vendor_id

    cdef struct up_ethernetip_config_t:
        uint16_t vendor_id
        uint16_t device_type
        uint16_t product_code
        uint8_t major_revision
        uint8_t minor_revision
        uint32_t min_data_interval
        uint32_t default_data_interval
        uint16_t input_assembly_id
        uint16_t output_assembly_id
        uint16_t config_assembly_id
        uint16_t input_only_heartbeat_assembly_id
        uint16_t listen_only_heartbeat_assembly_id

    cdef struct up_modbus_config_t:
        uint8_t id
        uint16_t port

    cdef union up_busconf_t:
        up_mockadapter_config_t mock
        up_profinet_config_t profinet
        up_ecat_device_t ecat
        up_ethernetip_config_t ethernetip
        up_modbus_config_t modbus

    cdef struct up_local_config_t:
        char* serial_number
        bool webgui_enable

    cdef struct up_device_t:
        char* name
        up_local_config_t cfg
        up_bustype_t bustype
        uint16_t n_slots
        up_slot_t* slots

    cdef struct up_device_cfg_t:
        char* name
        up_local_config_t cfg
        uint16_t n_slots

    ctypedef struct up_t:
        pass

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_avail_ft)(up_t* up, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_sync_ft)(up_t* up, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_param_write_ind_ft)(up_t* up, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_poll_ind_ft)(up_t* up, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_status_ind_ft)(up_t* up, uint32_t status, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_error_ind_ft)(up_t* up, up_error_t error, void* user_arg)  noexcept nogil

    ctypedef void (*_up_cfg_t_up_cfg_t_up_cfg_profinet_signal_led_ind_ft)(up_t* up, void* user_arg)  noexcept nogil

    cdef struct up_cfg:
        up_device_t* device
        up_busconf_t* busconf
        up_signal_info_t* vars
        _up_cfg_t_up_cfg_t_up_cfg_avail_ft avail
        _up_cfg_t_up_cfg_t_up_cfg_sync_ft sync
        _up_cfg_t_up_cfg_t_up_cfg_param_write_ind_ft param_write_ind
        _up_cfg_t_up_cfg_t_up_cfg_poll_ind_ft poll_ind
        _up_cfg_t_up_cfg_t_up_cfg_status_ind_ft status_ind
        _up_cfg_t_up_cfg_t_up_cfg_error_ind_ft error_ind
        _up_cfg_t_up_cfg_t_up_cfg_profinet_signal_led_ind_ft profinet_signal_led_ind
        void* cb_arg

    ctypedef up_cfg up_cfg_t

    const char* up_version() nogil

    up_t* up_init(const up_cfg_t* cfg) nogil

    const up_cfg_t* up_get_cfg(up_t* up) nogil

    void up_pack_input_frame(up_t* up, uint8_t* frame) nogil

    void up_unpack_output_frame(up_t* up, uint8_t* frame) nogil

    void up_read_outputs(up_t* up) nogil

    void up_write_inputs(up_t* up) nogil

    int up_param_get_write_req(up_t* up, uint16_t* slot_ix, uint16_t* param_ix, binary_t* param) nogil

    int up_write_param(up_t* up, uint16_t slot_ix, uint16_t param_ix, binary_t* param) nogil

    int up_read_param(up_t* up, uint16_t slot_ix, uint16_t param_ix, binary_t* param) nogil

    int up_add_alarm(up_t* up, uint16_t slot_ix, const up_alarm_t* alarm) nogil

    int up_remove_alarm(up_t* up, uint16_t slot_ix, const up_alarm_t* alarm) nogil

    uint32_t up_read_status(up_t* up) nogil

    int up_rpc_init(up_t* up) nogil

    int up_rpc_start(up_t* up, bool reset_core) nogil

    int up_init_device(up_t* up) nogil

    int up_start_device(up_t* up) nogil

    int up_enable_watchdog(up_t* up, bool enable) nogil

    int up_write_ecat_eeprom(up_t* up, const uint8_t* data, uint16_t size) nogil

    void up_event_ind() nogil

    bool up_worker(up_t* up) except+ nogil

    int up_tcp_transport_init(up_t* up, const char* ip, uint16_t port) nogil

    int up_spi_master_transport_init(up_t* up, const char* name) nogil

    int up_uart_transport_init(up_t* up, const char* name) nogil

    int up_serial_transport_init(up_t* up, const char* name) nogil


cdef extern from "up_util.h":
    int up_util_init (up_device_t * device, up_t * up, up_signal_info_t * up_vars) nogil

cdef extern from "osal_log.h":
    ctypedef void (*os_log_t) (uint8_t type, const char * fmt, ...) nogil
    os_log_t os_log


cdef class MemoryHolder:
    cdef void * _ptr
    cdef bool   _own
    cdef size_t _size
    cdef size_t _count

    cdef void * ptr(self)
    cdef void   borrow(self, void * ptr, size_t count)
    cdef void   reserve(self, size_t count)

cdef class MemoryObject:
    cdef MemoryHolder _mem

cdef class Signal():
    cdef up_signal_t _obj
    cdef bytes _name
    cdef up_signal_t * ptr(self)

    cdef void *               _value
    cdef up_signal_status_t * _status


cdef class Param():
    cdef up_param_t _obj
    cdef bytes _name
    cdef up_param_t * ptr(self)

    cdef void *               _value


cdef class SignalInfo:
    cdef up_signal_info_t _obj
    cdef up_signal_info_t * ptr(self)


cdef class SignalInfos():
    cdef up_signal_info_t * _ptr
    cdef bool               _own
    cdef list[SignalInfo]   _infos
    cdef up_signal_info_t * ptr(self)

cdef class Device:
    cdef up_device_t * _ptr
    cdef bool          _own
    cdef up_device_t * ptr(self)
    cdef dict[str, Slot] _slots
    cdef MemoryHolder    _slots_mem
    cdef bytes         _name
    cdef bool          _webgui_enable
    cdef bytes         _serial_number

cdef class BusConfig():
    cdef MemoryHolder   _mem
    cdef up_bustype_t   _bustype
    cdef up_busconf_t * ptr(self)

cdef class ProfinetSlot():
    cdef MemoryHolder      _mem
    cdef up_pn_slot_t  *   _ptr

    cdef up_pn_slot_t *    ptr(self)


cdef class ProfinetParam():
    cdef MemoryHolder       _mem
    cdef up_pn_param_t  *   _ptr

    cdef up_pn_param_t *    ptr(self)

cdef class ProfinetModule():
    cdef MemoryHolder        _mem
    cdef up_pn_module_t *    _ptr
    cdef list[ProfinetParam] _params
    cdef MemoryHolder        _params_mem

    cdef up_pn_module_t * ptr(self)


cdef class ProfinetConfig(BusConfig):
    cdef up_profinet_config_t * _ptr
    cdef list[ProfinetModule]   _modules
    cdef MemoryHolder           _modules_mem

    cdef list[ProfinetSlot]     _slots
    cdef MemoryHolder           _slots_mem

    cdef bytes                  _default_stationname
    cdef bytes                  _order_id




cdef class EthercatSlot():
    cdef MemoryHolder       _mem
    cdef up_ecat_slot_t  *  _ptr

    cdef up_ecat_slot_t *  ptr(self)


cdef class CiaObject():
    cdef MemoryHolder       _mem
    cdef up_ciaobject_t  *  _ptr

    cdef up_ciaobject_t *  ptr(self)


cdef class CiaPdo():
    cdef MemoryHolder       _mem
    cdef up_ciapdo_t  *     _ptr
    cdef MemoryHolder       _entries_mem
    cdef list[CiaObject]    _entries
    cdef bytes              _name


    cdef up_ciapdo_t *      ptr(self)


cdef class EthercatModule():
    cdef MemoryHolder        _mem
    cdef up_ecat_module_t *  _ptr

    cdef MemoryHolder       _rxpdos_mem
    cdef list[CiaPdo]       _rxpdos

    cdef MemoryHolder       _txpdos_mem
    cdef list[CiaPdo]       _txpdos

    cdef MemoryHolder       _objects_mem
    cdef list[CiaObject]    _objects

    cdef up_ecat_module_t *  ptr(self)



cdef class EthercatDevice(BusConfig):

    cdef bytes _hw_rew
    cdef bytes _sw_rew

    cdef up_ecat_device_t  *  _ptr

    cdef MemoryHolder         _modules_mem
    cdef list[EthercatModule] _modules

    cdef MemoryHolder         _slots_mem
    cdef list[EthercatSlot]   _slots



cdef class ModbusDevice(BusConfig):

    cdef up_modbus_config_t * _ptr


cdef class EthernetIPConfig(BusConfig):

    cdef up_ethernetip_config_t * _ptr



cdef class Slot:
    cdef up_slot_t _obj
    cdef bytes   _name

    cdef MemoryHolder      _inputs_mem
    cdef dict[str, Signal] _inputs

    cdef MemoryHolder      _outputs_mem
    cdef dict[str, Signal] _outputs

    cdef MemoryHolder      _params_mem
    cdef dict[str, Param]  _params

    cdef up_slot_t * ptr(self)
