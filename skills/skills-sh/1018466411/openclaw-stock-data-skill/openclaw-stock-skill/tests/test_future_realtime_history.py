import unittest
from unittest.mock import patch

import stock_api


class FutureRealtimeHistoryTest(unittest.TestCase):
    @patch("stock_api._make_request")
    def test_defaults(self, make_request):
        make_request.return_value = {"date": "2026-09-15", "total": 0, "list": []}

        result = stock_api.get_future_realtime_history()

        self.assertEqual(result["total"], 0)
        make_request.assert_called_once_with(
            "POST",
            "/future/realtime/history",
            json_data={"page": 0, "page_size": 2000},
        )

    @patch("stock_api._make_request")
    def test_forwards_filters_and_pagination(self, make_request):
        make_request.return_value = {"date": "2026-09-15", "total": 1, "list": [{}]}

        stock_api.get_future_realtime_history(
            contract_code=["CU2605.SHF"],
            contract_type="contract",
            trade_time="2026-09-15 09:31:00",
            date="2026-09-15",
            page=2,
            page_size=100,
        )

        make_request.assert_called_once_with(
            "POST",
            "/future/realtime/history",
            json_data={
                "page": 2,
                "page_size": 100,
                "contract_code": ["CU2605.SHF"],
                "contract_type": "contract",
                "trade_time": "2026-09-15 09:31:00",
                "date": "2026-09-15",
            },
        )


if __name__ == "__main__":
    unittest.main()
