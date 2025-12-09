# Deriv API Authentication and Application Setup Guide

This guide provides detailed instructions on how to create and collect credentials for Deriv API accounts, covering API authentication, OAuth2 setup, and application creation. Follow these steps to ensure a smooth integration process.

## API Authentication

### Introduction

Without proper authorization and authentication, access to the Deriv API is limited. For actions such as buying contracts or using Copy Trading features, users must be authenticated and authorized via OAuth and WebSocket Server.

### Requirements

- Deriv Client account
- Deriv API token with the appropriate access level
- Deriv app ID

**Note:** Refer to the [Setting up a Deriv application](https://api.deriv.com/docs/setting-up-a-deriv-application) for detailed instructions on creating a Deriv API token and application.

### API Token

An API token is a unique identifier for a client requesting access from a server. It is the simplest way to authorize users.

- Ensure the access level of each API token matches the required access level of the API call. Refer to the API Explorer for details.
- Keep the API token secure as it can be used with any app.

### OAuth2

OAuth2 is a protocol that allows a client to access resources on behalf of the user without revealing credentials. It is a safer method for sharing access.

For more information on OAuth2, visit [this guide](https://api.deriv.com/docs/core-concepts/authorization-authentication).

#### OAuth Flow

To authenticate a user via OAuth:

1. Specify the OAuth Authorization URL in the Dashboard on the Register Application tab.
2. Add a login button on your website/app directing users to `https://oauth.deriv.com/oauth2/authorize?app_id=your_app_id`, replacing `your_app_id` with your app ID.
3. Users will be redirected to your specified URL with their session tokens.

#### Example Authorization URL

```
https://[YOUR_WEBSITE_URL]/redirect/?acct1=cr799393&token1=a1-f7pnteezo4jzhpxclctizt27hyeot&cur1=usd&acct2=vrtc1859315&token2=a1clwe3vfuuus5kraceykdsoqm4snfq&cur2=usd
```

#### User Account Mapping

```javascript
const user_accounts = [
  {
    account: "cr799393",
    token: "a1-f7pnteezo4jzhpxclctizt27hyeot",
    currency: "usd",
  },
  {
    account: "vrtc1859315",
    token: "a1clwe3vfuuus5kraceykdsoqm4snfq",
    currency: "usd",
  },
];
```

#### Authorize API Call

```json
{
  "authorize": "a1-f7pnteezo4jzhpxclctizt27hyeot"
}
```

#### Example Authorization Response

```json
{
  "account_list": [
    {
      "account_type": "trading",
      "created_at": 1647509550,
      "currency": "USD",
      "is_disabled": 0,
      "is_virtual": 0,
      "landing_company_name": "svg",
      "loginid": "CR799393",
      "trading": {}
    },
    {
      "account_type": "trading",
      "created_at": 1664132232,
      "currency": "ETH",
      "is_disabled": 0,
      "is_virtual": 0,
      "landing_company_name": "svg",
      "loginid": "VRTC1859315",
      "trading": {}
    }
  ],
  "balance": 0,
  "country": "id",
  "currency": "USD",
  "email": "user_mail@email_provider.com",
  "fullname": "John Doe",
  "is_virtual": 0,
  "landing_company_fullname": "Deriv (SVG) LLC",
  "landing_company_name": "svg",
  "local_currencies": {
    "IDR": {
      "fractional_digits": 2
    }
  },
  "loginid": "CR799393",
  "preferred_language": "EN",
  "scopes": ["read", "trade", "trading_information", "payments", "admin"],
  "trading": {},
  "upgradeable_landing_companies": ["svg"],
  "user_id": 12345678
}
```

## Creating a Deriv Application

### Deriv Account

If you do not have a Deriv account, create one via the [signup page](https://deriv.com/signup/) or use the `new_account_virtual` API call. For real accounts, use `new_account_real` or `new_account_maltainvest` API calls.

**Caution:** Use a demo account for testing to avoid accidental loss of funds.

### Creating a Deriv API Token

1. Go to the Dashboard and select the Manage Tokens tab.
2. Create a new token with the required access level:
   - Select the scopes you need.
   - Provide a name for your token.
   - Click Create.

Alternatively, use the `api_token` API call.

**Caution:** An Admin scope token is required to create an application.

### Creating a Deriv Application

1. In the Dashboard, go to the Register Application tab.
2. Fill in the application details:
   - **Account:** The account used to create the application.
   - **API Token:** The Admin scope token for the account.
   - **App Name:** Name of the application.
   - **Markup:** Commission added to the trade price.
   - **Authorization URL:** URL for clients to log in to your app using Deriv accounts.
   - **Verification URL:** URL for email verification.
3. Select the required authorization scopes.
4. Click Register Application.

Ensure the authorization and verification URLs are correct based on your implementation.

For more details, refer to the [Setting up a Deriv application](https://api.deriv.com/docs/setting-up-a-deriv-application) guide.

### Modifying the `.env` File

After receiving your API token and app ID, update the `.env` file with these details. The `.env` file should be modified as follows:

```plaintext
DERIV_TOKEN='your_api_token'
APP_ID='your_app_id'
```

Replace `'your_api_token'` with the API token you received and `'your_app_id'` with your app ID.

## Running the Program

### Installing Dependencies

Ensure you are using a virtual environment to run this code. If not already done, set up and activate your virtual environment. Then, install the necessary dependencies by running:

```sh
pip install -r requirements.txt
```

#### Steps to Install Dependencies

1. Navigate to your project directory.
2. Ensure your virtual environment is activated:
   ```sh
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows
   ```
3. Run the installation command:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Trading Script

After setting up your environment and modifying the `.env` file, you can run the trading script by executing:

```sh
python main.py
```

## External Resources

1. [Setting up a Deriv application](https://api.deriv.com/docs/setting-up-a-deriv-application)
2. [Authorization and Authentication Core Concepts](https://api.deriv.com/docs/core-concepts/authorization-authentication)

Follow these steps to successfully create and collect credentials for Deriv API accounts, ensuring secure and efficient access to Deriv's features.
