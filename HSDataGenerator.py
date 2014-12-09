import os
import requests
import pandas as pd
from numpy import array
from numpy import zeros
from numpy import savetxt
from scipy.cluster.vq import vq, kmeans2, whiten
from sets import Set

site = "https://www.hackerschool.com"
access_token = "?access_token=" + os.environ.get('HS_API_TOKEN')
caller_email = "mdulieu@gmail.com"

# Get people from api and return a json object (list of dictionaries)
def get_people_in_all_batches():
	allBatches = requests.get(site + '/api/v1/batches' + access_token)
	allBatches = allBatches.json()
	batch_id = []
	for batch in allBatches:
		batch_id.append(batch['id'])
	allPeople = []
	for batch_nb in range(len(allBatches)):
		allPeople += requests.get(site + '/api/v1/batches/%d/people' % allBatches[batch_nb]['id'] + access_token).json()
	return allPeople

# Get people from api and returns json object containing all people from the last two batches
def get_people_in_two_last_batches():
	allBatches = requests.get(site + '/api/v1/batches' + access_token)
	twoLastBatches = allBatches.json()[0:2]
	currentPeople1 = requests.get(site + '/api/v1/batches/%d/people' % twoLastBatches[0]['id'] + access_token) 
	currentPeople2 = requests.get(site + '/api/v1/batches/%d/people' % twoLastBatches[1]['id'] + access_token)
	currentPeople = currentPeople1.json() + currentPeople2.json()
	return currentPeople

# Takes as an argument a json list of people and an email, and returns the api id corresponding to the email
def get_caller_id(people, caller_email):
	for person in people:
		if person['email'] == caller_email:
			caller_id = person['id']
			return caller_id

# Get a json object containing people from the api and returns a list of sorted skills without doubles
def get_all_skills(people):
	allSkillsSet = Set([])
	for person in people:
		for skill in person['skills']:
			allSkillsSet.add(skill.lower())
	allSkills = list(allSkillsSet)
	allSkills = sorted(allSkills)
	return allSkills

# Take a json object containing people and returns a list of ids + a dictionary with keys == ids referring to people
def create_people_dict(people):
	#first_name = []
	#last_name = []
	people_id = []
	people_dictionary = {}
	for person in people:
		#first_name.append(person['first_name'])
		#last_name.append(person['last_name'])
		people_id.append(person['id'])
		people_dictionary[person['id']] = person
		return people_id, people_dictionary

# Take a list of ids, a dictionary created by previous func, and a list of all skills
# Saves an csv array with people ids for each row, and skills for each column in HSData.csv
def create_people_skills_matrix(people_id, people_dictionary, allSkills):
	peopleSkills = zeros((len(people_id), len(allSkills)))
	for i, people in enumerate(people_id):
		for j, skill in enumerate(allSkills):
			peopleSkills[i,j]  = skill in people_dictionary[people]['skills']
	savetxt("HSData.csv", peopleSkills, delimiter=",", fmt = "%5i")

# Take a json of people, saves in skills.csv a list of all skills sorted without doubles
def create_dirty_skills_csv_file(people):
	allSkills = get_all_skills(people)
	allSkillsDF = pd.DataFrame(allSkills)
	allSkillsDF.to_csv("skills.csv", index = False, encoding = "utf-8")

# Take the name of a file containing a list of skills with doubles and the name of the file that will contain the cleaned skills
# Write in clean_skills_file a Data Frame in csv containing the skills cleaned (sorted, no doubles)
def last_clean_up_skills(dirty_skills_file, clean_skills_file):
	skills = [line.strip() for line in open(dirty_skills_file)]
	clean_skills = Set(skills)
	clean_skills_in_a_list = list(clean_skills)
	clean_skills_in_a_list.sort()
	allSkillsClean = pd.DataFrame(clean_skills_in_a_list)
	allSkillsClean.to_csv(clean_skills_file, index = False)

# Take the name of a file containing a Data Frame with clean skills, the name of the file that will contain the result, and a json object containing people
# Writes in the new file a data frame containing the count for each skill
def get_count_for_each_skill(my_skills_file, file_with_count_name, people):
	skills = [line.strip() for line in open(my_skills_file)]
	allSkillsDF = pd.DataFrame(skills)
	allSkillsDF.columns = ["Skills"]
	allSkillsDF['Count'] = 0
	for person in people:
		for index, row in allSkillsDF.iterrows():
			if row['Skills'] == 'd':
				if 'd' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'r':
				if 'r' in [x.lower() for x in person['skills']]:
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'c':  
				if 'c' in [x.lower() for x in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
				else: 
					for skill in person['skills']:
						if ('c/c++' in skill.lower()) or ('c++/c' in skill.lower()):
							allSkillsDF.ix[index, 'Count'] += 1 
							continue
			elif row['Skills'] == 'x':
				if 'x' in [x.lower() for x in person['skills']]:
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'io':
				if 'io' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'ip':
				if 'ip' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'ir':
				if 'ir' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'java':
				if 'java' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'art':
				if 'art' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'git':
				if 'git' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'cs':
				if 'cs' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'go':
				if 'go' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'cl':
				if 'cl' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'css':
				if 'css' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'js':
				if 'js' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'ml':
				if 'ml' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'sql':
				if 'sql' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'data':
				if 'data' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'learning':
				if 'learning' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'mac':
				if 'mac' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'rails':
				if 'rails' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'ruby':
				if 'ruby' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
			elif row['Skills'] == 'ux':
				if 'ux' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue

			elif row['Skills'] == 'backbone.js':
				if 'backbone' in [skill.lower() for skill in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
				else:
					for skill in person['skills']:
						if ('backbone.js' in skill.lower()) or ('backbone-js' in skill.lower()):
							allSkillsDF.ix[index, 'Count'] += 1 
							continue
			elif row['Skills'] == ('biking'):
				for skill in person['skills']:
					if ('bicycle' in skill.lower()) or ('bicycling' in skill.lower()) or ('biking' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'bittorrent':
				for skill in person['skills']:
					if ('bittorent' in skill.lower()) or ('bittorrent' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'coffeescript':
				for skill in person['skills']:
					if ('coffeescript' in skill.lower()) or ('coffescript' in skill.lower()) or ('cofeescript' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'cryptography':
				for skill in person['skills']:
					if ('cryptography' in skill.lower()) or ('crypto' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'front end':
				for skill in person['skills']:
					if ('front end' in skill.lower()) or ('front-end' in skill.lower()) or ('frontend' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'front end development':
				for skill in person['skills']:
					if ('front end development' in skill.lower()) or ('front-end development' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'full stack':
				for skill in person['skills']:
					if ('full stack' in skill.lower()) or ('full-stack' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'javascript':
				for skill in person['skills']:
					if ('javacript' in skill.lower()) or ('javascript' in skill.lower()) or ('javascrip'in skill.lower()) or ('javavscript' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'mapReduce':
				for skill in person['skills']:
					if ('map reduce' in skill.lower()) or ('map-reduce' in skill.lower()) or ('mapReduce' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'mathematics':
				for skill in person['skills']:
					if ('mathematics' in skill.lower()) or ('maths' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'artificial intelligence':
				if 'ai' in [x.lower() for x in person['skills']]:
					allSkillsDF.ix[index, 'Count'] += 1 
					continue
				else: 
					for skill in person['skills']:
						if ('artificial intelligence' in skill.lower()):
							allSkillsDF.ix[index, 'Count'] += 1 
							continue
			elif row['Skills'] == 'multithreading':
				for skill in person['skills']:
					if ('multithreading' in skill.lower()) or ('multthreading' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'objective c':   #not working ?!?
				for skill in person['skills']:
					if ('objective c' in skill.lower()) or ('obj-c' in skill.lower()) or ('objc' in skill.lower()) or ('objective-c' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'python':
				for skill in person['skills']:
					if ('python' in skill.lower()) or ('pytho' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'statistics':
				for skill in person['skills']:
					if ('statistics' in skill.lower()) or ('stats' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'technical writing':
				for skill in person['skills']:
					if ('technical writing' in skill.lower()) or ('tech writing' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'web development':
				for skill in person['skills']:
					if ('web development' in skill.lower()) or ('web dev' in skill.lower()) or ('web-dev' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'html':
				for skill in person['skills']:
					if ('html' in skill.lower()) or ('html5' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'node.js':
				for skill in person['skills']:
					if ('node' in skill.lower()) or ('node.js' in skill.lower()) or ('nodejs' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue
			elif row['Skills'] == 'ruby on rails':
				for skill in person['skills']:
					if ('rails' in skill.lower()):
						allSkillsDF.ix[index, 'Count'] += 1 
						continue

			else:
				for skill in person['skills']:
					if row['Skills'] in skill.lower():
						allSkillsDF.ix[index, 'Count'] += 1 
	allSkillsDF.to_csv(file_with_count_name, index = False)		
	#print allSkillsDF



# skills.csv and cleanSkills.csv files have been modified by hand
people = get_people_in_all_batches()
get_count_for_each_skill("cleanSkills.csv", "skillsCount.csv", people)





