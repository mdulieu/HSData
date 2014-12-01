import os
import requests
from numpy import array
from numpy import zeros
from numpy import savetxt
from scipy.cluster.vq import vq, kmeans2, whiten
from sets import Set

site = "https://www.hackerschool.com"
access_token = "?access_token=" + os.environ.get('HS_API_TOKEN')
caller_email = "mdulieu@gmail.com"

#Get all the people in the last two batches

allBatches = requests.get(site + '/api/v1/batches' + access_token)
#print allBatches.json()
#print allBatches.json()[0]
twoLastBatches = allBatches.json()[0:2]
#print twoLastBatches
#print twoLastBatches[0]['id']
currentPeople1 = requests.get(site + '/api/v1/batches/%d/people' % twoLastBatches[0]['id'] + access_token) 
currentPeople2 = requests.get(site + '/api/v1/batches/%d/people' % twoLastBatches[1]['id'] + access_token)
currentPeople = currentPeople1.json() + currentPeople2.json()
#for person in currentPeople:
#	print person['first_name']
#print len(currentPeople)

#Get the hackerschool id of the caller

for person in currentPeople:
	#print person['skills']
	if person['email'] == caller_email:
		#print person['first_name'], person['last_name']
		caller_id = person['id']
		print caller_id

#print caller_id
#Code if we don't find the caller_id

#list all the skills
#Clean-up of the skills: We need to extract skills from sentences and put everything in lower cases
first_name = []
last_name = []
people_id = []
people_dictionary = {}

allSkillsSet = Set([])
for person in currentPeople:
	first_name.append(person['first_name'])
	last_name.append(person['last_name'])
	people_id.append(person['id'])
	people_dictionary[person['id']] = person

	for skill in person['skills']:
		allSkillsSet.add(skill.lower())



#for skill in allSkills:
#	print skill

#print first_name
#print last_name
#print people_id

allSkills = list(allSkillsSet)
allSkills = sorted(allSkills)
#for index in range(len(allSkills)):
#	allSkills[index] = allSkills[index].lower()

#print allSkills
#for index, skill in enumerate(allSkills):
#	print(index, skill)

#for personIndex in range(len(currentPeople)):
#	for skillIndex in range(len(allSkills)):

peopleSkills = zeros((len(people_id), len(allSkills)))
for i, people in enumerate(people_id):
	for j, skill in enumerate(allSkills):
		peopleSkills[i,j]  = skill in people_dictionary[people]['skills']

savetxt("HSData.csv", peopleSkills, delimiter=",", fmt = "%5i")


