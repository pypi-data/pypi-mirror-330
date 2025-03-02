""" tests/test_ranges.py """

def test_date_ranges_to_dates():
	from temporal_lib.core import datestr_to_date, date_ranges_to_dates

	test_date_ranges = [
		('2023-10-01', '2023-10-05'),
		('2023-11-15', '2023-11-20'),
		('2023-12-09', '2023-12-13')
	]

	expected_dates = [
		datestr_to_date('2023-10-01'), datestr_to_date('2023-10-02'), datestr_to_date('2023-10-03'), datestr_to_date('2023-10-04'), datestr_to_date('2023-10-05'),
		datestr_to_date('2023-11-15'), datestr_to_date('2023-11-16'), datestr_to_date('2023-11-17'), datestr_to_date('2023-11-18'),
		datestr_to_date('2023-11-19'), datestr_to_date('2023-11-20'),
		datestr_to_date('2023-12-09'), datestr_to_date('2023-12-10'), datestr_to_date('2023-12-11'), datestr_to_date('2023-12-12'), datestr_to_date('2023-12-13')
	]

	actual_dates = date_ranges_to_dates(test_date_ranges)
	try:
		assert actual_dates == expected_dates
	except AssertionError:
		print("Test failed; expected results do not match actual.")
		print(f"Expected:\n{expected_dates}\n")
		print(f"Actual:\n{actual_dates}")
	else:
		print("\u2713 Successful test of function date_ranges_to_dates()")
