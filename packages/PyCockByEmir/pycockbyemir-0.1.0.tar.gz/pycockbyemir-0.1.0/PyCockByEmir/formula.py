def calculate_ratio(height: float, foot_length: float) -> float:
    """
    Boy uzunluğu ve ayak uzunluğuna göre özel bir hesaplama yapar.

    :param height: Boy uzunluğu (cm)
    :param foot_length: Ayak uzunluğu (cm)
    :return: Hesaplanan değer (float)
    """
    if height <= 0 or foot_length <= 0:
        raise ValueError("Boy ve ayak uzunluğu pozitif olmalıdır.")

    result = ((height / foot_length) + (foot_length / 2)) * 0.55
    return round(result, 4)
