# Migration Guide: Moving from Hardcoded Secrets to Environment Variables

## What Changed

This project has been refactored to use environment variables instead of hardcoded secrets. This prevents sensitive information from being committed to version control.

## Files Modified

### 1. `Config.py`
- **Before**: Hardcoded API credentials (client_id, client_secret, provision_key)
- **After**: Loads credentials from environment variables
- **Environment Variables Required**:
  - `FWD_CLIENT_ID`
  - `FWD_CLIENT_SECRET`
  - `FWD_PROVISION_KEY`
  - `FWD_AUTHENTICATED_USERID` (optional, defaults to 'svc_amg_prd')
  - `FWD_BASE_URL` (optional, defaults to 'https://apihk.fwd.com.hk')
  - `DEBUG` (optional, for debug mode)
  - `ACTIVE_PROVIDER` (optional, defaults to 'FWD')

### 2. `data/Email.py`
- **Before**: Hardcoded Office 365 credentials and SMTP password
- **After**: Loads credentials from environment variables
- **Environment Variables Required**:
  - `O365_CLIENT_ID`
  - `O365_CLIENT_SECRET`
  - `SMTP_EMAIL`
  - `SMTP_PASSWORD`

### 3. `data/Db.py`
- **Before**: Hardcoded database credentials for dev and production
- **After**: Loads credentials from environment variables
- **Environment Variables Required**:
  - **Development** (when DEBUG=true):
    - `DB_DEV_DRIVER` (optional, defaults to 'ODBC Driver 17 for SQL Server')
    - `DB_DEV_SERVER`
    - `DB_DEV_DATABASE`
    - `DB_DEV_USERNAME`
    - `DB_DEV_PASSWORD`
  - **Production** (when DEBUG=false):
    - `DB_PROD_DRIVER` (optional, defaults to 'ODBC Driver 18 for SQL Server')
    - `DB_PROD_SERVER`
    - `DB_PROD_DATABASE`
    - `DB_PROD_USERNAME`
    - `DB_PROD_PASSWORD`

### 4. `.gitignore`
- **Added**: Rules to exclude `.env` files and other sensitive files from version control
- **Note**: `.env.example` is explicitly allowed (it's a template file)

### 5. New Files Created
- `.env.example` - Template file showing all required environment variables
- `README_SECURITY.md` - Security configuration guide
- `requirements.txt` - Python dependencies (includes optional python-dotenv)

## Immediate Action Required

### Step 1: Create Your .env File

1. Copy the template file:
   ```bash
   # On Windows PowerShell:
   Copy-Item .env.example .env
   
   # On Linux/Mac:
   cp .env.example .env
   ```

2. Edit `.env` and fill in your actual credentials from the old hardcoded values:
   - Get values from your old `Config.py` (if you have a backup)
   - Get values from your old `data/Email.py` 
   - Get values from your old `data/Db.py`

### Step 2: Install python-dotenv (Optional but Recommended)

```bash
pip install python-dotenv
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

**Note**: The application will work without `python-dotenv` by reading directly from system environment variables, but using `.env` files is more convenient.

### Step 3: Test Your Application

Run your application to verify everything works:
```bash
python Main.py
```

If you see errors about missing environment variables, double-check your `.env` file.

## Important Security Notes

1. **Never commit `.env` to version control** - It's already excluded in `.gitignore`
2. **Rotate your credentials** - Since they were previously in version control, consider rotating:
   - FWD API credentials
   - Office 365 credentials
   - SMTP password
   - Database passwords
3. **Remove old secrets from git history** (if already pushed):
   - Consider using `git filter-branch` or BFG Repo-Cleaner
   - Or create new credentials and update your `.env` file

## Backward Compatibility

The code maintains backward compatibility through the backward compatibility section in `Config.py`. However, you **must** set environment variables for the application to work, as the hardcoded values have been removed.

## Getting Help

If you encounter issues:
1. Check `README_SECURITY.md` for detailed documentation
2. Verify all environment variables are set correctly
3. Check that `.env` file exists and is in the project root
4. Ensure variable names match exactly (case-sensitive)

## Next Steps After Migration

1. ✅ Create `.env` file with your credentials
2. ✅ Test the application
3. ✅ Rotate credentials that were previously exposed
4. ✅ Update your deployment process to use environment variables
5. ✅ Consider using a secrets management service for production (Azure Key Vault, AWS Secrets Manager, etc.)

