from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime
import sys
import getpass

def get_totals_for_days(date1, date2, browser):
	timedelta = date2 - date1
	if (timedelta.days > 31):
		print("probably wont work lmao")
		browser.quit()
		return ""
	timeUnitElement = browser.find_element_by_id("timeUnitCode")
	timeUnitElement.click();
	select = Select(timeUnitElement)
	select.select_by_index(0)
	periodBegin = browser.find_element_by_id("periodDailyBegin")
	periodBegin.clear()
	periodBegin.send_keys(str(date1))
	periodEnd = browser.find_element_by_id("periodDailyEnd")
	periodEnd.clear()
	periodEnd.send_keys(str(date2))
	searchFieldDTNO1 = browser.find_elements_by_class_name("searchFieldDTNO1")[1]
	fuckeryDiv = searchFieldDTNO1.find_element_by_class_name("btn-result")
	fuckeryDiv.find_element_by_class_name("btnGray").click()
	statsTable = browser.find_element_by_id("statisticsTable")
	rows = browser.find_elements_by_tag_name("tr")
	lastRow = rows[len(rows) - 1]
	cells = lastRow.find_elements_by_tag_name("td")
	cells = cells[1:-1]
	totals = ""
	oneDayDelta = datetime.timedelta(days=1)
	for cell in cells:
		totals = totals + cell.text + "\n"
		date1 = date1 + oneDayDelta
	return totals


browser = webdriver.Chrome()
browser.set_window_size(1120, 550)
url = 'http://seller.samsungapps.com/login/signIn.as?returnURL=%2fmain%2fsellerMain.as&ssoCheck=fail'
browser.get(url)
username = input("Username: ")
password = getpass.getpass("Password: ")
browser.find_element_by_id("emailID").send_keys(username)
browser.find_element_by_id("password").send_keys(password)
browser.find_element_by_class_name("btnNew01").click()
browser.get("http://seller.samsungapps.com/statistics/statisticsDownloadsSales.as")
totals = ""
startDateString = input("Start Date (mm/dd/yyyy): ")
startDate = datetime.datetime.strptime(startDateString, "%m/%d/%Y").date()
print(str(startDate))

endDateString = input("End Date (mm/dd/yyyy or today): ")
if endDateString == "today":
	endDate = datetime.date.today()
else:
	endDate = datetime.datetime.strptime(endDateString, "%m/%d/%Y").date()
print(str(endDate))
while startDate < endDate:
	timeDelta = datetime.timedelta(days=30)
	if ((endDate - startDate).days < 30):
		timeDelta = endDate - startDate - datetime.timedelta(days=1)
	totals = totals + get_totals_for_days(startDate, startDate + timeDelta, browser)
	startDate = startDate + timeDelta + datetime.timedelta(days=1)
print(totals)
browser.quit()