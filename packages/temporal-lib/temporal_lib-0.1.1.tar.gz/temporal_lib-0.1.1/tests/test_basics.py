""" test_basics.py """

from datetime import date, timedelta  # Standard Library

# Temporal
from temporal_lib.core import calc_future_dates
from temporal_lib.tlib_date import TDate, date_to_metadata_dict


def test_weekday_name():
	calendar_date = date(2021, 4, 17)  # April 17th is a Saturday

	# Test using TDate
	assert TDate(calendar_date).day_of_week_longname() == "Saturday"

	# Test using Metadata Dictionary (which is derived from TDate, so should be identical results)
	weekday_name = date_to_metadata_dict(calendar_date)['weekday_name']
	assert weekday_name == "Saturday"


def test_weekday_position():
	"""
	Test using Metadata Dictionary via TDate.
	"""
	calendar_date = date(2021, 4, 17)  # April 17th is a Saturday, so should be day number 7.
	retval = date_to_metadata_dict(calendar_date)['index_in_week']
	assert retval == 7


def test_future_dates_calculator():
	# Test a 7 day iteration.
	retval = calc_future_dates(epoch_date=date(2021, 7, 1),
			  			       multiple_of_days=7,
							   earliest_result_date= date(2021, 7, 16),
							   qty_of_result_dates=4)

	assert retval == [ date(2021, 7, 22),
						date(2021, 7, 29),
						date(2021, 8, 5),
						date(2021, 8, 12) ]

	# Test a 14 day iteration.
	retval = calc_future_dates(epoch_date=date(2021, 7, 1),
							   multiple_of_days=14,
							   earliest_result_date= date(2021, 7, 16),
							   qty_of_result_dates=4)

	assert retval == [ date(2021, 7, 29),
						date(2021, 8, 12),
						date(2021, 8, 26),
						date(2021, 9, 9) ]


def custom_test_one(year):
	""" Simple test for printing Dates and Weeks to console.
		bench execute --args "{2021}" temporal.test_temporal.custom_test_one
	"""
	if isinstance(year, str):
		year = int(year)
	start_date = date(year=year, month=1, day=1)
	end_date = date(year=year, month=12, day=31)

	list_of_dates = temporal.core.date_range(start_date, end_date)
	for each_date in list_of_dates:
		week_tuple = temporal.tlib_week.date_to_week_tuple(each_date)  # pylint: disable=protected-access
		print(f"Day {each_date}, Week Year {week_tuple[0]}, Week Number {week_tuple[1]}")


def test_addition():
	"""
	Test adding a timedelta to a TDate.
	"""
	calendar_tdate = TDate(date(2021, 4, 17))  # April 17th 2021 is a Saturday
	offset = timedelta(days=10)
	expected_result = TDate("2021-04-27")
	assert calendar_tdate + offset == expected_result
