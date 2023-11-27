# Raspberry Pi 5 stock tracker: v2.0.0

This Python script monitors the availability of specific Raspberry Pi 5 accessories from various sellers. It checks the stock status of the following products:

1. **Raspberry Pi 5 8GB Board**
2. **Active Cooler for Raspberry Pi 5**
3. **27 Watt Power Supply for Raspberry Pi 5**
4. **Case for Raspberry Pi 5**
5. **RTC Battery for Raspberry Pi 5**

## Usage

1. Install the required dependencies by running the following command:

    ```
    pip install beautifulsoup4 requests
    ```

2. Create a `products.json` file containing the details of the products to be monitored. The JSON file structure should be as follows:

    ```json
    {
      "seller_1": {
        "product_id_1": {
          "url": "product_url",
          "stock_class": "stock_class_selector",
          "sent_flag": false
        },
        "product_id_2": {
          "url": "product_url",
          "stock_class": "stock_class_selector",
          "sent_flag": false
        },
        ...
      },
      "seller_2": {
        ...
      },
      ...
    }
    ```

    - `"seller_1"`, `"seller_2"`, etc., are placeholders for the actual seller names.
    - `"product_id_1"`, `"product_id_2"`, etc., are placeholders for the product IDs.
    - `"product_url"` should be replaced with the URL of the product on the seller's website.
    - `"stock_class_selector"` should be replaced with the class selector for the HTML element indicating stock availability.
    - `"sent_flag"` is a boolean indicating whether an email notification has been sent for this product. Set it to `false` initially.

3. Create an `email-config.json` file with the email configuration. It should have the following structure:

    ```json
    {
      "sender_email": "your_email@gmail.com",
      "sender_password": "your_email_password",
      "recipient_email": "recipient_email@example.com"
    }
    ```

4. Run the script:

    ```
    python script_name.py
    ```

   Replace `script_name.py` with the actual name of your Python script.

## Email Notifications

The script uses the provided Gmail credentials to send email notifications when a product becomes available. Ensure that "Less secure app access" is enabled for the sender's Gmail account.

## Notes

- The script will update the `sent_flag` in the `products.json` file to avoid sending duplicate notifications for the same product.
- Check the console output for real-time updates on product availability.

Feel free to customize the script to track additional products or sellers as needed.
