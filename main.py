import requests
import os
import csv


def fetch_data(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data:", response.status_code)

    subscriptions = response.json()["subscriptions"]
    data = []

    for subscription in subscriptions:
        address_id = subscription["address_id"]
        address_url = f"https://api.rechargeapps.com/addresses/{address_id}"

        address_response = requests.get(address_url, headers=headers)
        if address_response.status_code == 200:
            address_data = address_response.json()["address"]
            subscription.update(address_data)
            data.append(subscription)
        else:
            print(f"Failed to fetch address data for {
                  address_id}: ", address_response.status_code)

    return data


access_token = os.environ.get("ACCESS_TOKEN", "")
api_url = "https://api.rechargeapps.com/subscriptions"
headers = {"X-Recharge-Access-Token": access_token,
           "Accept": "application/json"}
data = fetch_data(api_url, headers)


def generate_csv(data, csv_file_path, column_names):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=column_names, extrasaction="ignore")
        writer.writeheader()
        for item in data:
            writer.writerow(item)


csv_file_path = "assets/subscriptions.csv"
column_names = ["id", "address1", "status", "next_charge_scheduled_at"]
generate_csv(data, csv_file_path, column_names)
