# My Django E-commerce Project

This is a simple e-commerce application built with Django.

## Features
![Screenshot (13)](https://github.com/user-attachments/assets/4f8f177f-2bab-4674-8dfc-d68a6d35e745)
![Screenshot (12)](https://github.com/user-attachments/assets/9306ef75-da64-4af9-9e19-78e02fc43dd9)

### User registration and authentication
![Screenshot (11)](https://github.com/user-attachments/assets/69b557f7-c37a-46e8-9813-ac59f0120ee3)
![Screenshot (5)](https://github.com/user-attachments/assets/ec9431bb-e8c5-4c21-b13a-d095c58a0d7a)
![Screenshot (4)](https://github.com/user-attachments/assets/42e1f03c-624b-4973-bee9-a023e9e2b637)

### Product management as Admin
![Screenshot (3)](https://github.com/user-attachments/assets/80f3c188-2a62-4854-998d-0ca00c75b9a4)

### Search functionality
![Screenshot (6)](https://github.com/user-attachments/assets/1ed03f89-d123-49b8-9829-3e905ce95f94)

### Product listing and details
![Screenshot (7)](https://github.com/user-attachments/assets/ad2ecc95-0f2a-403f-b919-312a784fc4cc)

### Shopping cart functionality
![Screenshot (8)](https://github.com/user-attachments/assets/2d154557-edf0-466a-b4d9-109076f85c9d)

### Coupon functionality
![Screenshot (9)](https://github.com/user-attachments/assets/0b513b4f-7a7f-44ef-8807-459c09293254)

- Stripe payment integration
![Screenshot (10)](https://github.com/user-attachments/assets/a6da6528-4196-431b-9dad-2bf49a8e1ccc)
![Screenshot (2)](https://github.com/user-attachments/assets/86193668-91e6-4448-bfc8-901821f81a4b)


## Prerequisites

- Python 3.10 or higher
- Docker (for containerized setup)
- Git

## Setup

### Clone the repository

```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
### Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
Install dependencies
```
pip install -r requirements.txt
```
### Configure environment variables
Create a .env file in the project root directory and add the following:

```
SECRET_KEY=your_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
```
Apply migrations
```
python manage.py migrate
```
Collect static files
```
python manage.py collectstatic
```
Run the development server
```
python manage.py runserver
```
## Using Docker
Build the Docker image:

```
docker build -t mystore_khyati .
```
Run the Docker container:

```
docker run -d -p 8000:8000 mystore_khyati
```
