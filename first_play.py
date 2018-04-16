import urllib3
import json
import re
import pandas as pd

http = urllib3.PoolManager()
response = http.request('GET',
    'http://ifsc.egroupware.net/egw/ranking/json.php?comp=6166&cat=5&route=2')
data = json.loads(response.data)
response2 = http.request('GET',
    'http://ifsc.egroupware.net/egw/ranking/json.php?comp=6166&cat=5&route=3')
final_data = json.loads(response2.data)


cols = ['ID','CompDate', 'LastName', 'FirstName',
        'FinalRank','SemiRank','QualyRank',
        'semi_boulder1_top', 'semi_boulder1_bonus',
        'semi_boulder2_top', 'semi_boulder2_bonus',
        'semi_boulder3_top', 'semi_boulder3_bonus',
        'semi_boulder4_top', 'semi_boulder4_bonus']


resultsTable = pd.DataFrame(index=range(0,20),columns = cols)


delimiters = 't', ' ', 'b'
regexPattern = '|'.join(map(re.escape, delimiters))
cols = ['boulder1','boulder2','boulder3','boulder4']

for i in range(0,len(data['participants'])):
    tempID = (data['participants'][i]['PerId'])    

    resultsTable.iloc[i]['ID'] = tempID
    resultsTable.iloc[i]['LastName'] =  data['participants'][i]['lastname']
    resultsTable.iloc[i]['FirstName'] =  data['participants'][i]['firstname']
    resultsTable.iloc[i]['QualyRank'] = data['participants'][i]['start_order']
    resultsTable.iloc[i]['SemiRank'] = data['participants'][i]['result_rank']    
    
    resultsTable.iloc[i]['CompDate'] = data['comp_date']


    for col in cols:
        score = re.split(regexPattern,data['participants'][i][col])
        
        if len(score) == 4:
            resultsTable.iloc[i]['semi_'+col+'_top'] = score[1]
            resultsTable.iloc[i]['semi_'+col+'_bonus'] = score[3]
        
        elif len(score) == 2:
            resultsTable.iloc[i]['semi_'+col+'_top'] = '0'
            resultsTable.iloc[i]['semi_'+col+'_bonus'] = score[1]
        else:
            print('result error: ' +str(i) + ' ' +col)     


