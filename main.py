import requests
import os
import csv
from dotenv import load_dotenv


load_dotenv()

if not os.getenv("ACCESS_TOKEN"):
    raise EnvironmentError(
        "Required environment variable 'ACCESS_TOKEN' is not set.")

output_directory = "assets"
output_file_name = "subscription-contracts.csv"
columns = ["id", "address1", "status", "next_charge_scheduled_at"]


def fetch_data(endpoint):
    access_token = os.getenv("ACCESS_TOKEN")
    api_url = os.getenv("API_URL")
    headers = {"X-Recharge-Access-Token": access_token,
               "Accept": "application/json"}

    response = requests.get(f"{api_url}{endpoint}", headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data:", response.status_code)

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


def generate_csv(data, dir, filename, column_names):
    if not os.path.exists(dir):
        os.makedirs(dir)

    file_path = os.path.join(dir, filename)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=column_names, extrasaction="ignore")
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def main():
    data = fetch_subscriptions()
    generate_csv(data, output_directory, output_file_name, columns)


if __name__ == "__main__":
    main()
