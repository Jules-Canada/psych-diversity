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


conn = psycopg.connect(host="localhost", dbname="aact2025", user="juliecannon", password="test")
cur = conn.cursor()

def sex_from_nct_id(nct_id):
	count_male = 0
	count_female = 0


	query = "SELECT * FROM ctgov.baseline_measurements WHERE nct_id = '{}';".format(nct_id)

	data = pd.read_sql(query, conn)


	for index, row in data.iterrows():
		if row['category'] == 'Female':
			count_female += int(row['param_value'])
		elif row['category'] == 'Male':
			count_male += int(row['param_value'])

	return {'count_male': count_male, 'count_female': count_female}

def ethnicity_from_nct_id(nct_id):
	count_hispanic = 0
	count_non_hispanic = 0
	count_unknown_ethnicicty = 0

	query = "SELECT * FROM ctgov.baseline_measurements WHERE nct_id = '{}';".format(nct_id)

	data = pd.read_sql(query, conn)

	for index, row in data.iterrows():
		if row['title'] == 'Ethnicity (NIH/OMB)':
			if row['category'] == 'Hispanic or Latino':
				count_hispanic += int(row['param_value'])
			elif row['category'] == 'Not Hispanic or Latino':
				count_non_hispanic += int(row['param_value'])
			elif row['category'] == 'Unknown or Not Reported':
				count_unknown_ethnicicty += int(row['param_value'])

	return {'count_hispanic': count_hispanic, 'count_non_hispanic': count_non_hispanic,
			'count_unknown_ethnicicty': count_unknown_ethnicicty}

def race_from_nct_id(nct_id):
	count_american_indian_native = 0
	count_asian = 0
	count_hawaiian_pacific_islander = 0
	count_black = 0
	count_white = 0
	count_multiracial = 0
	count_unknown_race = 0

	query = "SELECT * FROM ctgov.baseline_measurements WHERE nct_id = '{}';".format(nct_id)

	data = pd.read_sql(query, conn)

	for index, row in data.iterrows():
		if row['title'] == 'Race (NIH/OMB)':
			if row['category'] == 'American Indian or Alaska Native':
				count_american_indian_native += int(row['param_value'])
			elif row['category'] == 'Asian':
				count_asian += int(row['param_value'])
			elif row['category'] == 'Native Hawaiian or Other Pacific Islander':
				count_hawaiian_pacific_islander += int(row['param_value'])
			elif row['category'] == 'Black or African American':
				count_black += int(row['param_value'])
			elif row['category'] == 'White':
				count_white += int(row['param_value'])
			elif row['category'] == 'More than one race':
				count_multiracial += int(row['param_value'])
			elif row['category'] == 'Unknown or Not Reported':
				count_unknown_race += int(row['param_value'])

	return {'count_american_indian_native': count_american_indian_native,
			'count_asian': count_asian,
			'count_hawaiian_pacific_islander': count_hawaiian_pacific_islander,
			'count_black': count_black,
			'count_white': count_white,
			'count_multiracial': count_multiracial,
			'count_unknown_race': count_unknown_race}


print (race_from_nct_id('NCT04848220'))
