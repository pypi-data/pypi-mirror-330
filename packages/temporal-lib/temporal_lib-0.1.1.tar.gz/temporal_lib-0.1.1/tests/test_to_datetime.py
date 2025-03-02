#!/bin/python

from datetime import datetime
from temporal_lib.tlib_types import any_to_datetime, offset_string_to_tzinfo

def test_string_to_datetime():

	datetime_string = "2022-03-10 20:46:37"
	expected_datetime = datetime(2022, 3, 10, 20, 46, 37)
	assert any_to_datetime(datetime_string) == expected_datetime

	datetime_string = "2022-03-10 20:46:37-08:00"
	tz_offset_string = datetime_string[-6:]
	new_tzinfo = offset_string_to_tzinfo(tz_offset_string)
	expected_datetime = datetime(2022, 3, 10, 20, 46, 37, tzinfo=new_tzinfo)
	assert any_to_datetime(datetime_string) == expected_datetime

	datetime_string = "2022-03-10 20:46:37.554284+05:30"
	tz_offset_string = datetime_string[-6:]  #  +05:30
	new_tzinfo = offset_string_to_tzinfo(tz_offset_string)
	expected_datetime = datetime(2022, 3, 10, 20, 46, 37, microsecond=554284, tzinfo=new_tzinfo)
	assert any_to_datetime(datetime_string) == expected_datetime
