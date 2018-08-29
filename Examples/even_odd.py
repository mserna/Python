##
##
##
##
##


def main():

	#Ask user fo number
	number = int(input("Please enter a number: "))
	if(isOdd(number)):
		print("Even")
	else:
		print("Odd")

def isOdd(number):
	if(number % 2):
		return False
	else:
		return True


main()
