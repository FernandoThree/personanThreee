def isYearLeap(year):
    if year % 400 == 0 or (year % 100 != 0 and year %4 == 0):
        return True
    else:
        None

testData = [1900, 2000, 2016, 1987]
testResults = [False, True, True, False]
for i in range(len(testData)):
    yr = testData[i]
    print(yr,"->",end="")
    result = isYearLeap(yr)
    if result == testResults[i]:
        print("OK")
    else:
        print("Error")


def daysInMonth(year, month):
    if year != None:
        isYearLeap(year)

    if year != None and month != None:
        if year == 1900 and month == 2:
            days = 28
        elif year == 2000 and month == 2:
            days = 29
        elif month == 1: 
            days = 31
        elif month == 11:
            days = 30
        else:
            None
        return (days)
    else:
        return None

testYears = [1900, 2000, 2016, 1987]
testMonths = [2, 2, 1, 11]
testResults = [28, 29, 31, 30]
for i in range(len(testYears)):
    yr = testYears[i]
    mo = testMonths[i]
    print(yr, mo, "->", end="")
    result = daysInMonth(yr, mo)
    if result == testResults[i]:
        print("OK")
    else:
        print("Error")
    
'''
testData = [1900, 2000, 2016, 1987]
testResults = [False, True, True, False]
for i in range(len(testData)):
	yr = testData[i]
	print(yr,"->",end="")
	result = isYearLeap(yr)
	if result == testResults[i]:
		print("OK")
	else:
		print("Error")

def daysInMonth(year, month):
    if year != None:
        isYearLeap(year)
    
    if year != None and month != None:
        print(calendar.monthrange(year,month))
        return calendar.monthrange(year,month)
    else:
        return None

testYears = [1900, 2000, 2016, 1987]
testMonths = [2, 2, 1, 11]
testResults = [28, 29, 31, 30]
for i in range(len(testYears)):
	yr = testYears[i]
	mo = testMonths[i]
	print("numero mes: ", mo)
	print(yr, mo, "->", end="")
	result = daysInMonth(yr, mo)
	if result == testResults[i]:
		print("OK")
	else:
		print("Error")
'''
