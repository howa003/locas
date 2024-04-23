from src.config import CONCRETE_CONDUCTIVITY_LIMIT


def steel_conductivity(temperature: float) -> float:
    # Temperature is in Celsius
    if temperature <= 800:
        return 54 - 3.33 * temperature / 100
    else:
        return 27.3


def concrete_conductivity(temperature: float) -> float:
    # Temperature is in Celsius
    if CONCRETE_CONDUCTIVITY_LIMIT == 0:
        return 1.36 - 0.136 * temperature / 100 + 0.0057 * (temperature / 100) ** 2
    else:
        return 2 - 0.2451 * temperature / 100 + 0.0107 * (temperature / 100) ** 2


