#!/usr/bin/env python3

ActualAnalogInputs = {
    "Analog1": {"dxsId": 167772417, "unit": "V"},
    "Analog2": {"dxsId": 167772673, "unit": "V"},
    "Analog3": {"dxsId": 167772929, "unit": "V"},
    "Analog4": {"dxsId": 167773185, "unit": "V"},
}

ActualBattery = {
    "Voltage": {"dxsId": 33556226, "unit": "V"},
    "Charge": {"dxsId": 33556229, "unit": "%"},
    "Current": {"dxsId": 33556238, "unit": "A"},
    "BatteryStatus": {"dxsId": 33556230, "unit": ""},
    "ChargeCycles": {"dxsId": 33556228, "unit": ""},
    "Temperature": {"dxsId": 33556227, "unit": "°C"},
}

BatteryStatusCodes = {0: "Charging", 1: "Discharging"}

ActualGrid = {
    "GridOutputPower": {"dxsId": 67109120, "unit": "W"},
    "GridFreq": {"dxsId": 67110400, "unit": "Hz"},
    "GridCosPhi": {"dxsId": 67110656, "unit": ""},
    "GridLimitation": {"dxsId": 67110144, "unit": "%"},
    "GridVoltageL1": {"dxsId": 67109378, "unit": "V"},
    "GridCurrentL1": {"dxsId": 67109377, "unit": "A"},
    "GridPowerL1": {"dxsId": 67109379, "unit": "W"},
    "GridVoltageL2": {"dxsId": 67109634, "unit": "V"},
    "GridCurrentL2": {"dxsId": 67109633, "unit": "A"},
    "GridPowerL2": {"dxsId": 67109635, "unit": "W"},
    "GridVoltageL3": {"dxsId": 67109890, "unit": "V"},
    "GridCurrentL3": {"dxsId": 67109889, "unit": "A"},
    "GridPowerL3": {"dxsId": 67109891, "unit": "W"},
}

ActualHouse = {
    "ActHomeConsumptionSolar": {"dxsId": 83886336, "unit": "W"},
    "ActHomeConsumptionBat": {"dxsId": 83886592, "unit": "W"},
    "ActHomeConsumptionGrid": {"dxsId": 83886848, "unit": "W"},
    "PhaseSelHomeConsumpL1": {"dxsId": 83887106, "unit": "W"},
    "PhaseSelHomeConsumpL2": {"dxsId": 83887362, "unit": "W"},
    "PhaseSelHomeConsumpL3": {"dxsId": 83887618, "unit": "W"},
}

ActualPVGenerator = {
    "dc1Voltage": {"dxsId": 33555202, "unit": "V"},
    "dc1Current": {"dxsId": 33555201, "unit": "A"},
    "dc1Power": {"dxsId": 33555203, "unit": "W"},
    "dc2Voltage": {"dxsId": 33555458, "unit": "V"},
    "dc2Current": {"dxsId": 33555457, "unit": "A"},
    "dc2Power": {"dxsId": 33555459, "unit": "W"},
    "dc3Voltage": {"dxsId": 33555714, "unit": "V"},
    "dc3Current": {"dxsId": 33555713, "unit": "A"},
    "dc3Power": {"dxsId": 33555715, "unit": "W"},
}

ActualSZeroIn = {
    "S0InPulseCnt": {"dxsId": 184549632, "unit": ""},
    "Loginterval": {"dxsId": 150995968, "unit": "s"},
}

Home = {
    "dcPowerPV": {"dxsId": 33556736, "unit": "W"},
    "acPower": {"dxsId": 67109120, "unit": "W"},
    "selfConsumption": {"dxsId": 83888128, "unit": "W"},
    "batStateOfCharge": {"dxsId": 33556229, "unit": "%"},
    # TODO: statusCodes
    "operatingStatus": {"dxsId": 16780032, "unit": ""},
}

OperatingStatusCodes = {0: "0", 1: "1", 2: "Starting", 3: "Feed In"}

InfoVersions = {
    "VersionUI": {"dxsId": 16779267, "unit": ""},
    "VersionFW": {"dxsId": 16779265, "unit": ""},
    "VersionHW": {"dxsId": 16779266, "unit": ""},
    "VersionPAR": {"dxsId": 16779268, "unit": ""},
    "SerialNumber": {"dxsId": 16777728, "unit": ""},
    "ArticleNumber": {"dxsId": 16777472, "unit": ""},
    "CountrySettingsName": {"dxsId": 16779522, "unit": ""},
    "CountrySettingsVersion": {"dxsId": 16779521, "unit": ""},
}

StatisticDay = {
    "Yield": {"dxsId": 251658754, "unit": "Wh"},
    "HomeConsumption": {"dxsId": 251659010, "unit": "Wh"},
    "SelfConsumption": {"dxsId": 251659266, "unit": "Wh"},
    "SelfConsRate": {"dxsId": 251659278, "unit": "%"},
    "AutonomyDegree": {"dxsId": 251659279, "unit": "%"},
}

StatisticTotal = {
    "Yield": {"dxsId": 251658753, "unit": "Wh"},
    "OperatingTime": {"dxsId": 251658496, "unit": "h"},
    "HomeConsumption": {"dxsId": 251659009, "unit": "Wh"},
    "SelfConsumption": {"dxsId": 251659265, "unit": "Wh"},
    "SelfConsRate": {"dxsId": 251659280, "unit": "%"},
    "AutonomyDegree": {"dxsId": 251659281, "unit": "%"},
}
