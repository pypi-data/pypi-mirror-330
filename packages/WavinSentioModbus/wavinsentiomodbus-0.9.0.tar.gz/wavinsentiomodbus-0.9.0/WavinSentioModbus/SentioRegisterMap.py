from enum import Enum



class RegisterType(Enum):
    DISCRETE_INPUT = 0
    INPUT_REGISTER = 1
    HOLDING_REGISTER = 2
    INPUT_REGISTER_MULT = 10
    
class RegisterDataType(Enum):
    NUMERIC = 0
    STRING = 1
    VAL_D2FP100 = 10

class RegisterObjectType(Enum):
    GENERIC = 0
    ROOM = 1
    DEHUMIDIFIERS = 10
    ITC_CIRCUIT = 20


class RegisterRepresentation:

    def __init__(
            self, 
            _regType: RegisterType,
            _address: int,
            _count: int,
            _dataType: RegisterDataType = RegisterDataType.NUMERIC,
            _objectType: RegisterObjectType = RegisterObjectType.GENERIC
    ):
        self.regType = _regType
        self.address = _address
        self.count = _count
        self.dataType = _dataType
        self.objectType = _objectType
        pass

    def __str__(self):
        return "Address:{0}, Type:{1}, Count:{2}, DataType:{3}, ObjectType:{4}".format(self.address, self.regType, self.count, self.dataType, self.objectType)

class SentioRegisterMap:
    DeviceType          = RegisterRepresentation(RegisterType.INPUT_REGISTER, 10, 1)
    DeviceHwVersion     = RegisterRepresentation(RegisterType.INPUT_REGISTER, 11, 1)
    DeviceSwVersion     = RegisterRepresentation(RegisterType.INPUT_REGISTER, 12, 1)
    DeviceSwVersionMinor= RegisterRepresentation(RegisterType.INPUT_REGISTER, 13, 1)
    DeviceSerialNrPrefix= RegisterRepresentation(RegisterType.INPUT_REGISTER, 14, 1)
    DeviceSerialNumber  = RegisterRepresentation(RegisterType.INPUT_REGISTER, 15, 2)
    ModbusMode          = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 5, 1)

    HCSourceState       = RegisterRepresentation(RegisterType.INPUT_REGISTER, 8101, 1)
    #Room Registers
    RoomTempSetpoint    = RegisterRepresentation(RegisterType.INPUT_REGISTER, 101, 1,  _dataType=RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomAirTempActual   = RegisterRepresentation(RegisterType.INPUT_REGISTER, 104, 1,  _dataType=RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomFloorTempActual = RegisterRepresentation(RegisterType.INPUT_REGISTER, 105, 1,  _dataType=RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomRelHumidity     = RegisterRepresentation(RegisterType.INPUT_REGISTER, 106, 1,  _dataType=RegisterDataType.VAL_D2FP100,  _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomCalcDewPoint    = RegisterRepresentation(RegisterType.INPUT_REGISTER, 107, 1,  _dataType=RegisterDataType.VAL_D2FP100,  _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomHeatingState    = RegisterRepresentation(RegisterType.INPUT_REGISTER, 102, 1,  _objectType = RegisterObjectType.ROOM) #101, 201, 301 - 2401
    RoomBlockingReason  = RegisterRepresentation(RegisterType.INPUT_REGISTER, 103, 1,  _objectType = RegisterObjectType.ROOM)

    RoomName            = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 101, 16, _dataType = RegisterDataType.STRING, _objectType = RegisterObjectType.ROOM)
    RoomModeOverride    = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 118, 1, _dataType = RegisterDataType.NUMERIC, _objectType = RegisterObjectType.ROOM)
    RoomTempSetpChange  = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 119, 1, _dataType = RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM)
    RoomTempSetpVacation= RegisterRepresentation(RegisterType.HOLDING_REGISTER, 121, 1, _dataType = RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM)
    RoomTempSetpStandby = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 122, 1, _dataType = RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ROOM)
    RoomMode            = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 117, 1, _objectType = RegisterObjectType.ROOM)
    RoomPresetMode      = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 135, 1, _objectType = RegisterObjectType.ROOM)
    

    OutdoorTemperature  = RegisterRepresentation(RegisterType.INPUT_REGISTER,   3301, 1, _dataType = RegisterDataType.VAL_D2FP100)
    
    #CMV Registers
    CMVDeviceName       = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 61001, 32, RegisterDataType.STRING)
    CMVVentilationState = RegisterRepresentation(RegisterType.INPUT_REGISTER, 61023, 1)

    #DHW
    DHWDeviceName       = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 6501, 32, RegisterDataType.STRING)

    #Dehumidifier
    DehumDeviceName     = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 65001, 32, RegisterDataType.STRING, _objectType = RegisterObjectType.DEHUMIDIFIERS)

    #ITC
    Itc_Name                = RegisterRepresentation(RegisterType.HOLDING_REGISTER, 7301, 32, RegisterDataType.STRING, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_State               = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7301, 1, RegisterDataType.NUMERIC, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_PumpState           = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7304, 1, RegisterDataType.NUMERIC, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_InletTempMeasured   = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7305, 1, RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_InletTempDesired    = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7306, 1, RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_ReturnTemperature   = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7307, 1, RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ITC_CIRCUIT)
    Itc_SupplierTemperature = RegisterRepresentation(RegisterType.INPUT_REGISTER, 7308, 1, RegisterDataType.VAL_D2FP100, _objectType = RegisterObjectType.ITC_CIRCUIT)
    
