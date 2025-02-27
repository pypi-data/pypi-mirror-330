import smtplib
import imaplib
import email
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from langchain.tools import tool
import re, unicodedata
from datetime import datetime

def decode_email_body(part, default_encoding='utf-8'):
    """Safely decode email body with proper encoding handling"""
    charset = part.get_content_charset() or default_encoding
    payload = part.get_payload(decode=True)
    
    # Try common encodings if the specified one fails
    for encoding in [charset, 'utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']:
        try:
            return payload.decode(encoding, errors='replace')
        except (UnicodeDecodeError, LookupError):
            continue
    return payload.decode('utf-8', errors='replace')

def extract_text_and_links(html_content, extract_links=False,emailLength:int=None):
    """
    Extracts plain text and links from an HTML email content.

    Parameters:
        html_content (str): The raw HTML content of the email.
        extract_links (bool): Flag to determine whether to extract links.

    Returns:
        tuple: A tuple containing:
            - extracted_text (str): The plain text with all links removed.
            - links (list): A list of hyperlinks found in anchor tags.
    """
    # Normalize newlines
    html_content = html_content.replace("\r\n", "\n").replace("\r", "\n")
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract all hyperlinks from anchor tags
    links = [a['href'] for a in soup.find_all('a', href=True)] if extract_links else []
    
    # Convert the soup text to plain text
    text_content = soup.get_text(separator=' ')
    
    text_content = unicodedata.normalize("NFKC", text_content)

    # Remove all links, including those in parentheses and without anchor tags
    text_without_links = re.sub(r'https?://\S+|www\.\S+', '', text_content)
    text_without_links = re.sub(r'\(\s*https?://\S+\s*\)', '', text_without_links)  # Remove links in parentheses

    # Remove extra spaces left after link removal
    text_without_links = re.sub(r'\s+', ' ', text_without_links).strip().encode("utf-8", "ignore").decode("utf-8")

    if emailLength<=10:
        feasibleCharacters=1000
    elif emailLength>10 and emailLength<=20:
        feasibleCharacters=500
    elif emailLength>20 and emailLength<=30:
        feasibleCharacters=200
    elif emailLength>30:
        feasibleCharacters=100
    text_without_links=' '.join(text_without_links.split(' ')[0:feasibleCharacters])
    # print(len(text_without_links.split(' ')))

    return text_without_links, links

def clean_texts(text, emailLength:int):
    text_content = unicodedata.normalize("NFKC", text)

    # Remove all links, including those in parentheses and without anchor tags
    text_without_links = re.sub(r'https?://\S+|www\.\S+', '', text_content)
    text_without_links = re.sub(r'\(\s*https?://\S+\s*\)', '', text_without_links)  # Remove links in parentheses

    # Remove extra spaces left after link removal
    text_without_links = re.sub(r'\s+', ' ', text_without_links).strip().encode("utf-8", "ignore").decode("utf-8")
    if emailLength<=10:
        feasibleCharacters=1000
    elif emailLength>10 and emailLength<=20:
        feasibleCharacters=500
    elif emailLength>20 and emailLength<=30:
        feasibleCharacters=200
    elif emailLength>30:
        feasibleCharacters=100
    text_without_links=' '.join(text_without_links.split(' ')[0:feasibleCharacters])
    # print(len(text_without_links.split(' ')))

    return text_without_links

@tool('Email_Handler',return_direct=False)
def email_handler(action_type, subject=None, body=None, receiver_email=None, search_keyword=None, sender_email=None, date=None, start_date=None, end_date=None,file_name=None):
    """
    Handles sending and reading emails based on the action_type parameter. Read all params properly.
    Note: end_date-start_date<=20 days at max.
    Read-Only Access (USE FILE_SYSTEM_TOOL)→
        - This directory is called User WorkSpace (contains user's personal data)
        - `"MAS/PRIVATE/Emails"` (Contains personal emails)
        - `MAS/PRIVATE/Calendar"` (Contains calendar details)
        - put directory to these paths for emails,calendars,etc.
    Parameters:
        action_type (str): 'send' to send an email, 'read' to fetch emails.
        subject (str): Subject of the email (required for sending).
        body (str): Body of the email (required for sending). Ask human to verify body before sending.
        receiver_email (str): Receiver's email address (required for sending).
        search_keyword (str): Keyword to search for in emails (optional for reading).
        sender_email (str): Sender's email address to filter emails (optional for reading).
        date (str): Specific date to filter emails in the strict strict format "DD-MMM-YYYY" (when reading).
        start_date (str): Start date for filtering emails in the strict format "DD-MMM-YYYY" (when reading).
        end_date (str): End date for filtering emails in the strict format "DD-MMM-YYYY" (when reading).
        file_name (str): If email body is already written in a file, provide the file name and not text in <data> field.
    """
    # Gmail credentials
    email_account =  os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS") 
    imap_server = "imap.gmail.com"
    smtp_server = "smtp.gmail.com"
    extract_link=False

    if file_name is not None:
        with open(os.path.join('MAS','WORKSPACE',file_name), 'r') as f:
            body=f.read()

    

    if action_type == 'send':


        # Sending email
        if not subject or not body or not receiver_email:
            print("Error: Missing required parameters for sending an email.")
            return
        
        decision = input(f"Do you want to send following mail?(Y/N)\n SUBJECT: {subject}\n BODY: {body}\n\n")
        if any(word.lower() in ['no', 'n', 'exit', 'better', 'new', 'not'] for word in decision.split(' ')):
            return "Human rejected the mail. Write better mail by asking the requirements."

        # Create the email content
        message = MIMEMultipart()
        message["From"] = email_account
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, 587) as server:
                server.starttls()  # Secure the connection
                server.login(email_account, app_password)  # Log in with App Password
                server.sendmail(email_account, receiver_email, message.as_string())
                return "Email sent successfully!"
        except Exception as e:
            print(f"Error sending email: {e}")

    elif action_type == 'read':
        # Reading emails
        if not search_keyword and not sender_email and not date and not start_date and not end_date:
            start_date = datetime.now().strftime("%d-%b-%Y")  # Remove hyphens
            end_date = datetime.now().strftime("%d-%b-%Y")    # Remove hyphens

        try:
            # Connect to the Gmail IMAP server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_account, app_password)
            mail.select("inbox")

            # Build the search query based on provided parameters
            search_criteria = []
            if search_keyword:
                search_criteria.append(f'(BODY "{search_keyword}")')
            if sender_email:
                search_criteria.append(f'(FROM "{sender_email}")')
            if date:
                search_criteria.append(f'(ON "{date}")')  # Date format: DD-MMM-YYYY
            if start_date and end_date:
                search_criteria.append(f'(SINCE "{start_date}" BEFORE "{end_date}")')  # Date range

            # Combine all criteria into a single query string
            query = " ".join(search_criteria)

            # Search emails based on the query
            status, messages = mail.search(None, query)
            email_ids = messages[0].split()

            print(f"Found {len(email_ids)} emails matching the criteria: {query}.")

            # Prepare a dictionary to store all fetched emails
            emails_data = {}

            # Iterate over all matching emails and process them
            for idx, email_id in enumerate(email_ids):
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        sender = msg["from"]

                        # Check if the message is multipart or single-part
                        if msg.is_multipart():
                            body_text = ""
                            links = []
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    decoded_text = decode_email_body(part)
                                    body_text += decoded_text
                                    body_text = clean_texts(text=body_text, emailLength=len(email_ids))
                        else:
                            decoded_content = decode_email_body(msg)
                            body_text, links = extract_text_and_links(
                                decoded_content, 
                                extract_links=extract_link, 
                                emailLength=len(email_ids)
                            )

                        # Store the extracted data into a dictionary
                        emails_data[f"email_{idx + 1}"] = {
                            "subject": subject,
                            "sender": sender,
                            "body": body_text.strip(),
                            "links": links,
                        }

            # Save all fetched emails into a JSON file
            os.makedirs(os.path.join("MAS","PRIVATE","Emails"),exist_ok=True)
            with open(os.path.join("MAS","PRIVATE","Emails","emails.json"), "w", encoding="utf-8") as json_file:
                json.dump(emails_data, json_file, indent=4)


            # Close the connection
            mail.logout()


            return f"{len(email_ids)} Emails have been saved to 'emails.json' in directory MAS/PRIVATE/Emails" if len(email_ids) > 0 else "No emails found for this criteria"


        except Exception as e:
            print(f"Error reading emails: {e}")
    else:
        print("Error: Invalid action_type. Use 'send' or 'read'.")