import dotenv
import concurrent.futures
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
import ast

def process_question(question):
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        question,
        temperature=0.3,
        max_output_tokens=1024,
    )
    return response.text.strip().strip('`').replace("json", "")


def get_response(url):

    # Load environment variables
    dotenv.load_dotenv(".env", override=False)

    aiplatform.init(project='datascience-393713')

    get_merchant_name = f"Extract the company name from the following website: {url}. Return the answer in a JSON " \
                        f"format of one line, with key='company' and value='RESPONSE'"
    get_description = f"Use the following url: {url}. Describe the company in up to five sentences, and no less than " \
                      f"three sentences. Focus on what they do as a company, and what services they offer. Be neutral " \
                      f"and descriptive. Return the answer in a JSON format of one line, " \
                      f"with key='description' and value='Your RESULT'"
    get_industry = f"Review the following company website: {url}. See this list of one-word industry descriptions: " \
                   f"'Retail, Financial Services, Travel, Gaming, Crypto, Software Subscription, Gambling, " \
                   f"Ticketing, Delivery'. Choose the description that suits the provided company the most. You can " \
                   f"only use the options provided above, don't invent other options. Return the answer in a json " \
                   f"format of one line, with key='industry' and value='Your choice'"
    get_channels = f"Review the following company website: {url}. See this list of selling channel options: " \
                   f"'Website, Mobile app, 3rd party / reseller, Phone calls'. Choose only the options the provided " \
                   f"company uses to sell their products. You can only choose out the options provided above, " \
                   f"don't invent other options. Return the answer in a json format of one line, with key='channels' " \
                   f"and value='Your choices'"
    get_billing = f"Review the following company website: {url}. See this list of billing models: 'One time payment, " \
                  f"Subscriptions, Installments'. out of this list, Choose only the options the provided company " \
                  f"offers. You can only choose out the options provided above, don't show other options. Choose as " \
                  f"many answers as applicable, but not options that are not listed. Return the answer in a json " \
                  f"format of one line, with key='billings' and value='Your choices'"
    get_email_address = f"`Review the following company website: {url}. What is their customer support email? " \
                        f"Return the answer in a json format of one line, with key='emailAddress' " \
                        f"and value='Your choice'"
    get_customer_support = f"`Go to {url}. Read through the Terms of Service. What is the maximal timeframe mentioned " \
                           f"per purchase for customer support? Summarize it and also provide the relevant paragraph " \
                           f"from the Terms of Service and save it as quote. If there are any specific conditions for " \
                           f"it, mention them. Provide URL for the source you use for your answer. Return the answer " \
                           f"in a json format of one line, with keys: ['timeframe', 'summary', 'quote' , " \
                           f"'specificConditions', 'source'] and values ['DAYS', 'SUMMARY', 'PARAGRAPH', " \
                           f"'SPECIFIC CONDITIONS', 'SOURCE']. If you do not have an answer to one of the options, " \
                           f"write 'NULL'."
    get_cencellation = f"`Go to {url}. Read through the Terms of Service. What is the maximal timeframe mentioned " \
                       f"per purchase for the cancellation policy? Summarize it and also provide the relevant " \
                       f"quotes from the Terms of Service. If there are any specific conditions for it, mention them. " \
                       f"Provide URL for the source you use for your answer. Return the answer in a json format of " \
                       f"one line, with keys: ['timeframe', 'summary', 'quote' , 'specificConditions', 'source'] " \
                       f"and values ['DAYS', 'SUMMARY', 'QUOTE', 'SPECIFIC CONDITIONS', 'SOURCE']. " \
                       f"If you do not have an answer to one of the options, write 'NULL'"
    get_refund_policy = f"Go to {url}. Read through the Terms of Service. Quote directly from the terms of service and " \
                        f"return the refund policy of the company. return it in a json format with key: 'refundPolicy' " \
                        f"and value: 'your REFUND POLICY'"

    questions = [get_merchant_name, get_description, get_industry, get_channels, get_billing, get_email_address,
                 get_customer_support, get_cencellation, get_refund_policy]

    # Using ThreadPoolExecutor to parallelize the processing of questions
    with concurrent.futures.ThreadPoolExecutor() as executor:
        responses = list(executor.map(process_question, questions))
    print("0: ", responses[0].strip().strip('`'))
    print("1: ", responses[1].strip().strip('`'))
    print("2: ", responses[2].strip().strip('`'))

    return responses

