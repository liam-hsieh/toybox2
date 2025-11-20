# Environment Variables with .env Files

Learn how to securely manage sensitive configuration using `.env` files and `python-dotenv`.

## Overview

Environment variables are a secure way to store sensitive information like API keys, database credentials, and passwords without hardcoding them in your source code.

**Benefits:**
- Keep secrets out of version control
- Different configurations per environment (dev/prod)
- Easy to change without code modifications
- Industry-standard security practice

## Installation

The `python-dotenv` package is included in the project dependencies:

```bash
uv sync --all-extras
```

## Quick Start

### 1. Create a .env File

Create a `.env` file in your project root:

```bash
# .env - Store sensitive configuration here
DEMO_API_KEY=sk_test_1234567890abcdef
DEMO_DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Email Configuration (used by send_mail.py)
SENDER=noreply@example.com
PSW=your_email_password
USER=smtp_username
SERVER=smtp.example.com
PORT=587
```

!!! warning "Security Notice"
    **Never commit `.env` files to version control!** Add `.env` to your `.gitignore` file.

### 2. Load Environment Variables in Your Code

```python
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access variables using os.getenv()
api_key = os.getenv("DEMO_API_KEY")
db_url = os.getenv("DEMO_DATABASE_URL")

# With default fallback value
port = os.getenv("PORT", 587)
```

### 3. Use in Streamlit Applications

Here's a complete example from `apps/demo_app/demo_app1.py`:

```python
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

st.title("Environment Variables Demo")

# Check for environment variables
api_key = os.getenv("DEMO_API_KEY")
database_url = os.getenv("DEMO_DATABASE_URL")

if api_key:
    st.success(f"✓ API Key loaded: {api_key[:10]}...")
else:
    st.warning("✗ DEMO_API_KEY not found in .env")

if database_url:
    st.success(f"✓ Database URL loaded: {database_url[:20]}...")
else:
    st.warning("✗ DEMO_DATABASE_URL not found in .env")
```

## Live Demo

Run the demo app to see environment variables in action:

```bash
uv run streamlit run apps/demo_app/demo_app1.py
```

### Expected Results

**With .env file containing variables:**

<div class="result" markdown>

```
Environment Variables Demo

DEMO_API_KEY
✓ Found: sk_test_12...

DEMO_DATABASE_URL  
✓ Found: postgresql://user:p...

💡 Tip: Create a .env file in the project root with these variables to see them loaded.
```

</div>

**Without .env file or missing variables:**

<div class="result" markdown>

```
Environment Variables Demo

DEMO_API_KEY
✗ Not found in .env file

DEMO_DATABASE_URL
✗ Not found in .env file

💡 Tip: Create a .env file in the project root with these variables to see them loaded.
```

</div>

## Real-World Usage

### Email Configuration (send_mail.py)

The `apps/shared/send_mail.py` module uses environment variables for email credentials:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SENDER = os.getenv("SENDER", 'DoNotReply <sys@example.com>')
PSW = os.getenv("PSW", None)
USER = os.getenv("USER", None)
SERVER = os.getenv("SERVER", 'smtp.example.com')
PORT = os.getenv("PORT", 587)
```

**Required .env configuration:**

```bash
# Email configuration for send_mail.py
SENDER=noreply@yourcompany.com
PSW=your_smtp_password
USER=smtp_username
SERVER=smtp.yourcompany.com
PORT=587
```

## Best Practices

### 1. Use .env.example Template

Create a `.env.example` file with dummy values to document required variables:

```bash
# .env.example - Commit this to version control
DEMO_API_KEY=your_api_key_here
DEMO_DATABASE_URL=your_database_url_here
SENDER=your_email@example.com
PSW=your_password_here
```

### 2. Add .env to .gitignore

Protect your secrets:

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

### 3. Provide Default Fallbacks

Always provide sensible defaults or handle missing variables:

```python
# Good - with fallback
port = int(os.getenv("PORT", 8501))

# Better - with validation
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is required")
```

### 4. Type Conversion

Environment variables are always strings. Convert as needed:

```python
# String
API_KEY = os.getenv("API_KEY")

# Integer
PORT = int(os.getenv("PORT", "8501"))

# Boolean
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# List
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
```

## Different Environments

### Development

```bash
# .env.development
DEBUG=true
DATABASE_URL=postgresql://localhost/dev_db
API_ENDPOINT=http://localhost:8000
```

### Production

```bash
# .env.production
DEBUG=false
DATABASE_URL=postgresql://prod-server/prod_db
API_ENDPOINT=https://api.example.com
```

Load specific environment:

```python
from dotenv import load_dotenv

# Load specific env file
load_dotenv('.env.production')
```

## Troubleshooting

### Variables Not Loading

**Problem:** `os.getenv()` returns `None`

**Solutions:**

1. **Check .env location** - Must be in project root
   ```bash
   ls -la .env  # Verify file exists
   ```

2. **Check .env format** - No quotes needed for values
   ```bash
   # Correct
   API_KEY=abc123
   
   # Incorrect (includes quotes in value)
   API_KEY="abc123"
   ```

3. **Verify load_dotenv() is called** - Must be called before accessing variables
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Call this first!
   
   api_key = os.getenv("API_KEY")
   ```

4. **Check for typos** - Variable names are case-sensitive
   ```python
   # .env has: DEMO_API_KEY=...
   
   # Wrong
   key = os.getenv("demo_api_key")  # None
   
   # Correct
   key = os.getenv("DEMO_API_KEY")  # Works
   ```

### Path Issues

If running from a subdirectory:

```python
from pathlib import Path
from dotenv import load_dotenv

# Find .env in project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
```

## Testing Demo App

1. **Create .env file:**
   ```bash
   cd /opt/projects/toybox2
   cat > .env << 'EOF'
   DEMO_API_KEY=sk_test_1234567890abcdef
   DEMO_DATABASE_URL=postgresql://user:password@localhost:5432/mydb
   EOF
   ```

2. **Run demo app:**
   ```bash
   uv run streamlit run apps/demo_app/demo_app1.py
   ```

3. **Expected result:**
   - Both variables show ✓ green checkmarks
   - Values are displayed (truncated for security)
   - Log messages confirm successful loading

4. **Test missing variable:**
   - Remove one variable from `.env`
   - Refresh the app
   - Should show ✗ warning for missing variable

## Related Documentation

- **[Sub-App Development Guide](../SUB_APP_DEVELOPMENT_GUIDE.md)** - Building applications
- **[Quick Start Guide](../getting-started/quick-start.md)** - Initial setup
- **[API Documentation](api-documentation.md)** - Code documentation patterns

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` template is documented
- [ ] No secrets committed to version control
- [ ] Production `.env` uses strong credentials
- [ ] Fallback values are safe defaults
- [ ] Team members have `.env` setup instructions
- [ ] CI/CD uses environment-specific secrets

!!! success "Best Practice"
    Store production secrets in your deployment platform's secret management system (GitHub Secrets, AWS Secrets Manager, etc.) rather than `.env` files.
