# Security Configuration Guide

This project uses environment variables to store sensitive information such as API keys, passwords, and database credentials. **Never commit sensitive information to version control.**

## Setup Instructions

### 1. Install python-dotenv (Optional but Recommended)

```bash
pip install python-dotenv
```

If you don't install `python-dotenv`, the application will still work by reading directly from system environment variables.

### 2. Create Your .env File

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in all the required values with your actual credentials.

### 3. Required Environment Variables

#### FWD Provider Configuration
- `FWD_CLIENT_ID` - Your FWD API client ID
- `FWD_CLIENT_SECRET` - Your FWD API client secret
- `FWD_PROVISION_KEY` - Your FWD provision key
- `FWD_AUTHENTICATED_USERID` - FWD authenticated user ID (default: svc_amg_prd)
- `FWD_BASE_URL` - FWD API base URL (default: https://apihk.fwd.com.hk)

#### Office 365 / Email Configuration
- `O365_CLIENT_ID` - Office 365 client ID for email access
- `O365_CLIENT_SECRET` - Office 365 client secret
- `SMTP_EMAIL` - SMTP email address for sending emails
- `SMTP_PASSWORD` - SMTP password

#### Database Configuration

**Development (when DEBUG=true):**
- `DB_DEV_DRIVER` - ODBC driver name (default: ODBC Driver 17 for SQL Server)
- `DB_DEV_SERVER` - Development database server
- `DB_DEV_DATABASE` - Development database name
- `DB_DEV_USERNAME` - Development database username
- `DB_DEV_PASSWORD` - Development database password

**Production (when DEBUG=false):**
- `DB_PROD_DRIVER` - ODBC driver name (default: ODBC Driver 18 for SQL Server)
- `DB_PROD_SERVER` - Production database server
- `DB_PROD_DATABASE` - Production database name
- `DB_PROD_USERNAME` - Production database username
- `DB_PROD_PASSWORD` - Production database password

#### Application Settings
- `DEBUG` - Set to `true`, `1`, or `yes` for debug mode, otherwise release mode
- `ACTIVE_PROVIDER` - Active insurance provider (default: FWD)

## Security Best Practices

1. **Never commit `.env` files** - The `.gitignore` file already excludes `.env` files from version control.

2. **Rotate credentials regularly** - If credentials are exposed, rotate them immediately.

3. **Use different credentials for development and production** - Never use production credentials in development.

4. **Limit access to `.env` files** - Only authorized personnel should have access to these files.

5. **Use secrets management in production** - For production deployments, consider using:
   - Azure Key Vault
   - AWS Secrets Manager
   - HashiCorp Vault
   - Or your platform's secrets management service

## Troubleshooting

### Error: "environment variable is required"

If you see an error about missing environment variables:
1. Make sure you've created a `.env` file from `.env.example`
2. Verify all required variables are set in your `.env` file
3. Check that variable names match exactly (case-sensitive)
4. Restart your application after creating/modifying `.env`

### Error: "python-dotenv not installed"

This is not an error - the application will work without `python-dotenv` by reading directly from system environment variables. However, using `.env` files is more convenient for local development.

## Migration from Hardcoded Values

If you're migrating from the old configuration with hardcoded values:

1. Check your old `Config.py` for the values you were using
2. Copy those values to your `.env` file
3. The application will automatically use the environment variables instead

**Important:** After migrating, make sure to remove any hardcoded secrets from your codebase before pushing to version control.

