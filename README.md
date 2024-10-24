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

## Social Authentication Flow (Google Example)

1. **Frontend**:

- Redirects the user to the Google authorization page for authentication.

```text
https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=<client_id>&redirect_uri=<redirect_uri>
&scope=email%20profile
```

2. **Google**:

- Prompts the user to select a Google account.
- Asks the user to authorize the app to access their profile and email.
- Sends a response to the redirect_uri with query parameters (code, scope, authuser, prompt).

3. **Frontend**:

- Uses the authorization code received to request an access token from Google:

```bash
POST https://oauth2.googleapis.com/token
{
client_id: <client_id>,
client_secret: <client_secret>,
code: <authorization_code>,
grant_type: authorization_code,
redirect_uri: <redirect_uri>
}
```

4. **Google**:

- Returns the following information to the frontend:
    - `access_token`
    - `expires_in`
    - `scope`
    - `token_type`
    - `id_token` (contains user information)

5. **Frontend**:

- Sends the access_token and provider (e.g., "google") to the backend API.

6. **Backend**:

- Uses the access_token to fetch the user's profile data from the Google API.
- Depending on whether it's a login or signup request:
    - If it's a **login**: Authenticates the user, creates a user if they don’t exist, and returns `access_token` and
      `refresh_token`.
    - If it's a **signup**: Creates a new user if they don’t exist and returns the created user's data.

---

**You can test the API on [Swagger Docs](http://localhost:8000/docs/) or by `Django REST Framework`'s UI for each
endpoints.**