import pymssql
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='1a65a9e520e3450fcf15949ebb62cda1498e5401')

conn = pymssql.connect(server='.', database='ScholarData')
cursor1 = conn.cursor()
cursor2 = conn.cursor()
cursor1.execute('SELECT scholarID from Scholar Where scholarID=1')


scholarRow = cursor1.fetchone() # Fetch 1st row
while scholarRow:
    #print("ScholarID="str(row[0]))# row[0] -> 1st column
    ScholarID=scholarRow[0]
    cursor2.execute('Select Article.ArticleTitle,Article.ArticleAbstract from Article inner join ScholarArticles on ScholarArticles.ArticleID=Article.ArticleID where ScholarArticles.ScholarID='+str(ScholarID))
    articleRow = cursor2.fetchone()
    while articleRow:
        textBody = articleRow[0]+". "+articleRow[1]
        #print(text)
        print("Sending request to Watson AlchemyAPI...")
        response = alchemy_language.concepts(text=textBody)
        if response['status'] == 'OK':
            print('## Concepts ##')
            for concept in response['concepts']:
                conceptName= concept['text'].encode('utf-8')
                conceptRelevance=  float(concept['relevance'])
                conceptDbpedia = concept['dbpedia']
                if conceptRelevance>0.5:
                    print(conceptName)

        articleRow = cursor2.fetchone()#Getting next article row

    scholarRow = cursor1.fetchone() #Getting next scholar row
