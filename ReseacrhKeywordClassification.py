# Utilising the IBM Watson service of AlchemyLanguageV1 to classify the research area of a scholar based on publication reocrds (top 50 cited)
import pymssql
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='')

conn = pymssql.connect(server='.', database='ScholarData')# Connecting to a local MSSQL DB storing collected scholar data
cursor1 = conn.cursor()
cursor2 = conn.cursor()
cursor1.execute('SELECT top(100) scholarID from Scholar')

scholarRow = cursor1.fetchone() # Fetch 1st row

while scholarRow:
    ScholarID = scholarRow[0]
    #Loading articles(title+abstract) associated with every scholar
    cursor2.execute('Select Article.ArticleTitle,Article.ArticleAbstract from Article inner join ScholarArticles on ScholarArticles.ArticleID=Article.ArticleID where ScholarArticles.ScholarID='+str(ScholarID))
    articleRow = cursor2.fetchone()
    textBody = "" #text to be submitted to AlchemyLanguage (i.e. a collection of top 50 cited publications (title+abstract only) of a scholar)
    while articleRow:
        textBody = textBody + articleRow[0]+"\n"+articleRow[1]#Publication Title
        textBody = textBody + articleRow[1]+"\n"#Publication Abstract
        articleRow = cursor2.fetchone()#Getting next article row

    scholarRow = cursor1.fetchone() #Getting next scholar row
print("###")
#print(textBody)
print("###")
#Sending request to AlchemyAPI
print("Sending request to Watson AlchemyAPI...")
# response = alchemy_language.concepts(text=textBody)
response = alchemy_language.combined(text=textBody, extract='concepts,taxonomy')
print(response)

if response['status'] == 'OK':
    print("###Concepts###")
    for concept in response['concepts']:
        conceptName = concept['text'].encode('utf-8')
        conceptRelevance = float(concept['relevance'])
        conceptDbpedia = concept['dbpedia']
        if conceptRelevance > 0.5:
            print(conceptName)
            print(conceptDbpedia)
    print("###Taxonomies###")
    for taxonomy in response['taxonomy']:
        taxonomyName = taxonomy['label'].encode('utf-8')
        taxonomyScore = float(taxonomy['score'])
        if taxonomyScore > 0.5:
            print(taxonomyName)
