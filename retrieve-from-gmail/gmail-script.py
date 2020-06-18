from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import base64
import email

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_api_service():
    """
    Use Gmail API to have access to my gmail account
    :return: Gmail service to make requests
    """
    creds = None
    creds_file = os.path.abspath('../../..') + '/credentials.json'
    token_file = os.path.abspath('../../..') + '/token.pickle'
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    # return the gmail service
    return build('gmail', 'v1', credentials=creds)


def list_message_ids(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return [message['id'] for message in messages]
    except errors.HttpError as error:
        print(f"An error occurred: {error}")


def get_message(service, user_id, msg_id):
    """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        # print(f"{message['payload']}")

        return message['payload']
    except errors.HttpError as error:
        print(f"An error occurred: {error}")


def get_subject(message):
    """
    Extract the subject of email from message object
    :param message: Gmail message object(json)
    :return: Subject text
    """
    for header in message['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
            problem_number = subject[subject.find('#'):subject.find('[')]
            difficulty = subject[subject.find('[') + 1: -1]
            return problem_number, difficulty


def get_body_section(message):
    """
    Extract section of body that contains Coding Problem question and example
    Note: The section contains the name of the big company and the interview question asked.

    :param message: Gmail message object(json)
    :return: tuple containing company and question asked
    """
    try:
        body = str(message['parts'][0]['body']['data'])
        body_decoded = base64.urlsafe_b64decode(body).decode()
        section = body_decoded[:body_decoded.index('--')].replace('\r\n\r', '').strip()
        company = section[section.find('by', 50) + 3: section.find('.', 70)]
        if 'asked' in company:
            # For email bodies missing the 'by' word mistakenly
            company = company[company.rfind(' '):]
        question = section[section.find('.', 65):]

        # company = The name of the company that asked the interview question
        return company, question
    except ValueError as err:
        print(err)


def main():
    """
    The main function to execute and integrate all function in one place
    :return: None for now
    """

    # Gmail API Service
    service = get_gmail_api_service()
    messages = list_message_ids(service=service,
                                user_id='me', query='"subject:Daily Coding Problem: Problem #"')
    for msg_id in messages:
        msg = get_message(service, user_id='me', msg_id=msg_id)
        print('Subject:', get_subject(msg))
        # print('Body:', get_body_section(msg))

    print(f"Daily Coding Problems sent {len(messages)} emails")


if __name__ == '__main__':
    pass
    main()
