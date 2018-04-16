import urllib3
import json
import re
import pandas as pd


# import data from semis and finals for one comp
def dataGetter(compID):
    http = urllib3.PoolManager()
    
    response = http.request('GET',
        'http://ifsc.egroupware.net/egw/ranking/json.php?comp='+compID+'&cat=5&route=2')
    semi_data = json.loads(response.data)
    
    response2 = http.request('GET',
        'http://ifsc.egroupware.net/egw/ranking/json.php?comp='+compID+'&cat=5&route=3')
    final_data = json.loads(response2.data)
    
#    qualy1_resp = http.request('GET',
#       'http://ifsc.egroupware.net/egw/ranking/json.php?comp='+compID+'&cat=5&route=0')
#    qualy1_data = json.loads(qualy1_resp.data)
#    
#    qualy2_resp = http.request('GET',
#       'http://ifsc.egroupware.net/egw/ranking/json.php?comp='+compID+'&cat=5&route=1')
#    qualy2_data = json.loads(qualy2_resp.data)
#    return semi_data, final_data, qualy1_data, qualy2_data   
    return semi_data, final_data
# establish results table

def TableBuild(semi_data,final_data):
    ''' Takes a json file of data from the semi final and returns an empty
    pandas data frame using PerId and CompDate as index'''
    
    cols = ['CompDate', 'LastName', 'FirstName',
            'FinalRank','SemiRank','QualyRank',
            'semi_boulder1_top', 'semi_boulder1_bonus',
            'semi_boulder2_top', 'semi_boulder2_bonus',
            'semi_boulder3_top', 'semi_boulder3_bonus',
            'semi_boulder4_top', 'semi_boulder4_bonus']
    tempID = []
    for i in range(0,len(semi_data['participants'])):
        tempID.append((semi_data['participants'][i]['PerId'])+'-'+(semi_data['comp_date']))
    resultsTable = pd.DataFrame(index=tempID,columns = cols)


    delimiters = 't', ' ', 'b'
    regexPattern = '|'.join(map(re.escape, delimiters))
    cols = ['boulder1','boulder2','boulder3','boulder4']
    
    for i in range(0,len(semi_data['participants'])):
    
        resultsTable.iloc[i]['LastName'] =  semi_data['participants'][i]['lastname']
        resultsTable.iloc[i]['FirstName'] =  semi_data['participants'][i]['firstname']
        resultsTable.iloc[i]['QualyRank'] = semi_data['participants'][i]['start_order']
        resultsTable.iloc[i]['SemiRank'] = semi_data['participants'][i]['result_rank']       
        resultsTable.iloc[i]['CompDate'] = semi_data['comp_date']
    
        for col in cols:
            score = re.split(regexPattern,semi_data['participants'][i][col])
            
            if len(score) == 4:
                resultsTable.iloc[i]['semi_'+col+'_top'] = score[1]
                resultsTable.iloc[i]['semi_'+col+'_bonus'] = score[3]
            
            elif len(score) == 2:
                resultsTable.iloc[i]['semi_'+col+'_top'] = '0'
                resultsTable.iloc[i]['semi_'+col+'_bonus'] = score[1]
            else:
                print('result error: ' +str(i) + ' ' +col)     

    # get finals positions    
    
    for i in range(0,len(final_data['participants'])):
        climberId = final_data['participants'][i]['PerId']+'-'+final_data['comp_date']
        resultsTable.loc[climberId]['FinalRank'] = final_data['participants'][i]['result_rank']
    
    resultsTable['FinalRank'] = resultsTable['FinalRank'].fillna('0')
    
    #qualy results    
   
    
    return resultsTable


compList = ['6158','6166','6170','6174','6182','6252','6198']
results = pd.DataFrame()
for i in compList:
    df = dataGetter(i)
    
    table = TableBuild(df[0],df[1])
    results = results.append(table)
    
