import pytest
from PyCockByEmir import calculate_ratio

def test_calculate_ratio():
    assert calculate_ratio(180, 25) == 10.83  # Örnek sonuç
    assert calculate_ratio(160, 23) == 10.15  # Örnek sonuç

    with pytest.raises(ValueError):
        calculate_ratio(-170, 25)  # Hata fırlatmalı
