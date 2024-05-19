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


def steel_volumetric_heat_capacity(temperature: float) -> float:
    # Temperature is in Celsius
    initial_density = 7850
    if temperature <= 600:
        return initial_density * (425 + 7.73 * temperature / 10 - 1.69 * (temperature ** 2) / 1000 + 2.22 * (temperature ** 3) / 1000000)
    elif temperature <= 735:
        return initial_density * (666 - (13002 / (temperature - 738)))
    elif temperature <= 900:
        return initial_density * (545 + 17820 / (temperature - 731))
    else:
        return initial_density * 650


def concrete_density(temperature: float, initial_density: float) -> float:
    # Temperature is in Celsius
    if temperature < 115:
        return initial_density
    elif temperature < 200:
        return initial_density * (1 - (0.02 * (temperature - 115) / 85))
    elif temperature < 400:
        return initial_density * (0.98 - (0.03 * (temperature - 200) / 200))
    else:
        return initial_density * (0.95 - (0.07 * (temperature - 400) / 800))


def concrete_specific_heat_capacity(temperature: float, water_content: float) -> float:
    # Temperature is in Celsius
    peak_capacity = 900 + (water_content / 3) * (2020 - 900)
    if temperature < 100:
        return 900
    elif temperature < 115:
        return peak_capacity
    elif temperature < 200:
        return peak_capacity - ((temperature - 115) / 85) * (peak_capacity - 1000)
    elif temperature < 400:
        return 1000 + (temperature - 200) / 2
    else:
        return 1100


def concrete_volumetric_heat_capacity(temperature: float, initial_density: float, water_content: float) -> float:
    # Temperature is in Celsius
    return concrete_density(temperature, initial_density) * concrete_specific_heat_capacity(temperature, water_content)




    # def volHeatCap(T):
    #     return (density(T)*heatCapac(T))
    #

    #
    # def volHeatCapSteel(T):
    #     rhoSt = 7850
    #     if T <= 600:
    #         return rhoSt*(425 + 7.73*T/10 - 1.69*T*T/1000 + 2.22*T*T*T/1000000)
    #     elif T <= 735:
    #         return rhoSt*(666 - (13002/(T-738)))
    #     elif T <= 900:
    #         return rhoSt*(545 + 17820/(T-731))
    #     else:
    #         return rhoSt*650