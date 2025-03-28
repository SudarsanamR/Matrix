import math

# Temperature conversion functions (Kelvin as standard)
def celsius_to_kelvin(c):
    return c + 273.15

def kelvin_to_celsius(k):
    return k - 273.15

def fahrenheit_to_kelvin(f):
    return (f + 459.67) * 5 / 9

def kelvin_to_fahrenheit(k):
    return k * 9 / 5 - 459.67

def rankine_to_kelvin(r):
    return r * 5 / 9

def kelvin_to_rankine(k):
    return k * 9 / 5

# Fuel consumption conversion functions (liter/100km as standard)
fuel_consumption_units = {
    'liter/100km': (lambda x: x, lambda x: x),
    'mpg (us)': (lambda mpg: 235.214583 / mpg, lambda l100: 235.214583 / l100),
    'km/liter': (lambda kmpl: 100 / kmpl, lambda l100: 100 / l100),
    'mpg (imp.)': (lambda mpg: 282.480936 / mpg, lambda l100: 282.480936 / l100),
}

# Conversion factors for categories with multiplicative conversions
# Length (meter as standard)
length_factors = {
    'kilometer': 1000,
    'meter': 1,
    'decimeter': 0.1,
    'centimeter': 0.01,
    'millimeter': 0.001,
    'micron': 1e-6,
    'nanometer': 1e-9,
    'picometer': 1e-12,
    'femtometer': 1e-15,
    'attometer': 1e-18,
    'zeptometer': 1e-21,
    'yoctometer': 1e-24,
    'dekameter': 10,
    'hectometer': 100,
    'megameter': 1e6,
    'gigameter': 1e9,
    'terameter': 1e12,
    'petameter': 1e15,
    'exameter': 1e18,
    'zettameter': 1e21,
    'yottameter': 1e24,
    'mile': 1609.344,
    'yard': 0.9144,
    'foot': 0.3048,
    'inch': 0.0254,
    'mil': 2.54e-5,
    'nautical mile': 1852,
    'li': 500,
    'half marathon': 21097.5,  # 42.195 km / 2 in meters
    'marathon': 42195,
    'parsec': 3.08567758149137e16,
    'milliparsec': 3.08567758149137e13,
    'nanoparsec': 3.08567758149137e7,
    'picoparsec': 3.08567758149137e4,
    'kiloparsec': 3.08567758149137e19,
    'megaparsec': 3.08567758149137e22,
    'gigaparsec': 3.08567758149137e25,
    'teraparsec': 3.08567758149137e28,
    'astronomical unit': 1.495978707e11,
    'light year': 9.4607304725808e15,
    'league': 4828.032,
    'chain': 20.1168,
    'furlong': 201.168,
    'megafurlong': 201168,
    'rod': 5.0292,
    'fathom': 1.8288,
    'smoot': 1.7018,
    'cubit': 0.4572,
    'beard second': 5e-9,
    'angstrom': 1e-10,
}

# Mass (kilogram as standard)
mass_factors = {
    'kilogram': 1,
    'gram': 0.001,
    'decigram': 0.0001,
    'centigram': 0.00001,
    'milligram': 1e-6,
    'microgram': 1e-9,
    'nanogram': 1e-12,
    'picogram': 1e-15,
    'femtogram': 1e-18,
    'dekagram': 0.01,
    'hectogram': 0.1,
    'megagram': 1000,
    'metric ton': 1000,
    'long ton': 1016.0469088,
    'short ton': 907.18474,
    'imperial ton': 1016.0469088,
    'metric quintal': 100,
    'us quintal': 45.359237,
    'french quintal': 100,
    'stone': 6.35029318,
    'pound': 0.45359237,
    'ounce': 0.0283495231,
    'troy ounce': 0.0311034768,
    'slug': 14.5939029,
    'tola': 0.0116638038,
    'dram': 0.0017718452,
    'carat': 0.0002,
    'grain': 6.479891e-05,
    'atomic mass unit': 1.66053906660e-27,
}

# Speed (meter/second as standard)
speed_factors = {
    'mile/hour': 0.44704,
    'kilometer/hour': 0.2777777777777778,
    'foot/second': 0.3048,
    'meter/second': 1,
    'knot': 0.5144444444444444,
    'mach': 340.29,  # More typical value for Mach 1 at sea level
}

# Volume (cubic meter as standard)
volume_factors = {
    'us bushel': 0.0352391,
    'us peck': 0.00880977,
    'us dry gallon': 0.00440488,
    'us gallon': 0.003785411784,
    'us dry quart': 0.00110122,
    'us quad': 0.00110122,  # Assuming typo for quart
    'us dry pint': 0.00055061,
    'us pint': 0.000473176473,
    'us cup': 0.0002365882365,
    'us ounce': 2.957352956e-5,
    'us tablespoon': 1.47867648e-5,
    'us teaspoon': 4.92892159375e-6,
    'us gill': 0.000118294118,
    'us beer barrel': 0.117348,
    'oil barrel': 0.158987294928,
    'imperial bushel': 0.0363687,
    'imperial peck': 0.00909218,
    'imperial gallon': 0.00454609,
    'imperial quart': 0.0011365225,
    'imperial pint': 0.00056826125,
    'imperial ounce': 2.84130625e-5,
    'imperial tbsp': 1.77575781e-5,
    'imperial tsp': 5.91939e-6,
    'nanoliter': 1e-12,
    'microliter': 1e-9,
    'milliliter': 1e-6,
    'centiliter': 1e-5,
    'deciliter': 0.0001,
    'liter': 0.001,
    'decaliter': 0.01,
    'hectoliter': 0.1,
    'kiloliter': 1,
    'megaliter': 1000,
    'cubic nanometer': 1e-27,
    'cubic millimeter': 1e-9,
    'cubic centimeter': 1e-6,
    'cubic decimeter': 0.001,
    'cubic meter': 1,
    'cubic kilometer': 1e9,
    'cubic foot': 0.028316846592,
    'cubic inch': 1.6387064e-5,
    'cubic yard': 0.764554857984,
    'cubic mile': 4.16818183e9,
    'cubic rod': 0.00363054,
    'cord': 3.62456,
    'hogshead': 0.238845,
}

# Area (square meter as standard)
area_factors = {
    'sq. kilometer': 1e6,
    'hectare': 10000,
    'are': 100,
    'sq. meter': 1,
    'square decimeter': 0.01,
    'square centimeter': 0.0001,
    'square millimeter': 1e-6,
    'sq. mile': 2.58998811e6,
    'acre': 4046.8564224,
    'sq. yard': 0.83612736,
    'sq. foot': 0.09290304,
    'sq. inch': 0.00064516,
    'square rod': 25.292956,
    'rood': 1011.7141056,
    'barn': 1e-28,
}

# Time (second as standard)
time_factors = {
    'femtosecond': 1e-15,
    'picosecond': 1e-12,
    'nanosecond': 1e-9,
    'microsecond': 1e-6,
    'millisecond': 0.001,
    'second': 1,
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'week': 604800,
    'fortnight': 1209600,
    'month': 2629800,  # Average month (30.44 days)
    'year': 31557600,  # Julian year
    'sidereal year': 31558149.8,
    'decade': 315576000,
    'century': 3155760000,
    'millennium': 31557600000,
}

# Frequency (hertz as standard)
frequency_factors = {
    'microhertz': 1e-6,
    'millihertz': 0.001,
    'hertz': 1,
    'kilohertz': 1000,
    'megahertz': 1e6,
    'gigahertz': 1e9,
    'terahertz': 1e12,
    'petahertz': 1e15,
    'exahertz': 1e18,
}

# Angle (radian as standard)
angle_factors = {
    'degree': math.pi / 180,
    'radian': 1,
    'milliradian': 0.001,
    'microradian': 1e-6,
    'gradian': math.pi / 200,
    'revolution': 2 * math.pi,
    'arc minute': math.pi / 10800,
    'arc second': math.pi / 648000,
    'milliarcsecond': math.pi / 648000000,
    'microarcsecond': math.pi / 648000000000,
}

# Force (newton as standard)
force_factors = {
    'newton': 1,
    'kilonewton': 1000,
    'dyne': 1e-5,
    'gram-force': 0.00980665,
    'ounce-force': 0.2780139,
    'pound-force': 4.4482216152605,
    'kilogram-force': 9.80665,
    'kip-force': 4448.2216152605,
    'metric ton-force': 9806.65,
}

# Pressure (pascal as standard)
pressure_factors = {
    'barye': 0.1,
    'pascal': 1,
    'millipascal': 0.001,
    'hectopascal': 100,
    'kilopascal': 1000,
    'megapascal': 1e6,
    'gigapascal': 1e9,
    'torr': 133.32236842105263,
    'psi': 6894.757293168361,
    'standard atmosphere': 101325,
    'technical atmosphere': 98066.5,
    'millibar': 100,
    'centibar': 1000,
    'decibar': 10000,
    'bar': 100000,
    'kilobar': 1e8,
    'megabar': 1e11,
    'gigabar': 1e14,
}

# Energy (joule as standard)
energy_factors = {
    'joule': 1,
    'kilojoule': 1000,
    'calorie': 4.184,
    'kilocalorie': 4184,
    'kilowatt hour': 3600000,
    'british thermal unit (btu)': 1055.05585262,
    'erg': 1e-7,
    'foot pound': 1.3558179483314004,
    'electron volt': 1.602176634e-19,
    'decielectron volt': 1.602176634e-20,
    'centielectron volt': 1.602176634e-21,
    'millielectron volt': 1.602176634e-22,
    'microelectron volt': 1.602176634e-25,
    'nanoelectron volt': 1.602176634e-28,
    'picoelectron volt': 1.602176634e-31,
    'femtoelectron volt': 1.602176634e-34,
    'attoelectron volt': 1.602176634e-37,
    'zeptoelectron volt': 1.602176634e-40,
    'yoctoelectron volt': 1.602176634e-43,
    'decaelectron volt': 1.602176634e-18,
    'hectoelectron volt': 1.602176634e-17,
    'kiloelectron volt': 1.602176634e-16,
    'megaelectron volt': 1.602176634e-13,
    'gigaelectron volt': 1.602176634e-10,
    'teraelectron volt': 1.602176634e-7,
    'petaelectron volt': 1.602176634e-4,
    'exaelectron volt': 1.602176634e-1,
    'zettaelectron volt': 1.602176634e2,
    'yottaelectron volt': 1.602176634e5,
}

# Power (watt as standard)
power_factors = {
    'watt': 1,
    'kilowatt': 1000,
    'megawatt': 1e6,
    'gigawatt': 1e9,
    'terawatt': 1e12,
    'petawatt': 1e15,
    'exawatt': 1e18,
    'horsepower': 745.699872,
}

# Electric Current (ampere as standard)
current_factors = {
    'microampere': 1e-6,
    'milliampere': 0.001,
    'ampere': 1,
    'kiloampere': 1000,
    'megaampere': 1e6,
    'gigaampere': 1e9,
    'teraampere': 1e12,
    'petaampere': 1e15,
    'exaampere': 1e18,
}

# Voltage (volt as standard)
voltage_factors = {
    'microvolt': 1e-6,
    'millivolt': 0.001,
    'volt': 1,
    'kilovolt': 1000,
    'megavolt': 1e6,
    'gigavolt': 1e9,
    'teravolt': 1e12,
    'petavolt': 1e15,
    'exavolt': 1e18,
}

# Resistance (ohm as standard)
resistance_factors = {
    'microohm': 1e-6,
    'milliohm': 0.001,
    'ohm': 1,
    'kiloohm': 1000,
    'megaohm': 1e6,
}

# Digital Storage (byte as standard)
digital_storage_factors = {
    'bit': 0.125,
    'nibble': 0.5,
    'byte': 1,
    'kilobit': 125,
    'kibibit': 128,
    'kilobyte': 1000,
    'kibibyte': 1024,
    'megabit': 125000,
    'mebibit': 131072,
    'megabyte': 1e6,
    'mebibyte': 1048576,
    'gigabit': 125000000,
    'gibibit': 134217728,
    'gigabyte': 1e9,
    'gibibyte': 1073741824,
    'terabit': 125000000000,
    'tebibit': 137438953472,
    'terabyte': 1e12,
    'tebibyte': 1099511627776,
    'petabit': 125000000000000,
    'pebibit': 140737488355328,
    'petabyte': 1e15,
    'pebibyte': 1125899906842624,
    'exabit': 1.25e17,
    'exbibit': 144115188075855872 / 1e9,  # approximate conversion factor
    'exabyte': 1e18,
    'exbibyte': 1.152921504606846976e18,
    'zettabit': 1.25e20,
    'zebibit': 1.4757395258969968e20,
    'zettabyte': 1e21,
    'zebibyte': 1.1805916207174113e21,
    'yottabit': 1.25e23,
    'yobibit': 1.511157e23,
    'yottabyte': 1e24,
    'yobibyte': 1.2089258196146292e24,
}

# Categories dictionary
categories = {
    'length': {
        'standard': 'meter',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in length_factors.items()}
    },
    'mass': {
        'standard': 'kilogram',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in mass_factors.items()}
    },
    'temperature': {
        'standard': 'kelvin',
        'units': {
            'celsius': (celsius_to_kelvin, kelvin_to_celsius),
            'fahrenheit': (fahrenheit_to_kelvin, kelvin_to_fahrenheit),
            'kelvin': (lambda x: x, lambda x: x),
            'rankine': (rankine_to_kelvin, kelvin_to_rankine),
        }
    },
    'speed': {
        'standard': 'meter/second',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in speed_factors.items()}
    },
    'volume': {
        'standard': 'cubic meter',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in volume_factors.items()}
    },
    'area': {
        'standard': 'sq. meter',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in area_factors.items()}
    },
    'time': {
        'standard': 'second',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in time_factors.items()}
    },
    'frequency': {
        'standard': 'hertz',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in frequency_factors.items()}
    },
    'angle': {
        'standard': 'radian',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in angle_factors.items()}
    },
    'force': {
        'standard': 'newton',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in force_factors.items()}
    },
    'pressure': {
        'standard': 'pascal',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in pressure_factors.items()}
    },
    'energy': {
        'standard': 'joule',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in energy_factors.items()}
    },
    'power': {
        'standard': 'watt',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in power_factors.items()}
    },
    'electric current': {
        'standard': 'ampere',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in current_factors.items()}
    },
    'voltage': {
        'standard': 'volt',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in voltage_factors.items()}
    },
    'resistance': {
        'standard': 'ohm',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in resistance_factors.items()}
    },
    'digital storage': {
        'standard': 'byte',
        'units': {unit: (lambda x, f=factor: x * f, lambda x, f=factor: x / f) 
                  for unit, factor in digital_storage_factors.items()}
    },
    'fuel consumption': {
        'standard': 'liter/100km',
        'units': fuel_consumption_units
    },
}

# Build unit-to-category mapping
unit_to_category = {}
for cat, data in categories.items():
    for unit in data['units']:
        unit_to_category[unit] = cat

# Conversion function
def convert(value, source_unit, target_unit):
    """
    Convert a value from source_unit to target_unit.
    
    Args:
        value (float): The value to convert.
        source_unit (str): The unit to convert from.
        target_unit (str): The unit to convert to.
        
    Returns:
        float: The converted value.
        
    Raises:
        ValueError: If units are not recognized or not in the same category.
    """
    source_unit = source_unit.lower()
    target_unit = target_unit.lower()
    if source_unit not in unit_to_category or target_unit not in unit_to_category:
        raise ValueError("Unit not recognized")
    source_cat = unit_to_category[source_unit]
    target_cat = unit_to_category[target_unit]
    if source_cat != target_cat:
        raise ValueError("Units are not in the same category")
    category = categories[source_cat]
    to_standard = category['units'][source_unit][0]
    from_standard = category['units'][target_unit][1]
    value_in_standard = to_standard(value)
    value_in_target = from_standard(value_in_standard)
    return value_in_target

# Main menu loop
def main():
    while True:
        print("\nSelect a category of conversion:")
        category_list = list(categories.keys())
        # Display categories with capitalized names
        for i, cat in enumerate(category_list, 1):
            print(f"{i}. {cat.capitalize()}")
        exit_option = len(category_list) + 1
        print(f"{exit_option}. Exit")
        
        try:
            category_num = int(input("Enter the number of the category: "))
            if category_num == exit_option:
                print("Exiting the program.")
                break
            elif 1 <= category_num <= len(category_list):
                selected_category = category_list[category_num - 1]
            else:
                print(f"Please enter a number between 1 and {exit_option}.")
                continue
        except ValueError:
            print("Please enter a valid integer.")
            continue

        units_list = list(categories[selected_category]['units'].keys())
        
        # Select 'from' unit
        print(f"\nSelect the 'from' unit for {selected_category.capitalize()}:")
        for i, unit in enumerate(units_list, 1):
            print(f"{i}. {unit}")
        while True:
            try:
                from_unit_num = int(input("Enter the number of the 'from' unit: "))
                if 1 <= from_unit_num <= len(units_list):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(units_list)}.")
            except ValueError:
                print("Please enter a valid integer.")
        from_unit = units_list[from_unit_num - 1]
        
        # Select 'to' unit
        print(f"\nSelect the 'to' unit for {selected_category.capitalize()}:")
        for i, unit in enumerate(units_list, 1):
            print(f"{i}. {unit}")
        while True:
            try:
                to_unit_num = int(input("Enter the number of the 'to' unit: "))
                if 1 <= to_unit_num <= len(units_list):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(units_list)}.")
            except ValueError:
                print("Please enter a valid integer.")
        to_unit = units_list[to_unit_num - 1]
        
        # Get the value to convert
        while True:
            try:
                value = float(input(f"\nEnter the value in {from_unit}: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Perform conversion and display result
        try:
            result = convert(value, from_unit, to_unit)
            print(f"\n{value} {from_unit} = {result} {to_unit}\n")
        except ValueError as e:
            print(f"Conversion error: {e}")
        
        # Prompt user to press 0 to return to main menu
        while True:
            user_input = input("Press 0 to return to the main menu: ")
            if user_input.strip() == "0":
                break

if __name__ == "__main__":
    main()
