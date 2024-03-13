import pytest
from project import pair_date, pair_input, average, get_symbols, get_historic, print_

def main():
    test_get_historic()
    test_print_()
    test_average()

def test_get_historic():
    assert get_historic('1/1/2020', 'BTCUSDT') == '7195.24000000'
    with pytest.raises(UnboundLocalError):
        get_historic('cat', 'dog')

def test_average():
    assert average(100, 110) == 10

def test_print_():
    assert print_(1, '1/1/2020', 'BTCUSDT') == 'The open price for the pair BTCUSDT on 1/1/2020 was $1.00'
    assert print_(0.005739, '1/1/2020', 'LTCBTC') == 'The open price for the pair LTCBTC on 1/1/2020 was 0.005739 BTC'

if __name__ == "__main__":
    main()