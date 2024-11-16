# Example Superset configuration

# The SQLAlchemy connection string to your database backend
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset/superset.db'

# Flask App Builder configuration
# Your App secret key must be strong and unique for production.
SECRET_KEY = 'UQCghpiYrdp4T4TXxO3qW+CaZJ9cz+LMlzSzBr+WErBU4N0uj3oeng1B'

# Enable guest user access
AUTH_ROLE_PUBLIC = "Gamma"
PUBLIC_ROLE_LIKE = "Gamma"

# Allow guest user to access API
GUEST_TOKEN_JWT_SECRET = "UQCghpiYrdp4T4TXxO3qW+CaZJ9cz+LMlzSzBr+WErBU4N0uj3oeng1B"
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_JWT_EXP_SECONDS = 86400
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"

# Grant additional roles to the admin user
ADMIN_ROLES = ["Admin", "Alpha", "Gamma", "sql_lab"]

# Enable secure proxy headers when running behind a reverse proxy (e.g., Nginx).
ENABLE_PROXY_FIX = True

# Address and port for the Superset web server.
SUPERSET_WEBSERVER_ADDRESS = "0.0.0.0"
SUPERSET_WEBSERVER_PORT = 8088

# Flask-WTF configuration for CSRF protection.
WTF_CSRF_ENABLED = False
WTF_CSRF_EXEMPT_LIST = []
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365  # Token expiry time (1 year).

# Limit the number of rows displayed in SQL Lab.
ROW_LIMIT = 5000

# Mapbox API key for map visualizations. Leave empty if unused.
MAPBOX_API_KEY = ''

# Logging configuration (optional, for debugging).
DEBUG = False

# Other potential security-related settings for production.
SESSION_COOKIE_SECURE = True  # Use HTTPS for cookies.
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing cookies.
SESSION_COOKIE_SAMESITE = "Lax"  # Restrict cross-site cookie sharing.
