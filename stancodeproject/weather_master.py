"""
File: weather_master.py
Name: Andy Huang
-----------------------
This program should implement a console program
that asks weather data from user to compute the
average, highest, lowest, cold days among the inputs.
Output format should match what is shown in the sample
run in the Assignment 2 Handout.

"""
EXIT = -100


def main():
	"""
	After ask the user to input the data, we assign several variables we need to calculate the average and cold days.
	Everytime the user input a data, the count will plus one, helping us to get the average in the end.
	Everytime the new data is higher/lower than the current highest/lowest temperature, our record would change.
	Everytime the new data is lower than 16, the cold_days will plus one.
	In the end, after the user input -100, the function will end and print the 4 information we need.
	"""
	print('stanCode "Weather Master 4.0"!')
	data = int(input('Next Temperature: (or -100 to quit)? '))
	if data == EXIT:
		print('No temperatures were entered.')
	else:
		count = 1
		highest = data
		lowest = data
		total = data
		cold_days = 0
		if data < 16:
			cold_days += 1
		while True:
			data = int(input('Next Temperature: (or -100 to quit)? '))
			while data != EXIT:
				if data >= highest:
					highest = data
				if data <= lowest:
					lowest = data
				if data < 16:
					cold_days += 1
				count += 1
				old_total = total
				total = old_total + data
				data = int(input('Next Temperature: (or -100 to quit)? '))
			break
		average = total / count
		print('Highest Temperature = ' + str(highest))
		print('Lowest Temperature = ' + str(lowest))
		print('Average = ' + str(average))
		print(str(cold_days) + ' cold day(s)')


# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == "__main__":
	main()
