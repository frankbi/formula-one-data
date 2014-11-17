from bs4 import BeautifulSoup
import requests
import os


def get_race_num(idx):

	# add a leading zero if char is only 1 digit
	if idx > 0:
		if len(str(idx)) is 1:
			return "0" + str(idx) + "_"
		else:
			return str(idx) + "_"


def get_race_results(paths, year):

	# loop through each race called by a given year
	for idx1, each_race in enumerate(paths):

		race_url = each_race[0]

		# race number, country of race and year fpr file name
		file_name = get_race_num(idx1 + 1) + each_race[1].replace(" ", "").lower() + "_" + year

		r = requests.get(race_url)

		soup = BeautifulSoup(r.text)

		race_tables = soup.findAll("table", attrs={"class":"raceResults"})

		# won't be a table if there hasn't been a race
		if len(race_tables) > 0:

			directory_name = "season_races"

			subdirectory_name = directory_name + "/" + year

			# check to see if results folder already exists or not
			# if not, creates the folder to store race results
			if not os.path.exists(directory_name):
				os.makedirs(directory_name)

			# does the same for subdirectories
			if not os.path.exists(subdirectory_name):
				os.makedirs(subdirectory_name)

			f = open(subdirectory_name + "/" + file_name + ".csv", "w")

			race_table_rows = race_tables[0].findAll("tr")

			for idx2, each_row in enumerate(race_table_rows):

				# get header and write that first
				if idx2 is 0:
					th_cells = each_row.findAll("th")
					cells = [cell.get_text() for cell in th_cells]
					f.write(",".join(cells) + "\n")

				# then loop over and write rest of cells
				else:
					td_cells = each_row.findAll("td")
					cells = [cell.get_text() for cell in td_cells]
					f.write(",".join(cells).encode("utf-8") + "\n")

		f.close()


def get_yearly_results(year):

	year = str(year)

	r = requests.get(base_path + year + "/")

	# stores race results urls and country of race
	season_results_paths = []

	soup = BeautifulSoup(r.text)

	# get the table with specified class
	tables = soup.findAll("table", attrs={"class":"raceResults"})

	# there should be only one table
	if len(tables) < 2:

		directory_name = "season_results"

		if not os.path.exists(directory_name):
			os.makedirs(directory_name)

		# create and open new document for data
		f = open(directory_name + "/" + year + ".csv", "w")

		# break the table down to rows
		table_rows = tables[0].findAll("tr")

		# loop over each row
		for idx, each_row in enumerate(table_rows):

			# get header and write that first
			if idx is 0:
				th_cells = each_row.findAll("th")
				cells = [cell.get_text() for cell in th_cells]
				f.write(",".join(cells) + "\n")

			# then loop over and write rest of cells
			else:
				td_cells = each_row.findAll("td")

				cells = [cell.get_text() for cell in td_cells]
				f.write(",".join(cells).encode("utf-8") + "\n")

				# get links to each race's result
				result_paths = td_cells[0].find("a")
				full_result_path = results_base_path + str(result_paths["href"])

				# push everything to global list for accessing later on
				season_results_paths.append([full_result_path, result_paths.get_text()])
			
		f.close()

	# move onto the next step ...
	get_race_results(season_results_paths, year)


if __name__ == "__main__":

	base_path = "http://www.formula1.com/results/season/"
	
	results_base_path = base_path.replace("/results/season", "")

	for year in range(1950, 2015):
		get_yearly_results(year)







