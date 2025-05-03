# Jules / Julie Cannon May 1, 2025
# For analysis of psychiatry trial diversity
# Don't ask me about SQL
# Please take mercy on my formatting I don't know how to code

#load packages - they are probably all important, who could say
import psycopg
import sqlalchemy
import sys, os
import numpy as np
import pandas as pd
import json
from scipy import stats
import itertools
from datetime import date 
import csv


# CONNECT TO THE MAGIC OF SQL
# We currently use a static copy through AACT
conn = psycopg.connect(host="localhost", dbname="aact2025", user="juliecannon", password="test")
cur = conn.cursor()


# CREATE A LIST WITH PSYCH CONDITIONS BY GROUPING
# This should live in a function
Anxiety_Disorders = []
Mood_Disorders = []

with open('psych_conditions.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        print(row)
        if row["Classification"] == "Anxiety Disorders":
            Anxiety_Disorders.append(row["Disease"])

        elif row["Classification"] == "Mood Disorders":
            Mood_Disorders.append(row["Disease"])

All_Neuro = (Anxiety_Disorders + Mood_Disorders)


# FIND ALL NCTIDS MATCHING A LIST OF CONDITIONS
def applicable_studies(all_condition_list):
	applicable_studies_nct_ids = []

	for condition in all_condition_list:
		#condition = condition.translate(None,"'")
		condition = condition.upper()

		query = """SELECT nct_id from ctgov.studies where UPPER(brief_title) like '%{}%' 
			Union select nct_id from ctgov.browse_conditions where UPPER(mesh_term) like '%{}%' 
			Union select nct_id from ctgov.conditions where UPPER(name) like '%{}%' 
			Union select nct_id from ctgov.keywords where UPPER(name) like '%{}%';""".format(condition,condition,condition,condition)

		print('NOW RUNNING QUERY: ')
		print(query)

		data = pd.read_sql(query, conn)

		applicable_studies_nct_ids.append(data['nct_id'].tolist())

	# Flatten the list
	applicable_studies_nct_ids1 = list(itertools.chain.from_iterable(applicable_studies_nct_ids)) 
	# Remove Duplicates by making a set
	allNCTSet = set(applicable_studies_nct_ids1)
	applicable_studies_nct_ids = list(allNCTSet)

	return applicable_studies_nct_ids


# FINDS ALL STUDIES FOR A GIVEN MONTH AND YEAR
def filter_study_nct_by_date(nct_id_list,year,month):
	output_nct_ids = []

	query = """SELECT nct_id from ctgov.studies where study_first_submitted_date >= '{}-{}-01' AND
			   study_first_submitted_date <= '{}-{}-{}'""".format(str(year),str(month['month']),
			   str(year),str(month['month']),str(month['day']))
	data = pd.read_sql(query, conn)['nct_id'].tolist()

	for i in nct_id_list:
		if i in data:
			output_nct_ids.append(i)

	return output_nct_ids


# FINDS ALL STUDIES FOR A GIVEN MONTH AND YEAR
def filter_study_nct_by_year(nct_id_list,year):
	output_nct_ids = []

	query = """SELECT nct_id from ctgov.studies where study_first_submitted_date >= '{}-01-01' AND
			   study_first_submitted_date <= '{}-12-31'""".format(str(year),
			   str(year))
	data = pd.read_sql(query, conn)['nct_id'].tolist()

	for i in nct_id_list:
		if i in data:
			output_nct_ids.append(i)

	return output_nct_ids


# FIND ALL PSYCH STUDY NCT IDS FOR A GIVEN SET OF YEARS
def all_psych_studies(start_year,end_year):
	output = {}

	all_neuro_studies = applicable_studies(All_Neuro)

	for year in range(start_year,end_year):
		year_study_ids = filter_study_nct_by_year(all_neuro_studies,year)
		output[str(year)] = year_study_ids
		print('***' + str(year) + '***')
		print(year_study_ids)
		
psych_studies_by_year_df = pd.DataFrame(all_psych_studies(2023,2025))
