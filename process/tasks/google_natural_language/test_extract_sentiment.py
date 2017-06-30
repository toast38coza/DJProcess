from google.cloud import language
client = language.Client()
import csv

def get_sentiment(message):
    doc = client.document_from_text(message)

f_in = open('/Users/toast38coza/Downloads/verbatims.csv', 'rb')
f_out = open('/Users/toast38coza/Downloads/verbatims-new.csv', 'wb')
reader = csv.reader(f_in)
writer = csv.writer(f_out)
entities = {}
default_blank_entity = {'instances': []}
for row in reader:
    text = row[5]
    doc = client.document_from_text(text)
    result = doc.annotate_text(include_sentiment=True, include_syntax=False, include_entities=True)
    row.append(result.sentiment.score)
    row.append(result.sentiment.magnitude)
    writer.writerow(row)

    for e in result.entities:
        key = '{}:{}'.format(e.name, e.entity_type)
        instance = {
            'name': e.name,
            'type': e.entity_type,
            'salience': e.salience,
            'sentiment': e.sentiment,
            'doc': text
        }
        entity = entities.get(key, default_blank_entity)
        entity.get('instances').append(instance)


# f_in.close()
# f_out.close()


