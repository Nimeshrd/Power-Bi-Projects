
# Import necessary libraries
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv
import openai
import os
import requests
import re
import json
import datetime
from bson.decimal128 import Decimal128
from concurrent.futures import ThreadPoolExecutor, as_completed
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler
import os
import logging

#this is test

load_dotenv()

# Fetch environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
azure_openai_api_base = os.getenv('AZURE_OPENAI_API_BASE')
azure_openai_api_version= os.getenv("AZURE_OPENAI_API_VERSION")
num_candidates = int(os.getenv('NUM_CANDIDATES'))
database_name = os.getenv('DATABASE_NAME')
collection_name = os.getenv('COLLECTION_NAME')
vector_name = os.getenv('VECTOR_NAME')
base_uri = os.getenv('BASE_URI')
api_key = os.getenv('API_KEY')
app_insights_connection_string = os.getenv('APP_INSIGHTS_CONNECTION_STRING')
cosmosdb_connection_string= os.getenv('COSMOSDB_CONNECTION_STRING')
cosmos_uri = os.getenv('COSMOS_URI')
cosmos_key = os.getenv('COSMOS_KEY')
print(database_name)
 
# Connect to MongoDB 
# cosmos_client = CosmosClient(cosmos_uri, cosmos_key)
# database = cosmos_client.get_database_client(database_name)
# collection = database.get_container_client(collection_name)

# print(collection)
 

openai.api_type = "azure"
openai.api_key = openai_api_key
openai.api_base = azure_openai_api_base
openai.api_version = azure_openai_api_version
vectorName = vector_name
api_key = api_key
baseUri= base_uri

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
connection_string = app_insights_connection_string
logger.addHandler(AzureLogHandler(connection_string=connection_string))

logger.info('successfully printed by Nimish')
# if num_candidates is None or num_candidates==0:
#     query = "SELECT * FROM c"
#     data_collect = list(collection.query_items(query=query, enable_cross_partition_query=True))
#     total_documents = len(data_collect)
# else:
#     query = f"SELECT TOP {num_candidates} * FROM c"
#     data_collect = list(collection.query_items(query=query, enable_cross_partition_query=True))
#     total_documents = num_candidates


# BATCH_SIZE = int(os.getenv('batch_size'))
# input_tokens_sum = 0
# output_tokens_sum = 0
# total_tokens_sum = 0
# candidates_processed = 0

# def include_if_not_none(row, fields):
#     """
#     Creates a dictionary containing non-null values from the given row and fields.

#     Args:
#         row (dict): The row containing the values.
#         fields (list): The list of fields to include in the result.

#     Returns:
#         dict: A dictionary containing non-null values from the row and fields.
#     """

#     result = {}
#     for field in fields:
#         try:
#             if row[field] is not None:                
#                     result[field] = row[field]
#         except KeyError:
#             pass  # Ignore if the field doesn't exist in the row
#     return result

# def serialize_datetime(obj):
#     """
#     Serializes a datetime object into a string representation.

#     Args:
#         obj (datetime.datetime): The datetime object to be serialized.

#     Returns:
#         str: The serialized string representation of the datetime object.

#     Raises:
#         TypeError: If the input object is not of type datetime.datetime.
#     """
#     # if obj is not None :    
#     #     if isinstance(obj, datetime.datetime):
#     #         return obj.strftime('%Y-%m-%d')
#     #     raise TypeError("Type not serializable")
#     timestamp = obj /  1000000
 
#     # Convert to datetime object
#     date_available = datetime.datetime.utcfromtimestamp(timestamp)
 
#     # Format the datetime object as a string in ISO 8601 format
#     date_available_iso = date_available.strftime('%Y-%m-%dT%H:%M:%SZ')
   
#     return(date_available_iso)

# def process_candidate(row):
#     """
#     Process a candidate's data and generate a summary using OpenAI's GPT model, create vector embeddings and post to Azure AI Search index

#     Args:
#         row (dict): A dictionary containing the candidate's data.

#     Returns:
#         str: A success message if the candidate's data is processed successfully.
#         str: An error message if there is an issue with processing the candidate's data.
#     """    
#     descEmbeddings = None
#     educations = []
#     certifications = []
#     workHistories = []
#     references = []
#     openAIJson = []
#     global candidates_processed
#     global input_tokens_sum
#     global output_tokens_sum
#     global total_tokens_sum

#     openAIJson = include_if_not_none(row, [
#         'candidateId', 'candidateName', 'categories', 
#         'primarySpecialties', 'secondarySpecialties', 'yearsOfExperience', 
#         'description', 'certifications', 'workHistories', 
#         'zip', 'state', 'desiredLocations', 'willRelocate', 
#         'licenseStates', 'educations', 'dateAvailable', 'references'
#     ])    

#     if openAIJson.get('workHistories') is not None and len(openAIJson.get('workHistories')) > 0:
#         for wh in openAIJson.get('workHistories'):
#             newwh = include_if_not_none(wh, [
#                 'title', 'jobTitle', 'startDate', 'endDate', 
#                 'terminationReason', 'category', 'city', 
#                 'state', 'software', 'description'])          
#             if 'startDate' in wh and wh['startDate'] is not None:
#                 newwh['startDate'] = serialize_datetime(wh['startDate'])
#             if 'endDate' in wh and wh['endDate'] is not None:
#                 newwh['endDate'] = serialize_datetime(wh['endDate'])
#             workHistories.append(newwh)

#     if openAIJson.get('educations') is not None and len(openAIJson.get('educations')) > 0:
#         for edu in openAIJson.get('educations'):
#             newEdu = include_if_not_none(edu, ['degree', 'major'])
#             educations.append(newEdu)            
           
       
 
    
#     if openAIJson.get('certifications') is not None and len(openAIJson.get('certifications')) > 0:
#         for cert in openAIJson.get('certifications'):
#             newCert = include_if_not_none(cert, [
#             'name','displayStatus','boardCertification', 'location', 'issuedBy'])
#             certifications.append(newCert)           

#     if openAIJson.get('references') is not None and len(openAIJson.get('references')) > 0:
#         for ref in openAIJson.get('references'):
#             newref = include_if_not_none(ref, ['companyName', 'numReference'])
#             references.append(newref)             
    
#     if ('latitude' in row and 'longitude' in row):
#         # Convert Decimal128 objects to Decimal
#         latitude_decimal = row['latitude']
#         longitude_decimal = row['longitude']
        
#         # Then convert Decimal objects to floats
#         latitude = float(latitude_decimal)
#         longitude = float(longitude_decimal)               
#         geolocation = {"type": "Point", "coordinates": [longitude, latitude]}
#     else:
#         geolocation = {"type": "Point","coordinates": [0,0]}             

#     if educations:
#         openAIJson['educations'] = educations

#     if certifications:
#         openAIJson['certifications'] = certifications

#     if workHistories:
#         openAIJson['workHistories'] = workHistories

#     if references:
#         openAIJson['references'] = references    
    
#     try:
#         gptResponse = openai.ChatCompletion.create(
#             engine=os.getenv('AI_MODEL'),
#             messages=[
#                 {"role": "system", "content": "You are an expert in formatting json and extracting summary from it.The user provided json is a candidate data inclusive of details like educations, certifications, work histories, references, category, specialties, experience, zip, state, license states etc candidate is a applying for jobs within health care industry for nursing, allied, medical technicians etc positions. Read and extract data from provided JSON and summarize it into a paragraph not more than 15 lines. \n INSTRUCTIONS: You must extract and summarize details while excluding any unspecified information. Summary should include all details and names of the certifications, licenses, experience, location, work histories. These are crucial details and need precise information on certifications, licenses, experience, location, work histories. Your language must be neutral in summary. Exclude all personal information like contact number, email, address etc from your response. The response summary should only have details mentioned in json, do not infer additional conclusions on own."},
#                 {"role": "user", "content": str(openAIJson)}
#             ]
#         )
#         candidates_processed += 1
#         input_tokens_sum += gptResponse['usage']['prompt_tokens']
#         output_tokens_sum += gptResponse['usage']['completion_tokens']
#         total_tokens_sum += gptResponse['usage']['total_tokens']        
#         if (candidates_processed) % BATCH_SIZE == 0 or candidates_processed == total_documents:
#             logger.info(f'Token usage - Candidate processed: {candidates_processed}, Input Tokens : {input_tokens_sum}, Output Tokens : {output_tokens_sum}, Total Tokens : {total_tokens_sum}')
#             # Counters for tokens
#             input_tokens_sum = 0
#             output_tokens_sum = 0
#             total_tokens_sum = 0
#             candidates_processed = 0
    
#         logger.info(f'CandidateID: {row["candidateId"]}, InputTokens : {gptResponse["usage"]["prompt_tokens"]}, Output Tokens: {gptResponse["usage"]["completion_tokens"]}, Total Tokens: {gptResponse["usage"]["total_tokens"]}')

#         query = {"candidateId": row['candidateId']}
#         new_field = {"inputTokens": gptResponse['usage']['prompt_tokens'], "outputTokens": gptResponse['usage']['completion_tokens'], "totalTokens": gptResponse['usage']['total_tokens']}        

#         if "content" in gptResponse['choices'][0]['message']:
#             new_field["summary"] = gptResponse['choices'][0]['message']['content']

#             try:
#                 descResponse = openai.Embedding.create(
#                     input=gptResponse['choices'][0]['message']['content'],
#                     engine= os.getenv('EMBEDDING_MODEL')
#                 )
#                 descEmbeddings = descResponse['data'][0]['embedding']

#                 dataJson = {'value' : [{    
#                                 'descriptionVector':descEmbeddings,
#                                 'summary':gptResponse['choices'][0]['message']['content'],
#                                 'candidateId': str(row['candidateId']),
#                                 'candidateName': openAIJson.get('candidateName'),
#                                 'categories': openAIJson.get('categories') if openAIJson.get('categories') is not None else [],
#                                 'primarySpecialties': openAIJson.get('primarySpecialties') if openAIJson.get('primarySpecialties') is not None else [],
#                                 'secondarySpecialties': openAIJson.get('secondarySpecialties') if openAIJson.get('secondarySpecialties') is not None else [],
#                                 'description': openAIJson.get('description'),
#                                 'status': row['status'],
#                                 'yearsOfExperience': openAIJson.get('yearsOfExperience') if openAIJson.get('yearsOfExperience') is not None else "0",
#                                 'certifications': certifications,
#                                 'workHistories': workHistories,
#                                 'geoLocation': geolocation,
#                                 'zip': openAIJson.get('zip'),
#                                 'state': openAIJson.get('state'),
#                                 'desiredLocations': openAIJson.get('desiredLocations') if openAIJson.get('desiredLocations') is not None else [],
#                                 'willRelocate': openAIJson.get('willRelocate'),
#                                 'licenseStates': openAIJson.get('licenseStates') if openAIJson.get('licenseStates') is not None else [],
#                                 'educations': educations,
#                                 'dateAvailable': serialize_datetime(openAIJson.get('dateAvailable')) if openAIJson.get('dateAvailable') is not None else None,               
#                                 'references': references,
#                                 '@search.action': 'upload'
#                 }]}

#                 try:
#                     aiSearchResponse = requests.post(baseUri, json=dataJson, headers={'api-key': api_key, 'Content-Type': 'application/json'})

#                     if aiSearchResponse.status_code != 200:
#                         return f'Error posting for CandidateID: {row["candidateId"]}, Status: {aiSearchResponse.status_code}'
#                     else:
#                         logger.info(f'Successfully processed CandidateID: {row["candidateId"]}, Status: {aiSearchResponse.status_code}')
                                     
#                 except Exception as e:
#                     return f'Error posting to Azure AI for CandidateID: {row["candidateId"]}: {str(e)}'                

#             except openai.error.APIConnectionError as e:
#                 return f'API connection error while creating embedding for CandidateID: {row["candidateId"]}: {str(e)}'

#             except Exception as e:
#                 return f'Unexpected error while creating embedding for CandidateID: {row["candidateId"]}: {str(e)}'
#         else:

#             return f'Error creating chat completion due to context of CandidateID: {row["candidateId"]}'
        
#         patch_ops = [{"op": "add", "path": f"/{k}", "value": v} for k, v in new_field.items()]
#         collection.patch_item(item=row['id'], partition_key=row['candidateId'], patch_operations=patch_ops)
        
  

#     except openai.error.APIConnectionError as e:
#         return f'API connection error while creating chat completion for CandidateID: {row["candidateId"]}: {str(e)}'

#     except Exception as e:
#         return f'Unexpected error for CandidateID: {row["candidateId"]}: {str(e)}'
#     return None
    
# # Number of threads to use in the ThreadPoolExecutor
# num_threads = 10

# # Process candidates in batches using ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=num_threads) as executor:
#     """It is processing data related to "candidates" in a multithreaded manner, using the `concurrent.futures.ThreadPoolExecutor` class to create a pool of worker threads for executing calls asynchronously.

#     The `executor.submit` method schedules the `process_candidate` function to be executed and returns a Future object. A Future represents a computation that hasn't necessarily completed yet.

#     The `as_completed` function yields Futures as they complete. This is used in a loop to get the result of each Future with `future.result()`.

#     The code also includes several exception handling blocks to catch and handle different types of exceptions that might occur during the execution. 

#     The exceptions are caught and an error message is returned, including the ID of the candidate that caused the error. The error messages are then logged in the Application Insights."""    
#     futures = {executor.submit(process_candidate, row): row for row in data_collect}

    # for future in as_completed(futures):
    #     result = future.result()
    #     if result is not None:
    #         logger.exception(result)
