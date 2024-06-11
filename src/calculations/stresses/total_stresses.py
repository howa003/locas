from src.models import Results


def sum_all_stresses(
        results: Results) -> str:
    '''
    This function sums the thermal, internal-pressure, and prestressing stresses.

    :param results: A handle to the :class:`models.Results` object containing the results.
    :type results: class:`Results`
    :return: String indicating the successful/unsuccessful calculation of the circumferential stress.
    :rtype: str
    '''

    try:
        # print('===== All stresses started. =====')
        # print('Adding thermal stresses to overall stresses.')
        results.stress_total_fixed = results.stress_temp_fixed
        results.stress_total_clamped = results.stress_temp_clamped
        results.stress_total_free = results.stress_temp_free
        # print('Adding internal-pressure stresses to overall stresses.')
        results.stress_total_fixed = results.stress_total_fixed + results.stress_internal_pressure
        results.stress_total_clamped = results.stress_total_clamped + results.stress_internal_pressure
        results.stress_total_free = results.stress_total_free + results.stress_internal_pressure
        # matrixStrnR = matrixStrnR + matrixStrnOvrprss
        # matrixStrnD = matrixStrnD + matrixStrnOvrprss
        # print('Adding prestressing stresses to overall stresses.')
        results.stress_total_fixed = results.stress_total_fixed + results.stress_prestressing
        results.stress_total_clamped = results.stress_total_clamped + results.stress_prestressing
        results.stress_total_free = results.stress_total_free + results.stress_prestressing
        # matrixStrnR = matrixStrnR + matrixStrnPrstrss
        # matrixStrnD = matrixStrnD + matrixStrnPrstrss
        # print('===== All stresses ended. =====')

        result_message = "Total stresses obtained successfully."

    except Exception as exception:
        result_message = "Summing of total stresses FAILED: " + str(exception)

    return result_message
