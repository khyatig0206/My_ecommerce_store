
# Ecommerce Platform with ChatBot

## Overview

This project is a full-featured Ecommerce platform built using **Django**, incorporating user authentication with email verification, Stripe payment gateway integration, coupon functionality, and a chatbot powered by **Dialogflow**. The platform also includes an admin panel for managing products, and an easy-to-use customer interface to add products to the cart and manage their orders.

## Features

### 1. **User Registration and Authentication**
   - Users can register and verify their email addresses to activate their accounts.
   - Login credentials for testing:
     - **Email:** `test123@gmail.com`
     - **Password:** `123`

### 2. **Coupon Functionality**
   - Customers can apply discount coupons at checkout.
   - Test coupon: `firstbuy` for a discount on the first purchase.

### 3. **Add to Cart**
   - Customers can browse through products, add them to their cart, and proceed to checkout.

### 4. **Stripe Payment Gateway Integration**
   - Secure payment processing is done via **Stripe**.
   - Use the following **test card details** to simulate payments:
     - **Card Number:** `4242 4242 4242 4242`
     - **Expiry Date:** `12/34`
     - **CVC:** `567`
     - **Name on Card:** `Test User`
     - **Country/Region:** India
     - **ZIP Code:** `12345`

### 5. **Orders Management**
   - Users can view their order history in a dedicated orders section.

### 6. **Admin Panel**
   - A powerful admin panel is provided to manage products, orders, and coupons.
   - Admins can add new products, edit existing ones, and track orders from customers.

### 7. **Chatbot Integration (Dialogflow)**
   - A customer support chatbot powered by **Dialogflow** is integrated with the platform.
   - The chatbot communicates with the backend through webhooks, enabling users to track order status through order ID and also enabling users to add items to cart by just using texts and it will search for the product in the database that user wants to order and add it to cart.

### 8. **Email Verification**
   - During the registration process, users receive a verification email to ensure the authenticity of their account.

### 9. **Bootstrap Frontend**
   - The frontend UI is styled using **Bootstrap**, making it responsive and visually appealing across different devices.

## Installation

### 1. Clone the Repository

   ```bash
   git clone https://github.com/khyatig0206/My_ecommerce_store.git 
   cd My_ecommerce_store
   ```

### 2. Install Dependencies

   Make sure you have `Python` and `pip` installed, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### 3. Set up Environment Variables

   Create a `.env` file to store your environment variables:

   ```
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   EMAIL_HOST_USER=your_email_user
   EMAIL_HOST_PASSWORD=your_email_password
   ```

### 4. Run Database Migrations

   Apply database migrations to set up the initial structure:

   ```bash
   python manage.py migrate
   ```

### 5. Run the Development Server

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

### 6. Access the Admin Panel

   You can access the Django admin panel at `http://localhost:8000/admin/` using the admin credentials created during setup.

## Technologies Used

- **Backend:** Django
- **Frontend:** Bootstrap, HTML/CSS
- **Database:** PostgreSQL (or SQLite for development)
- **Payment Gateway:** Stripe
- **Chatbot:** Google Dialogflow (Webhook integration with Django backend)
- **Email Service:** Django's built-in email system (SMTP or any other email service)

![Screenshot (150)](https://github.com/user-attachments/assets/723a9695-f11d-44fe-b263-7b0f9e5a2bee)

![Screenshot (148)](https://github.com/user-attachments/assets/fcb7827e-fdcf-4c5d-98f9-7e2dcdd4949e)
![Screenshot (147)](https://github.com/user-attachments/assets/3913ccb7-0e8e-4ff1-a9a5-8d9aa6357cd3)

![Screenshot (6)](https://github.com/user-attachments/assets/139e57e7-423f-4e16-909d-0b8893936079)
![Screenshot (151)](https://github.com/user-attachments/assets/bfae0be0-bb9b-4fc6-aabc-1c55e57a8f90)

![Screenshot (3)](https://github.com/user-attachments/assets/00d58183-87ed-4610-8069-b885161ae618)
![Screenshot (146)](https://github.com/user-attachments/assets/539d7478-ed28-4d27-8723-9189851f3389)

![Screenshot (152)](https://github.com/user-attachments/assets/081319f0-9c64-4acf-847e-3d375aaead66)

![Screenshot (2)](https://github.com/user-attachments/assets/82285918-af27-48a7-92e1-02d1b2b5b71b)

![Screenshot (142)](https://github.com/user-attachments/assets/c35e04a7-e65c-4f15-8a31-cc5abae588e1)

![Screenshot (143)](https://github.com/user-attachments/assets/c23e03b4-f070-4dfe-8dff-e2a329cbb832)

![Screenshot (144)](https://github.com/user-attachments/assets/6c3b1eeb-d5a4-488a-bd8b-c0b98d1f14eb)

![Screenshot (145)](https://github.com/user-attachments/assets/ace2026e-e6fb-443b-a97f-e4f6118e8b48)

![Screenshot (146)](https://github.com/user-attachments/assets/a57e2d32-c41f-4823-a5c9-3580d35a49ab)

![Screenshot (149)](https://github.com/user-attachments/assets/b7277449-38e2-484b-bda5-00634a51aea2)

## How to Contribute

Feel free to open issues or submit pull requests if you'd like to contribute to this project.

