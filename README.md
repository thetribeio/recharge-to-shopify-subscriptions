# Recharge to Shopify Subscriptions

This script facilitates the creation of a CSV file required to import subscription contracts into the [Shopify Subscriprions app](https://apps.shopify.com/shopify-subscriptions). It streamlines the process of transferring subscription data from Recharge to Shopify, making the migration smoother and more efficient.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry for dependency management

### Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/slavamak/recharge-to-shopify-subscriptions.git
```

2. Navigate to the project directory:
```bash
cd recharge-to-shopify-subscriptions
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Copy `.env.example` to `.env` and fill in the necessary environment variables:
```bash
cp .env.example .env
```
Edit `.env` to include your `ACCESS_TOKEN` and `API_URL`.

### Generating an API Key

Before using this script, you'll need to obtain an API token from Recharge. Follow the instructions provided in the [Recharge API documentation](https://docs.rechargepayments.com/docs/recharge-api-key) to generate your API key. Once obtained, add this key to your `.env` file as the `ACCESS_TOKEN`.

### Usage

To run the script, execute the following command:
```bash
poetry run python main.py
```
This will generate the CSV file needed for importing subscription contracts into Shopify Subscriptions, located at `output/subscription-contracts.csv`.

Please note that the current implementation does not support retrieving the shipping type and price for shipping.

## Dependencies

- Python 3.12
- Requests
- python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Limitations

The script does not currently support fetching shipping type and price. This feature was not implemented because, in the project's initial use case with a specific client, there was no configuration for shipping methods other than free shipping, making it impossible to test and unnecessary to include.

If you encounter a need for these shipping types and have suggestions for implementing this feature, please contribute your ideas by opening a [issue](https://github.com/slavamak/recharge-to-shopify-subscriptions/issues).

## License

This project is licensed under the [MIT License](LICENSE).
