
#    pip install xmltodict


import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import xmltodict
import zipfile

from io import BytesIO

def download_data():
    county_result = requests.get("https://results.enr.clarityelections.com//MI/Oakland/105840/269402/reports/detailxml.zip")
    print(county_result.content)

    county_zip_data = BytesIO(county_result.content)
    county_zip_file = zipfile.ZipFile(county_zip_data)
    county_file = county_zip_file.open('detail.xml')
    county_xml = county_file.read()
    county_data = json.loads(json.dumps((xmltodict.parse(county_xml))))

    return county_data

elections_to_parse = ['Straight Party Ticket', 'Electors of President and Vice-President of the United States']
def process_data(data):
    records = []
    for election in data['ElectionResult']['Contest']:
        if election['@text'] not in elections_to_parse:
            continue
        if type(election['Choice']) is dict:
            election['Choice'] = [election['Choice']]
        for choice in election['Choice']:
            for vote_type in choice['VoteType']:
                if int(election['@precinctsReported']) == 1:
                    vote_type['Precinct'] = [vote_type['Precinct']]
                for precinct in vote_type['Precinct']:
                    records.append({
                        'choice':       choice['@text'],
                        'precinct':     precinct['@name'],
                        'election':     election['@text'],
                        'party':        choice.get('@party', 'Unaffiliated'),
                        'precinct':     precinct['@name'],
                        'votes':        int(precinct['@votes']),
                        'vote_type':    vote_type['@name'],
                    })
    return pd.DataFrame.from_records(records)

data = download_data()
election_df = process_data(data)

presidential_df = election_df[election_df['election'] == 'Electors of President and Vice-President of the United States']

choice_precinct_df = presidential_df.groupby(['precinct', 'choice']).sum().reset_index()
choice_precinct_df = choice_precinct_df[['precinct', 'choice', 'votes']].set_index('precinct')

total_votes_df = choice_precinct_df.groupby(['precinct']).sum().reset_index()
total_votes_df = total_votes_df[['precinct', 'votes']].set_index('precinct')

trump_df = choice_precinct_df[choice_precinct_df['choice'] == 'Donald J. Trump/Michael R. Pence']
trump_df = trump_df.drop('choice', 1)
biden_df = choice_precinct_df[choice_precinct_df['choice'] == 'Joseph R. Biden/Kamala D. Harris']
biden_df = biden_df.drop('choice', 1)

precinct_df = trump_df.join(biden_df, lsuffix = '_trump', rsuffix = '_biden')
precinct_df = precinct_df.join(total_votes_df)

straight_party_df = election_df[election_df['election'] == 'Straight Party Ticket']
straight_party_df = straight_party_df.groupby(['precinct', 'choice']).sum().reset_index()
straight_party_df = straight_party_df[['precinct', 'choice', 'votes']].set_index('precinct')

rep_df = straight_party_df[straight_party_df['choice'] == 'Republican Party']
rep_df = rep_df.drop('choice', 1)
dem_df = straight_party_df[straight_party_df['choice'] == 'Democratic Party']
dem_df = dem_df.drop('choice', 1)

party_df = rep_df.join(dem_df, lsuffix='_straight_rep', rsuffix='_straight_dem')

precinct_df = party_df.join(precinct_df)

precinct_df['republicanism'] = precinct_df['votes_straight_rep'] / (precinct_df['votes_straight_rep'] + precinct_df['votes_straight_dem'])
precinct_df['democratism'] = precinct_df['votes_straight_dem'] / (precinct_df['votes_straight_rep'] + precinct_df['votes_straight_dem'])
precinct_df['trump_share'] = precinct_df['votes_trump'] / precinct_df['votes']
precinct_df['trump_diff'] = precinct_df['trump_share'] - precinct_df['republicanism']
precinct_df['biden_share'] = precinct_df['votes_biden'] / precinct_df['votes']
precinct_df['biden_diff'] = precinct_df['biden_share'] - precinct_df['democratism']

precinct_df.to_csv('oakland_precincts.csv', encoding='utf-8')

import numpy as np
import statsmodels.api as sm

oakland_data_df = pd.read_csv('oakland_precincts.csv')
republicanism = oakland_data_df['republicanism']
plt.scatter(republicanism, oakland_data_df['trump_diff'], color='red')
plt.scatter(republicanism, oakland_data_df['biden_diff'], color='blue')
plt.show()

plt.scatter(republicanism, oakland_data_df['trump_share'], color='red')
plt.scatter(oakland_data_df['democratism'], oakland_data_df['biden_share'], color='blue')
plt.show()

plt.scatter(precinct_df['votes_trump'] - precinct_df['votes_straight_rep'], precinct_df['votes_straight_rep'])

X = np.transpose(np.matrix(republicanism))
X = sm.add_constant(X)
y = np.asarray(oakland_data_df['trump_diff'])

# Fit linear models to downballot performance
r_model = sm.OLS(y, X).fit()
print(r_model.summary)

y = np.asarray(oakland_data_df['biden_diff'])

d_model = sm.OLS(y, X).fit()
print(d_model.summary())

# Std of model residuals used as variance for true downballot performance
resid_std = np.std(r_model.resid)

# By construction in the initial set, republicanism = red_ballots / (rep_ballots + dem_ballots)
oakland_rep_sim = republicanism
oakland_dem_sim = 1 - oakland_rep_sim

# Simulation vote fraction for each candidate
oakland_trump_sim = oakland_rep_sim + np.random.normal(r_model.params[0], resid_std, len(oakland_rep_sim))
oakland_biden_sim = oakland_dem_sim + np.random.normal(d_model.params[0], resid_std, len(oakland_rep_sim))

# Swap Votes
oakland_observed_trump_sim = oakland_trump_sim * (1 + r_model.params[1])
oakland_observed_biden_sim = oakland_biden_sim - oakland_trump_sim * r_model.params[1]

# Observed performane
oakland_trump_odiff_sim = oakland_observed_trump_sim - oakland_rep_sim
oakland_biden_odiff_sim = oakland_observed_biden_sim - oakland_dem_sim

# Actual Performance
oakland_trump_diff_sim = oakland_trump_sim - oakland_rep_sim
oakland_biden_diff_sim = oakland_biden_sim - oakland_dem_sim

# Plot
plt.scatter(republicanism, oakland_trump_odiff_sim, color='red')
plt.scatter(republicanism, oakland_biden_odiff_sim, color='blue')
plt.show()

plt.scatter(republicanism, oakland_trump_diff_sim, color='red')
plt.scatter(republicanism, oakland_biden_diff_sim, color='blue')
plt.show()

fig, axs = plt.subplots(2,1)
axs[0].scatter(republicanism, oakland_data_df['trump_diff'], color='red')
axs[0].scatter(republicanism, oakland_data_df['biden_diff'], color='blue')

axs[1].scatter(republicanism, oakland_trump_odiff_sim, color='red')
axs[1].scatter(republicanism, oakland_biden_odiff_sim, color='blue')
plt.show()