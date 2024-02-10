import requests
import os
import csv
from dotenv import load_dotenv
from utils import extract_id_from_token, format_iso8601, transform_cadence

load_dotenv()

OUTPUT_DIRECTORY = "output"
OUTPUT_FILE_NAME = "subscription-contracts.csv"


class SubscriptionProcessor:
    def __init__(self, api_url, access_token):
        self.api_url = api_url
        self.access_token = access_token
        self.subscriptions = []

    def fetch_data(self, endpoint):
        headers = {
            "X-Recharge-Access-Token": self.access_token,
            "Accept": "application/json",
        }
        response = requests.get(f"{self.api_url}{endpoint}", headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data: {response.status_code}")
        return response.json()

    def fetch_subscriptions(self):
        subscriptions = self.fetch_data(
            "/subscriptions?status=active&limit=250")["subscriptions"]
        self.subscriptions = [self.process_subscription(
            sub) for sub in subscriptions]
        return self.subscriptions

    def subscription_keys(self):
        return self.subscriptions[0].keys() if len(self.subscriptions) > 0 else None

    def default_payment_method(self, customer_id):
        payment_data = self.fetch_data(
            f"/payment_methods?customer_id={customer_id}")
        for payment_method in payment_data["payment_methods"]:
            if payment_method["default"]:
                return payment_method
        return None

    def process_subscription(self, subscription):
        address_id = subscription["address_id"]
        customer_id = subscription["customer_id"]

        address = self.fetch_data(f"/addresses/{address_id}?active=true")
        payment_method = self.default_payment_method(customer_id)

        subscription.update(address)
        subscription["payment_method"] = payment_method
        transformed_subscription = self.transform_subscription(subscription)

        return transformed_subscription

    def transform_subscription(self, data):
        cadence_interval, cadence_interval_count = transform_cadence(
            data["order_interval_unit"], data["order_interval_frequency"])

        return {
            "handle": data["id"],
            "upcoming_billing_date": format_iso8601(data["next_charge_scheduled_at"]),
            "customer_id": data["payment_method"]["processor_customer_token"],
            "currency_code": data["presentment_currency"],
            "status": data["status"],
            "cadence_interval": cadence_interval,
            "cadence_interval_count": cadence_interval_count,
            "customer_payment_method_id": extract_id_from_token(data["payment_method"]["processor_payment_method_token"]),
            "delivery_price": 0,
            "delivery_method_type": "Shipping",
            "delivery_address_first_name": data["address"]["first_name"],
            "delivery_address_last_name": data["address"]["last_name"],
            "delivery_address_address1": data["address"]["address1"],
            "delivery_address_address2": data["address"]["address2"],
            "delivery_address_city": data["address"]["city"],
            "delivery_address_province_code": data["address"]["province"],
            "delivery_address_country_code": data["address"]["country_code"],
            "delivery_address_company": data["address"]["company"],
            "delivery_address_zip": data["address"]["zip"],
            "delivery_address_phone": data["address"]["phone"],
            "delivery_local_delivery_phone": "",
            "delivery_local_delivery_instructions": "",
            "delivery_pickup_method_location_id": "",
            "line_variant_id": data["shopify_variant_id"],
            "line_quantity": data["quantity"],
            "line_current_price": data["price"],
            "line_selling_plan_id": "",
            "line_selling_plan_name": "",
        }


def generate_csv(data, directory, filename, column_names):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=column_names, extrasaction="ignore")
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def main():
    api_url = os.getenv("API_URL")
    access_token = os.getenv("ACCESS_TOKEN")
    if not api_url or not access_token:
        raise EnvironmentError("Required environment variables are missing.")

    processor = SubscriptionProcessor(api_url, access_token)
    data = processor.fetch_subscriptions()

    generate_csv(data, OUTPUT_DIRECTORY, OUTPUT_FILE_NAME,
                 processor.subscription_keys())


if __name__ == "__main__":
    main()
