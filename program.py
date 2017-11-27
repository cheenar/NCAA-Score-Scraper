import requests, bs4, json, sys, os

#Create the group dictionary
#CAA=33 -> Excample

groups = {}
group_data = open("teams.dat").read().split("\n")
for line in group_data:
	pieces = line.split("=")
	groups[pieces[0]] = pieces[1]

user_agent = "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

from datetime import datetime
# Some Helper Functions for the Scraper
def date():
	d = str(datetime.now()).split(" ")
	return d[0], d[1]

def get_date(date):
	return date[0]

def get_time(date):
	return date[1]

def get_current_date():
	return get_date(date()).replace("-", "")

def create_folder(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def create_url(date, group_num):
	base_url = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?lang=en&region=us&calendartype=blacklist&limit=300&dates=" + str(date) + "&tz=America%2FNew_York&groups=" + str(group_num)
	return base_url

def grab_data(date, group_num):
	x = requests.get(create_url(date, group_num), headers={"User-Agent":user_agent})
	json_data = json.loads(x.text)
	events = json_data["events"]
	matchup = []

	for event in events:
		team_a = event["competitions"][0]["competitors"][0]["team"]["name"], event["competitions"][0]["competitors"][0]["team"]["location"], event["competitions"][0]["competitors"][0]["score"]
		team_b = event["competitions"][0]["competitors"][1]["team"]["name"], event["competitions"][0]["competitors"][1]["team"]["location"], event["competitions"][0]["competitors"][1]["score"]
		print(team_a, "\n", team_b, "\n")
		matchup.append({"team_a": team_a, "team_b": team_b})

	return matchup

def __main__():
	for key in groups.keys():
		_date = ""
		if len(sys.argv) > 1:
			_date = sys.argv[1]
		else:
			_date = get_current_date()
		data = grab_data(_date,groups[key])
		create_folder("Data")
		create_folder("Data/" + _date)
		file = open("Data/" + _date + "/" + key + ".csv", "+w")
		file.write("Location,Name,Score\n")
		for point in data:
			team_a = point["team_a"]
			team_b = point["team_b"]
			file.write(team_a[1] + "," + team_a[0] + "," + team_a[2] + "\n")
			file.write(team_b[1] + "," + team_b[0] + "," + team_b[2] + "\n")
			file.write("-,-,-\n")

__main__()
