# Cash or Trade

Cash or Trade is a web application built with Flask that allows users to list items for sale or trade. Users can register, log in, add items, edit items, and make offers on listings.

## Project Structure

```
.env
.gitignore
app.db
app.py
requirements.txt
.github/
    workflows/
        ec2_deploy.yml
cash_or_trade/
    auth.py
    db_client.py
    extensions.py
    models.py
    blueprints/
        accounts.py
        items.py
        listings.py
        purchases.py
static/
    styles.css
templates/
    base.html
    accounts/
        login.html
        register.html
    items/
        add_item.html
        edit_item.html
        delete_item.html
        show_item.html
        user_items.html
    listings/
        all_listings.html
        show_listing.html
        listing_offer.html
        example_email.html
```

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/cash-or-trade.git
    cd cash-or-trade
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables in a `.env` file:
    ```
    SECRET_KEY=your_secret_key
    DATABASE_CONNECTION=your_database_connection_string
    S3_ACCESS_KEY=your_s3_access_key
    S3_SECRET_ACCESS_KEY=your_s3_secret_access_key
    BUCKET_NAME=your_s3_bucket_name
    BUCKET_REGION=your_s3_bucket_region
    ```

5. Initialize the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Running the Application

1. Start the Flask development server:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Deployment

The project includes a GitHub Actions workflow for deploying to an EC2 instance. The workflow is defined in [`.github/workflows/ec2_deploy.yml`](.github/workflows/ec2_deploy.yml).

## Features

- User registration and login
- Add, edit, and delete items
- View all listings
- Make offers on listings
- Email notifications for offers

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
