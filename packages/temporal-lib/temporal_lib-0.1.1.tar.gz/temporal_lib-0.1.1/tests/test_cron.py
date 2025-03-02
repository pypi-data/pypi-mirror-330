""" tests/test_cron.py """

# CLI: pytest src/tests/test_cron.py

from temporal_lib import cron

# pylint: disable=pointless-string-statement
"""
Test Case #1:
$ npx local-crontab  '0 10 * * *' --tz America/New_York
0 15 * 1-2,12 *
0 15 1-10 3 *
0 14 11-31 3 *
0 14 * 4-10 *
0 14 1-3 11 *
0 15 4-31 11 *

Test Case #2:
$ npx local-crontab  '0 10 * * *' --tz America/Denver
0 17 * 1-2,12 *
0 17 1-10 3 *
0 16 11-31 3 *
0 16 * 4-10 *
0 16 1-3 11 *
0 17 4-31 11 *
"""


def test_validate_cron_string():
	"""
	Minutes		Hours	Day of month	Month	Day of week
	"""
	cron_string = "30 23 * * * "  # 11:30 PM daily.
	assert cron.validate_cron_string(cron_string) is True

	cron_string = "10,20,30 23 * * * "  # 11:30 PM daily.
	assert cron.validate_cron_string(cron_string) is True

	cron_string = "10-15 23 * * * "  # 11:30 PM daily.
	assert cron.validate_cron_string(cron_string) is True

	cron_string = "30 23 11-31 * *"  # 11:30 PM on the 11th through 31st days of every month.
	assert cron.validate_cron_string(cron_string) is True

	cron_string = "30 23 11-31 3 *"  # 11:30 PM on the 11th through 31st days of March.
	assert cron.validate_cron_string(cron_string) is True

def test_eastern_cron_to_utc_cron():
	import local_crontab
	cron_string = "30 23 * * * "

	expected_values = ['30 4 2-31 1 *',  # 4:30 AM UTC January 2nd through 31st
	                   '30 4 * 2 *',     # 4:30 AM UTC throughout February 
					   '30 4 1-12 3 *',  # 4:30 AM UTC from March 1st UTC through March 12 UTC (March 11st Eastern)
					   '30 3 13-31 3 *', # 3:30 AM UTC from March 13th UTC through March 31st UTC
					   '30 3 * 4-10 *',  # 3:30 AM UTC throughout April and October.
					   '30 3 1-5 11 *',  # 3:30 AM UTC from November 1st through 5th UTC
					   '30 4 6-30 11 *', # 4:30 AM UTC from November 6th through 30th UTC
					   '30 4 * 12 *',    # 4:30 AM UTC throughout December UTC
					   '30 4 1 1 *']     # 4:30 AM UTC January 1st.

	actual_values: list = local_crontab.Converter(cron_string, 'US/Eastern', year=2023).to_utc_crons()  # List of Strings (not cron objects)
	assert actual_values == expected_values


def test_cron_to_utc_datetimes():
	result = cron.local_cron_to_utc_datetimes("30 23 * * *", 'US/Eastern')
	assert isinstance(result, list) is True
