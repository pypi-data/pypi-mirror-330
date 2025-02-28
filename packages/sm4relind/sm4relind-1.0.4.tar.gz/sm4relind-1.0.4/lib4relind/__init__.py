import smbus2 as smbus

# bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x38  # 7 bit address (will be left shifted to add the read write bit)
ALTERNATE_DEVICE_ADDRESS = 0x20

RELAY4_INPORT_REG_ADD = 0x00
RELAY4_OUTPORT_REG_ADD = 0x01
RELAY4_POLINV_REG_ADD = 0x02
RELAY4_CFG_REG_ADD = 0x03

relayMaskRemap = [0x80, 0x40, 0x20, 0x10]
relayChRemap = [7, 6, 5, 4]
optoMaskRemap = [0x08, 0x04, 0x02, 0x01]
optoChRemap = [3, 2, 1, 0]

# CPU type card
I2C_MEM_RELAY_VAL = 0x00
I2C_MEM_AC_IN = 0x04
SLAVE_OWN_ADDRESS_BASE = 0x0e
CARD_TYPE_IO_EXP = 0
CARD_TYPE_CPU = 1

cardType = CARD_TYPE_IO_EXP


def __relayToIO(relay):
    val = 0
    for i in range(0, 4):
        if (relay & (1 << i)) != 0:
            val = val + relayMaskRemap[i]
    return val


def __IOToRelay(iov):
    val = 0
    for i in range(0, 4):
        if (iov & relayMaskRemap[i]) != 0:
            val = val + (1 << i)
    return val


def __IOToOpto(iov):
    val = 0
    for i in range(0, 4):
        if (iov & optoMaskRemap[i]) == 0:
            val = val + (1 << i)
    return val


def __optoToIO(opto):
    val = 0
    for i in range(0, 4):
        if (opto & (1 << i)) == 0:
            val = val + optoMaskRemap[i]
    return val


def __check(bus, add):
    global cardType
    cfg = bus.read_byte_data(add, RELAY4_CFG_REG_ADD)
    if SLAVE_OWN_ADDRESS_BASE <= add < (SLAVE_OWN_ADDRESS_BASE + 8):
        cardType = CARD_TYPE_CPU
        return bus.read_byte_data(add, I2C_MEM_RELAY_VAL)
    if cfg != 0x0f:
        bus.write_byte_data(add, RELAY4_CFG_REG_ADD, 0x0f)
        bus.write_byte_data(add, RELAY4_OUTPORT_REG_ADD, 0)
    return bus.read_byte_data(add, RELAY4_INPORT_REG_ADD)


def __ident(bus, stack):
    if stack < 0 or stack > 7:
        raise ValueError('Invalid stack level')
    st = stack  # for hw versions less than 1.1 (stack & 0x02) + (0x01 & (stack >> 2)) + (0x04 & (stack << 2))
    stack = 0x07 ^ st
    hwAdd = DEVICE_ADDRESS + stack
    try:
        oldVal = __check(bus, hwAdd)
    except Exception as e:
        hwAdd = ALTERNATE_DEVICE_ADDRESS + stack
        try:
            oldVal = __check(bus, hwAdd)
        except Exception as e:
            hwAdd = SLAVE_OWN_ADDRESS_BASE + st
            try:
                oldVal = __check(bus, hwAdd)
            except Exception as e:
                bus.close()
                raise RuntimeError("Unable to communicate with 4relind with exception " + str(e))
    return hwAdd, oldVal


def set_relay(stack, relay, value):
    if relay < 1 or relay > 4:
        raise ValueError('Invalid relay number')
    bus = smbus.SMBus(1)
    hwAdd, oldVal = __ident(bus, stack)
    try:
        if cardType == CARD_TYPE_CPU:
            if value == 0:
                oldVal = oldVal & (~(1 << (relay - 1)))
                bus.write_byte_data(hwAdd, I2C_MEM_RELAY_VAL, oldVal)
            else:
                oldVal = oldVal | (1 << (relay - 1))
                bus.write_byte_data(hwAdd, I2C_MEM_RELAY_VAL, oldVal)
        else:
            oldVal = __IOToRelay(oldVal)
            if value == 0:
                oldVal = oldVal & (~(1 << (relay - 1)))
                oldVal = __relayToIO(oldVal)
                bus.write_byte_data(hwAdd, RELAY4_OUTPORT_REG_ADD, oldVal)
            else:
                oldVal = oldVal | (1 << (relay - 1))
                oldVal = __relayToIO(oldVal)
                bus.write_byte_data(hwAdd, RELAY4_OUTPORT_REG_ADD, oldVal)
    except Exception as e:
        bus.close()
        raise RuntimeError("Unable to communicate with 4relind with exception " + str(e))
    bus.close()


def set_relay_all(stack, value):
    bus = smbus.SMBus(1)
    hwAdd, oldVal = __ident(bus, stack)
    try:
        if cardType == CARD_TYPE_CPU:
            bus.write_byte_data(hwAdd, I2C_MEM_RELAY_VAL, value)
        else:
            value = __relayToIO(value)
            bus.write_byte_data(hwAdd, RELAY4_OUTPORT_REG_ADD, value)
    except Exception as e:
        bus.close()
        raise RuntimeError("Unable to communicate with 4relind with exception " + str(e))
    bus.close()


def get_relay(stack, relay):
    if relay < 1 or relay > 4:
        raise ValueError('Invalid relay number')
    bus = smbus.SMBus(1)
    hwAdd, val = __ident(bus, stack)
    bus.close()
    if cardType == CARD_TYPE_IO_EXP:
        val = __IOToRelay(val)
    val = val & (1 << (relay - 1))
    if val == 0:
        return 0
    return 1


def get_relay_all(stack):
    bus = smbus.SMBus(1)
    hwAdd, val = __ident(bus, stack)
    bus.close()
    if cardType == CARD_TYPE_IO_EXP:
        val = __IOToRelay(val)
    return val


def get_opto(stack, channel):
    if channel < 1 or channel > 4:
        raise ValueError('Invalid opto channel number')
    bus = smbus.SMBus(1)
    hwAdd, val = __ident(bus, stack)
    if cardType == CARD_TYPE_CPU:
        try:
            val = bus.read_byte_data(hwAdd, I2C_MEM_AC_IN)
        except Exception as e:
            bus.close()
            raise RuntimeError("Unable to communicate with 4relind with exception " + str(e))
    bus.close()
    if cardType == CARD_TYPE_IO_EXP:
        val = __IOToOpto(val)
    val = val & (1 << (channel - 1))
    if val == 0:
        return 0
    return 1


def get_opto_all(stack):
    bus = smbus.SMBus(1)
    hwAdd, val = __ident(bus, stack)
    if cardType == CARD_TYPE_CPU:
        try:
            val = bus.read_byte_data(hwAdd, I2C_MEM_AC_IN)
        except Exception as e:
            bus.close()
            raise RuntimeError("Unable to communicate with 4relind with exception " + str(e))
    bus.close()
    if cardType == CARD_TYPE_IO_EXP:
        val = __IOToOpto(val)
    return val
