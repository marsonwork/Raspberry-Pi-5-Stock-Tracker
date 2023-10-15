#Inclues
import time
#Includes: To parse web page
import requests
from bs4 import BeautifulSoup
#Inclues : To send email
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to check Raspberry Pi stock availability
def pi_stock_availability():
    # URL of the website you want to parse
    url_pi5 = 'https://robu.in/product/raspberry-pi-5-model-8gb/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # Send an HTTP GET request to the URL
    response = requests.get(url_pi5, headers=headers)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the element with class "electro-stock-availability"
        stock_element = soup.find(class_="electro-stock-availability")
        if stock_element:
            # Print the text content of the element
            stock_availability = stock_element.get_text()
        else:
            stock_availability = "Stock availability not found on the page."
        return stock_availability
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# Function to send an email
def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the appropriate SMTP server for your email provider
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Email sending failed. Error: {str(e)}')

# Function to execute the main logic
def main():
    global email_sent  # Use the email_sent variable from the outer scope
    while True:  # Run the check continuously
        stock_availability = pi_stock_availability()
        print("Pi 5 Availability:", stock_availability)
        if stock_availability == "In stock"  and not email_sent:
            print('Hurraah!! Raspberry Pi 5 is in Stock')
            with open('email-config.json') as config_file:
                config = json.load(config_file)
            with open('recipient-mail-data.json') as config_file:
                recipient_config = json.load(config_file)
            
            sender_email    = config['sender_email']
            sender_password = config['sender_password']
            recipient_email = recipient_config['recipient_email']
            subject         = recipient_config['subject']
            message_body    = recipient_config['message_body']

            send_email(sender_email, sender_password, recipient_email, subject, message_body)
            email_sent = True  # Set the email_sent variable to True
        elif stock_availability != "In stock":
            # Reset the email_sent flag if the Raspberry Pi is out of stock
            email_sent = False

        # Sleep for 5 minutes before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()
