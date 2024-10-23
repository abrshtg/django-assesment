# Django-Assesment

Create a Django API with django rest framework

- [ ]  users with custom roles - admin, coach, agent, football player
- [ ]  sign up and social sign up (google, facebook)
- [ ]  login and social login
- [ ]  password reset

---

# Django API with Custom User Roles and Social Authentication

This is a Django API built with Django Rest Framework (DRF) that includes custom user roles, authentication, social
signup/login, and password reset functionalities.

## Features

- **Custom User Roles**: `Admin`, `Coach`, `Agent`, `Football Player`.
- **User Signup/Login**: Traditional email/password signup and login.
- **Password Reset**: Reset password via email with token-based reset.
- **Social Signup/Login**: Google and Facebook social authentication.

---

## Installation and Setup

1. **Clone the Repository**:
    ```bash
    git clone git@github.com:abrshtg/django-assesment.git
    cd django-assesment
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Database**:
   Update your `settings.py` to configure the database:
   ```python
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
   }
   ```

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser** (for admin access):
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

---

## API Endpoints

### User Management

- **Signup**:
    - **POST** `/api/users/signup/`
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword",
        "role": "admin"  // or "coach", "agent", "football player"
    }
    ```

- **Login**:
    - **POST** `/api/users/login/`
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword"
    }
    ```

### Password Management

- **Password Reset Request**:
    - **POST** `/api/users/password-reset/`
    ```json
    {
        "email": "user@example.com"
    }
    ```

- **Password Change**:
    - **POST** `/api/users/password-change/`
    ```json
    {
        "email": "user@example.com",
        "token": "reset_token",
        "new_password": "newpassword"
    }
    ```

### Social Authentication

- **Social Signup/Login**:
    - **POST** `/api/users/social-login/`
    ```json
    {
        "provider": "google", // or "facebook"
        "access_token": "<your-access-token>"
    }
    ```

---

## Configuration

### Environment Variables

Make sure to configure your environment variables for security purposes. You can use a `.env` file for settings like
your database credentials, email backend, and social authentication credentials.

Example `.env` file:

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Facebook OAuth
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
```

### Email Backend

To enable the password reset functionality, configure the email backend in `settings.py`. For development, you can use
Django's console backend:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Swagger Docs

[http://localhost:8000/docs/](http://localhost:8000/docs/ "swagger docs")
---
