from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


class SignalCollectionType():
    keyIndicator = 'key_indicator'
    consumption = 'consumption'
    measurement = 'measurement'
    
    _label_map = {
        keyIndicator: "Kennzahlen",
        consumption: "Verbrauchswerte",
        measurement: "Messwerte",
    }
    
    @classmethod
    def get_label(cls, collection_type):
        """Gibt das lesbare Label für einen gegebenen Signaltyp zurück."""
        return cls._label_map.get(collection_type, "Unbekannt")
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
    
    
class SignalType():
    unDef = 'undef'
    measurement = 'measurement'
    occupancy = 'occupancy'
    
    meterReading = 'meter_reading'
    meterReadingRef = 'meter_reading_reference'
    consumption = 'consumption'
    consumptionRef = 'consumption_reference'
    # currentConsumption = 'current_consumption'  # Aktueller Verbrauch (z. B. letzte Stunde)
    # averageConsumption = 'average_consumption'  # Durchschnittsverbrauch über eine bestimmte Zeitspanne
    # peakConsumption = 'peak_consumption'  # Spitzenverbrauch in einer Periode
    # minConsumption = 'min_consumption'  # Minimalverbrauch in einer Periode
    # totalConsumption = 'total_consumption'  # Gesamter Verbrauch über eine Periode
    powerOutput = 'power_output'  # Aktuelle Leistung (z. B. von Solaranlage)
    energyProduction = 'energy_production'  # Gesamtenergieproduktion einer Quelle
    energyProductionRef = 'energy_production_reference'  # Referenzenergieproduktion einer Quelle
    costEstimation = 'cost_estimation'  # Geschätzte Kosten für einen bestimmten Verbrauch
    co2Emissions = 'co2_emissions'  # CO2-Emissionen basierend auf Verbrauchsdaten
    
     # Mapping der Signaltypen zu lesbaren Labels
    _label_map = {
        unDef: "Unbestimmt",
        measurement: "Messwert",
        occupancy: "Belegung",
        meterReading: "Zählerstand",
        meterReadingRef: "Referenzzählerstand",
        consumption: "Verbrauch",
        consumptionRef: "Referenzverbrauch",
        # currentConsumption: "Aktueller Verbrauch",
        # averageConsumption: "Durchschnittsverbrauch",
        # peakConsumption: "Spitzenverbrauch",
        # minConsumption: "Minimalverbrauch",
        # totalConsumption: "Gesamtverbrauch",
        powerOutput: "Leistung",
        energyProduction: "Energieproduktion",
        energyProductionRef: "Referenzenergieproduktion",
        costEstimation: "Kostenabschätzung",
        co2Emissions: "CO2-Emissionen",
    }

    @classmethod
    def get_label(cls, signal_type):
        """Gibt das lesbare Label für einen gegebenen Signaltyp zurück."""
        return cls._label_map.get(signal_type, "Unbekannt")
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
    
class Unit:
    # Allgemein
    un_def = "undef"

    # Energieeinheiten
    watt = "watt"  # Watt
    kilowatt = "kilowatt"
    megawatt = "megawatt"
    gigawatt = "gigawatt"
    wattHour = "watt_hour"
    kilowattHour = "kilowatt_hour"
    megawattHour = "megawatt_hour"
    gigawattHour = "gigawatt_hour"
    joule = "joule"
    kilojoule = "kilojoule"
    megajoule = "megajoule"

    # Leistung (Power)
    voltAmpere = "volt_ampere"
    kilovoltAmpere = "kilovolt_ampere"
    megavoltAmpere = "megavolt_ampere"
    voltAmpereReactive = "volt_ampere_reactive"
    kilovoltAmpereReactive = "kilovolt_ampere_reactive"
    powerFactor = "power_factor"

    # Elektrische Spannung und Stromstärke
    volt = "volt"
    millivolt = "millivolt"
    kilovolt = "kilovolt"
    ampere = "ampere"
    milliampere = "milliampere"
    kiloampere = "kiloampere"
    ohm = "ohm"

    # Frequenz
    hertz = "hertz"
    kilohertz = "kilohertz"
    megahertz = "megahertz"

    # Gas- und Wassereinheiten
    cubic_meter = "cubic_meter"
    liter = "liter"
    milliliter = "milliliter"
    gallon = "gallon"

    # Druck
    pascal = "pascal"
    kilopascal = "kilopascal"
    bar = "bar"

    # Temperatur
    celsius = "celsius"
    fahrenheit = "fahrenheit"
    kelvin = "kelvin"

    # CO2-Emissionen
    gramCo2 = "gram_co2"
    kilogramCo2 = "kilogram_co2"
    tonCo2 = "ton_co2"

    # Zeitangaben
    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"

    # Mapping für lesbare Labels
    _label_map = {
        un_def: "Unbestimmt",
        watt: "W",
        kilowatt: "kW",
        megawatt: "MW",
        gigawatt: "GW",
        wattHour: "Wh",
        kilowattHour: "kWh",
        megawattHour: "MWh",
        gigawattHour: "GWh",
        joule: "J",
        kilojoule: "kJ",
        megajoule: "MJ",
        voltAmpere: "VA",
        kilovoltAmpere: "kVA",
        megavoltAmpere: "MVA",
        voltAmpereReactive: "VAR",
        kilovoltAmpereReactive: "kVAR",
        powerFactor: "PF",
        volt: "V",
        millivolt: "mV",
        kilovolt: "kV",
        ampere: "A",
        milliampere: "mA",
        kiloampere: "kA",
        ohm: "Ω",
        hertz: "Hz",
        kilohertz: "kHz",
        megahertz: "MHz",
        cubic_meter: "m³",
        liter: "L",
        milliliter: "mL",
        gallon: "gal",
        pascal: "Pa",
        kilopascal: "kPa",
        bar: "bar",
        celsius: "°C",
        fahrenheit: "°F",
        kelvin: "K",
        gramCo2: "gCO2",
        kilogramCo2: "kgCO2",
        tonCo2: "tCO2",
        second: "s",
        minute: "min",
        hour: "h",
        day: "d",
        week: "w",
        month: "M",
        year: "Y",
    }


    @classmethod
    def get_label(cls, unit):
        """Gibt das lesbare Label für eine gegebene Einheit zurück."""
        return cls._label_map.get(unit, "Unbekannt")
    
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig sind die Keys 'name' und 'label'.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]
