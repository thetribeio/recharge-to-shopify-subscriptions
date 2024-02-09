import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIRECTORY = "output"
OUTPUT_FILE_NAME = "subscription-contracts.csv"
COLUMNS = ["id", "address1", "status", "next_charge_scheduled_at"]


def fetch_data(endpoint):
    access_token = os.getenv("ACCESS_TOKEN")
    api_url = os.getenv("API_URL")
    if not access_token:
        raise EnvironmentError(
            "Required environment variable 'ACCESS_TOKEN' is not set.")

    headers = {"X-Recharge-Access-Token": access_token,
               "Accept": "application/json"}
    response = requests.get(f"{api_url}{endpoint}", headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data: {response.status_code}")

    return response.json()


def fetch_subscriptions():
    subscriptions = fetch_data("/subscriptions")["subscriptions"]
    data = []

    for subscription in subscriptions:
        address_id = subscription["address_id"]
        address_data = fetch_data(f"/addresses/{address_id}")["address"]
        subscription.update(address_data)
        data.append(subscription)

    return data


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
    data = fetch_subscriptions()
    generate_csv(data, OUTPUT_DIRECTORY, OUTPUT_FILE_NAME, COLUMNS)


if __name__ == "__main__":
    main()
