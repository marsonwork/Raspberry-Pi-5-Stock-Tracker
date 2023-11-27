import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This function checks the stock availability of a product on a given URL
def stock_availability(url, stock_class):
    # Set the user agent header to make the request more human-like
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Send a GET request to the URL and retrieve the response
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element containing the stock information using the provided class name
        stock_element = soup.find(class_=stock_class)

        # Extract the stock availability text from the element
        if stock_element:
            stock_availability = stock_element.get_text().replace("Availability", "").strip()
        else:
            stock_availability = "Stock availability not found on the page."

        # Return the extracted stock availability
        return stock_availability
    else:
        # If the request failed, return an error message
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


# This function loads the email configuration from a JSON file
def config_email(config_file_path='email-config.json'):
    try:
        # Open the JSON file and load the configuration data
        with open(config_file_path) as config_file:
            config = json.load(config_file)

        # Extract the sender email, password, and recipient email from the configuration
        sender_email = config['sender_email']
        sender_password = config['sender_password']
        recipient_email = config['recipient_email']

        # Print a success message and return the extracted email details
        print("Email Configuration loaded successfully!")
        return sender_email, sender_password, recipient_email

    except Exception as e:
        # Print an error message and return None for all email details
        print(f"Error: {e}")
        return None, None, None

# This function sends an email notification using the provided email details and message
def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Create a multipart MIME message
    msg = MIMEMultipart()

    # Set the sender, recipient, and subject of the email
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body as plain text
    msg.attach(MIMEText(message, 'plain'))

    # Try to connect to the SMTP server and send the email
    try:
        # Connect to the Gmail SMTP server on port 587 and start TLS encryption
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()

        # Log in to the email account using the provided credentials
        smtp_server.login(sender_email, sender_password)

        # Send the email from the sender to the recipient
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the SMTP server connection
        smtp_server.quit()

        # Print a success message
        print('Email sent successfully!')

    except Exception as e:
        # Print an error message if sending the email fails
        print(f'Email sending failed. Error: {str(e)}')

def main():
    # Load the product details from a JSON file
    with open('products.json', 'r') as file:
        sellers_products = json.load(file)

    # Load the email configuration using the config_email function
    sender, password, recipient = config_email()

    # Iterate over the sellers and their products
    for seller, products in sellers_products.items():
        print(f"\nChecking products from {seller}:\n")

        # Iterate over each product and check its stock availability
        for product_id, details in products.items():
            url = details["url"]
            stock_class = details["stock_class"]

            # Initialize sent_flag or get its value if it already exists
            sent_flag = details['sent_flag']

            # Check the stock availability and update the sent_flag accordingly
            result = stock_availability(url, stock_class)

            print(f"{product_id} : {result}")

            if result.lower() not in ["out of stock", "sold out"] and not sent_flag:
                # If the product is available, send an email notification
                subject = f"Product Available: {product_id}"
                body = f"The product '{product_id}' from seller '{seller}' is now available. Check it out!"
                send_email(sender, password, recipient, subject, body)

                # Update the 'sent_flag' in the JSON file
                details['sent_flag'] = True

            elif result.lower() in ["out of stock", "sold out"]:
                # If the product is out of stock, reset the 'sent_flag'
                details['sent_flag'] = False

    # Save the updated product data back to the JSON file
    with open('products.json', 'w') as file:
        json.dump(sellers_products, file, indent=2)

if __name__ == "__main__":
    main()