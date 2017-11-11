import requests, bs4, json, sys

#Create the group dictionary
#CAA=33 -> Excample

groups = {}
group_data = open("teams.dat").read().split("\n")
for line in group_data:
	pieces = line.split("=")
	groups[pieces[0]] = pieces[1]

user_agent = "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

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
		data = grab_data(sys.argv[1],groups[key])
		file = open("Data/" + key + ".csv", "+w")
		file.write("Location,Name,Score\n")
		for point in data:
			team_a = point["team_a"]
			team_b = point["team_b"]
			file.write(team_a[1] + "," + team_a[0] + "," + team_a[2] + "\n")
			file.write(team_b[1] + "," + team_b[0] + "," + team_b[2] + "\n")

__main__()
