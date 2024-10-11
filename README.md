
# Ecommerce Platform with Stripe Integration, Coupon Functionality, and Chatbot

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
   - The chatbot communicates with the backend through webhooks, providing assistance on products, orders, and more.

### 8. **Email Verification**
   - During the registration process, users receive a verification email to ensure the authenticity of their account.

### 9. **Bootstrap Frontend**
   - The frontend UI is styled using **Bootstrap**, making it responsive and visually appealing across different devices.

## Installation

### 1. Clone the Repository

   ```bash
   git clone https://github.com/your-repo/ecommerce-platform.git
   cd ecommerce-platform
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

## Testing

1. **Coupon Testing**
   - Apply the coupon `firstbuy` during checkout to test discount functionality.

2. **Payment Testing**
   - Use the following test card information to test Stripe payment:
     - **Card Number:** `4242 4242 4242 4242`
     - **Expiry Date:** `12/34`
     - **CVC:** `567`
     - **ZIP Code:** `12345`

3. **Login Testing**
   - Use the test credentials:
     - **Email:** `test123@gmail.com`
     - **Password:** `123`

## Technologies Used

- **Backend:** Django
- **Frontend:** Bootstrap, HTML/CSS
- **Database:** PostgreSQL (or SQLite for development)
- **Payment Gateway:** Stripe
- **Chatbot:** Google Dialogflow (Webhook integration with Django backend)
- **Email Service:** Django's built-in email system (SMTP or any other email service)

## How to Contribute

Feel free to open issues or submit pull requests if you'd like to contribute to this project.

## License

This project is licensed under the MIT License.

---

This version specifies that the project is built with Django, keeping all the relevant details for users and developers. Let me know if you'd like to modify any section or add more details!
