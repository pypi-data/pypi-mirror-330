import logging 
#Api regisers and defaults
from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException, ParameterException
from pymodbus.pdu import ExceptionResponse
import struct

#import Defaults
from .Defaults import Defaults
from .SentioRegisterMap import *
from .SentioTypes import *

class ModbusWrapper:

    def __init__(self, _client, slaveId):
        self.client = _client
        self.slaveId = slaveId

    def registers_to_string(self, registers):
        """Converts Modbus registers (list of 16-bit values) to a UTF-8 string."""
        byte_array = b"".join(struct.pack(">H", reg) for reg in registers)  # Pack each register as big-endian
        return byte_array[:44].decode("utf-8").rstrip("\x00")  # Decode and remove null padding

    def writeRegister(self, registerMapObject, value, _subIndex = 0):
        returnValue = 0
        
        try:
            address = registerMapObject.address
            if(registerMapObject.objectType == RegisterObjectType.ROOM):
                logging.debug("Detected Room Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.regType == RegisterType.INPUT_REGISTER):
                logging.error("Not possible to write input reg")
            elif(registerMapObject.regType == RegisterType.DISCRETE_INPUT):
                logging.error("Not possible to write discrete input reg")
            elif(registerMapObject.regType == RegisterType.HOLDING_REGISTER):
                returnValue = self.client.write_register(address, value, slave=self.slaveId)
        except Exception as e:
            logging.exception("error occured ==>  {0}".format(e))
            returnValue = -1
        return returnValue


    def readRegister(self, registerMapObject, _subIndex = 0):
        returnValue = None
        logging.debug("Reading {0}".format(registerMapObject))
        try:
            address = registerMapObject.address
            if(registerMapObject.objectType == RegisterObjectType.ROOM):
                logging.debug("Detected Room Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.objectType == RegisterObjectType.DEHUMIDIFIERS):
                logging.debug("Detected Dehumidifier Object {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address
            if(registerMapObject.objectType == RegisterObjectType.ITC_CIRCUIT):
                logging.debug("Detected ITC Circuit {0} - {1}".format(address, _subIndex))
                address = (_subIndex * 100) + address


            if(registerMapObject.regType == RegisterType.INPUT_REGISTER):
                response = self.client.read_input_registers(address, count=registerMapObject.count, slave=self.slaveId)
                if not response.isError(): 
                    if(registerMapObject.dataType == RegisterDataType.NUMERIC):
                        if(registerMapObject.count == 1):
                            returnValue = response.registers[0]
                        else:
                            if(registerMapObject.count == 2):
                                returnValue = self.client.convert_from_registers(response.registers, data_type=self.client.DATATYPE.INT32)
                            elif(registerMapObject.count == 4):
                                returnValue = self.client.convert_from_registers(response.registers, data_type=self.client.DATATYPE.INT64)
                            else:
                                logging.error("Unsupported decoding format {0}".format(registerMapObject.count))
                    elif(registerMapObject.dataType == RegisterDataType.STRING):
                        logging.info(f"Read string {0}".format(response.registers))
                        
                        if isinstance(response, ExceptionResponse) or not response or not hasattr(response, "registers"):
                            print(f"Modbus Error: {response}")
                            return None

                        returnValue = self.registers_to_string(response.registers)
                    elif(registerMapObject.dataType == RegisterDataType.VAL_D2FP100):
                        if(registerMapObject.count == 1):
                            
                            fp100value = response.registers[0]
                            if fp100value > 0xF000: #most likely negative
                                fp100value = 0xFFFF - fp100value
                                fp100value = fp100value * -1
                                logging.debug("Detected abnormal high value {0} {1} {2}".format(fp100value, 0xFFFF - fp100value, 0xF000))
        
                            returnValue = float(fp100value / 100)
                            logging.debug("Registers: {0} {1} {2}".format(response.registers[0], float(0x7FFF), 0x7FFF))
                            logging.debug("Found {0} -> /100 = {1}".format(fp100value, returnValue))
                        else:
                            logging.error("Unsupported count for Holding Registers {0} D2_FP100".format(registerMapObject.count))

                    else:
                        logging.error("No support yet for Input Register with {0} type".format(registerMapObject.regType))
                else:
                    logging.debug("Error while reading register {0} type INPUT".format(address)) #not really error, could be register is not used. just return error
                    returnValue = None
                #logging.error("Read InputReg complete {0}".format(returnValue))
            elif(registerMapObject.regType == RegisterType.DISCRETE_INPUT):
                logging.error("Discrete Input type {0} - {1}".format(address, registerMapObject.count))
            
            elif(registerMapObject.regType == RegisterType.HOLDING_REGISTER):
                #logging.error("Holding Register type {0} - {1}".format(registerMapObject.address, registerMapObject.count))
                response = self.client.read_holding_registers(address, count=registerMapObject.count, slave=self.slaveId)
                if not response.isError(): 
                    if(registerMapObject.dataType == RegisterDataType.NUMERIC):
                        if(registerMapObject.count == 1):
                            returnValue = response.registers[0]
                        else:
                            logging.error("Unsupported count for Holding Registers {0} Numeric".format(registerMapObject.count))
                    elif(registerMapObject.dataType == RegisterDataType.STRING):
                        if isinstance(response, ExceptionResponse) or not response or not hasattr(response, "registers"):
                            print(f"Modbus Error: {response}")
                            return None

                        returnValue = self.registers_to_string(response.registers)
                        
                        
                    elif(registerMapObject.dataType == RegisterDataType.VAL_D2FP100):
                        if(registerMapObject.count == 1):
                            fp100value = response.registers[0]
                            if fp100value > 0xF000: #most likely negative
                                fp100value = 0xFFFF - fp100value
                                fp100value = fp100value * -1
                                logging.debug("Detected abnormal high value {0} {1} {2}".format(fp100value, 0xFFFF - fp100value, 0xF000))
        
                            returnValue = fp100value / 100
                            logging.info("Found {0} -> /100 = {1}".format(fp100value, returnValue))
                        else:
                            logging.error("Unsupported count for Holding Registers {0} D2_FP100".format(registerMapObject.count))
                else:
                    logging.debug("Error while reading register") #not really error, could be register is not used. just return error
                    returnValue = None
        except Exception as e:
            logging.exception("error occured ==>  {0} for reading address {1}, type {2}".format(e, registerMapObject.address, registerMapObject.regType))
            return None
        return returnValue