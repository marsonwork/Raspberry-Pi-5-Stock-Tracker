# Raspberry Pi 5 Stock Availability Notifier : v1.0.0

This Python script periodically checks the stock availability of Raspberry Pi 5 on a specified seller's website. If the product is in stock, it sends a notification email using Gmail.

## Prerequisites

Before running the script, make sure you have the following:

- Python installed (version 3.x recommended)
- Required Python packages installed (`requests`, `bs4` - BeautifulSoup, `smtplib`)
- Gmail account for sending notification emails

## Setup

1. **Install Dependencies:**

   ```bash
   pip install requests beautifulsoup4
   ```

2. **Create Configuration Files:**

   Create two JSON files in the same directory as the script:

   - **`email-config.json`**

     ```json
     {
       "sender_email": "your_email@gmail.com",
       "sender_password": "your_email_password"
     }
     ```

     Replace `"your_email@gmail.com"` with your Gmail email address and `"your_email_password"` with your Gmail password. Note: It's recommended to use an app password for enhanced security.

   - **`recipient-mail-data.json`**

     ```json
     {
       "recipient_email": "recipient_email@example.com",
       "subject": "Raspberry Pi 5 Availability Notification",
       "message_body": "Hurray! Raspberry Pi 5 is in stock now. Grab it before it's gone!"
     }
     ```

     Replace `"recipient_email@example.com"` with the email address where you want to receive notifications. Customize the subject and message body according to your preference.

3. **Run the Script:**

   Execute the script using:

   ```bash
   python script_name.py
   ```

   The script will run indefinitely, checking the stock availability every 5 minutes. If the Raspberry Pi 5 is in stock, it will send a notification email.

## Important Note

- Ensure that you comply with the terms of service of the seller's website when using this script.
- Use the script responsibly and avoid excessive requests to the seller's website to prevent any issues.
- Be cautious with storing email credentials directly in the script. Consider using secure methods for handling credentials.

Feel free to customize the script or improve it based on your needs!
```

Replace `"script_name.py"` with the actual name of your Python script. This README provides basic instructions for setup and usage. Adjustments can be made based on your specific requirements.
