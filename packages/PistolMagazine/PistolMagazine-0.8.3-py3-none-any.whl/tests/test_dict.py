from random import choice
from pistol_magazine import List, Datetime, Float, Timestamp, Dict, StrInt, provider
from pistol_magazine.self_made import ProviderField


@provider
class MyProvider:
    def symbol(self):
        return choice(["BTC", "ETH"])


def test_dict():
    expect_format = {
        "a": Float(left=2, right=4, unsigned=True),
        "b": Timestamp(Timestamp.D_TIMEE10, days=2),
        "C": List(
            [
                Datetime(Datetime.D_FORMAT_YMD_T, weeks=2),
                StrInt(byte_nums=6, unsigned=True)
            ]
        ),
        "d": ProviderField(MyProvider().symbol)
    }
    # # e.g. {"a": -95.7105, "b": 1717570325, "C": ["2024-06-15T03:14:05", "39"]} <JSON>
    print(Dict(expect_format).mock(to_json=True))
