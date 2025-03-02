""" test_weeks.py """

from datetime import date
import json
import pathlib

# import temporal_lib as temporal
from temporal_lib import tlib_week, tlib_year
from temporal_lib.tlib_types import (
	any_to_date,
	datestr_to_date,
)

def test_number_iso_weeks_in_year():
	expected_results = [
		(2000, 52),
		(2001, 52),
		(2002, 52),
		(2003, 52),
		(2004, 53),
		(2005, 52),
		(2006, 52),
		(2007, 52),
		(2008,	52),
		(2009,	53),
		(2010,	52),
		(2011,	52),
		(2012,	52),
		(2013,	52),
		(2014,	52),
		(2015,	53),
		(2016,	52),
		(2017,	52),
		(2018,	52),
		(2019,	52),
		(2020,	53),
		(2021,	52),
		(2022,	52),
		(2023,	52),
		(2024,	52)
	]

	# Per ISO specification, January 4th is always going to be Week 1 of a given year.
	# And the 28th of December will always be the last week.
	for each_tuple in expected_results:
		december_28 = date(each_tuple[0], 12, 28)
		assert december_28.isocalendar()[1] == each_tuple[1]

	for each_tuple in expected_results:
		# Calculate the number of Weeks in a Year, and compare to expected.
		assert tlib_year.Year( each_tuple[0]).number_of_iso_weeks() == each_tuple[1]

# --------
# All tests below this point use a modified Western Calendar (the week containing January 1st = Week 1)
# --------

def test_date_to_week_tuple():
	"""
	These tests validate that given a Calendar Date, the library calculates the correct Year and Week Number.
	"""
	any_date = datestr_to_date("2020-12-25")
	week_tuple = tlib_week.date_to_week_tuple(any_date, verbose=True)
	assert week_tuple == (2020, 52)

	any_date = datestr_to_date("2020-12-29")
	week_tuple = tlib_week.date_to_week_tuple(any_date, verbose=True)
	assert week_tuple == (2021, 1)


def test_date_to_weeknums():
	"""
	Loop through a variety of calendar dates, and validate the week number is correct.
	"""
	test_directory = pathlib.Path(__file__).parent.absolute()
	with open(test_directory / "week_numbering_WT_2.json", "r", encoding="utf-8") as json_file:
		file_data = json.load(json_file)

	for each_row in file_data["calendar_dates"]:
		calendar_date = any_to_date(each_row["calendar_date"])
		calculated_week_number = tlib_week.date_to_week_tuple(calendar_date)[1]  # pylint: disable=protected-access
		try:
			assert calculated_week_number == int(each_row["week_number"])
		except AssertionError as ex:
			print(f"Date: {calendar_date}, Expected: {each_row['week_number']}, Calculated: {calculated_week_number}")
			calculated_week_number = tlib_week.date_to_week_tuple(calendar_date, verbose=True)[1]  # pylint: disable=protected-access
			raise ex


def test_last_date_in_week():
	"""
	Given a unique week, calculate the last calendar date in the Week (always a Saturday)
	"""
	# NOTE: Standard Python library begins each week on a Monday.  So code below uses an index of 5 for Saturdays.
	week_tuple = (2005, 53)
	expected_saturday = datestr_to_date("2005-12-31")
	assert expected_saturday.weekday() == 5  # standard Python library starts week on a Monday.
	assert expected_saturday == tlib_week._week_tuple_to_last_date_in_week(week_tuple)  # pylint: disable=protected-access

	week_tuple = (2006, 1)
	expected_saturday = datestr_to_date("2006-01-07")
	assert expected_saturday.weekday() == 5  # standard Python library starts week on a Monday.
	assert expected_saturday == tlib_week._week_tuple_to_last_date_in_week(week_tuple)  # pylint: disable=protected-access

	week_tuple = (2020, 5)
	expected_saturday = datestr_to_date("2020-02-01")
	assert expected_saturday.weekday() == 5  # standard Python library starts week on a Monday.
	assert expected_saturday == tlib_week._week_tuple_to_last_date_in_week(week_tuple)  # pylint: disable=protected-access

	week_tuple = (2020, 52)
	expected_saturday = datestr_to_date("2020-12-26")
	assert expected_saturday.weekday() == 5  # standard Python library starts week on a Monday.
	assert expected_saturday == tlib_week._week_tuple_to_last_date_in_week(week_tuple)  # pylint: disable=protected-access

	week_tuple = (2021, 1)
	expected_saturday = datestr_to_date("2021-01-02")
	assert expected_saturday.weekday() == 5  # standard Python library starts week on a Monday.
	assert expected_saturday == tlib_week._week_tuple_to_last_date_in_week(week_tuple)  # pylint: disable=protected-access


def test_get_weeks_as_dict():
	from temporal_lib.tlib_week import get_weeks_as_dict
	expected_length = 5
	result = get_weeks_as_dict(from_year=2023, from_week_num=1, to_year=2023, to_week_num=5)
	assert len(result) == expected_length
