#!/usr/bin/env python3

import os
import subprocess
import re
import datetime
import pygsheets
import speedtest

# Set constants
DATE = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

def get_credentials():
    """Function to check for valid OAuth access tokens."""
    gc = pygsheets.authorize(outh_file="credentials.json")
    return gc

def submit_into_spreadsheet(download, upload, ping):
    """Function to submit speedtest result."""
    gc = get_credentials()

    speedtest = gc.open(os.getenv('SPREADSHEET', 'Speedtest'))
    sheet = speedtest.sheet1

    data = [DATE, download, upload, ping]

    sheet.append_table(values=data)

def bits_2_human_readable(number_of_bits):
	if number_of_bits < 0:
		raise ValueError("!!! numberOfBits can't be smaller than 0 !!!")
	
	step_to_greater_unit = 1000.

	number_of_bits = float(number_of_bits)
	unit = 'bits'

	if (number_of_bits / step_to_greater_unit) >= 1:
		number_of_bits /= step_to_greater_unit
		unit = 'Kb'

	if (number_of_bits / step_to_greater_unit) >= 1:
		number_of_bits /= step_to_greater_unit
		unit = 'Mb'

	if (number_of_bits / step_to_greater_unit) >= 1:
		number_of_bits /= step_to_greater_unit
		unit = 'Gb'

	if (number_of_bits / step_to_greater_unit) >= 1:
		number_of_bits /= step_to_greater_unit
		unit = 'Tb'

	precision = 1
	number_of_bits = round(number_of_bits, precision)

	return float(number_of_bits)


def main():
    # Check for proper credentials
    print("Checking OAuth validity...")
    credentials = get_credentials()

    # Run speedtest and store output
    print("Starting speed test...")
    #Use servers variable to specify the server to use with speedtest, servers listed in https://www.speedtestserver.com/ example servers=["ID_server"]
    servers = []
    spdtest = speedtest.Speedtest()
    spdtest.get_servers(servers)
    spdtest.get_best_server()
    download = bits_2_human_readable(spdtest.download())
    upload = bits_2_human_readable(spdtest.upload())
    ping = spdtest.results.ping
    print("Starting speed finished!")

    # Write to spreadsheet
    print("Writing to spreadsheet...")
    submit_into_spreadsheet(download, upload, ping)
    print("Successfuly written to spreadsheet!")

if __name__ == "__main__":
    main()
