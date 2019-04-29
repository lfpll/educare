from schema import classify_csv
from os import remove 
sample_data = [
    ['FIRST','SECOND','THIRD','FOURTH','FIFTH'],
    [1,2,3,4,5],
    ['TRUE',2,3,4,5],
    [0,'AEAEAE',3,4,5],
    ['FALSE',2,'02/04/2018','4.56',5],
    [1,'TESTE','30/12/1990',4.56,299]
]


response = {'FIRST':'BOOLEAN',
            'SECOND':'STRING',
            'THIRD':'DATETIME',
            'FOURTH':'FLOAT',
            'FIFTH':'INTEGER'}

    
def test_csv_assertion():
    with open('./tmp.csv','w') as file:
        map(file.write,sample_data)
    assert response == classify_csv('./tmp.csv')
    remove('./tmp.csv')