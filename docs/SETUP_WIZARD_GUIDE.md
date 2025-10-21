# Using the Setup Wizard - Quick Guide

## First-Time Setup

When you start the application for the first time (or when credentials are not configured), the **First Time Setup** wizard will appear automatically.

### Step-by-Step Instructions

#### 1. Fill in API Credentials

**API Key:**
- Enter your LCSC API Key in the first field
- This is provided by LCSC when you apply for API access

**API Secret:**
- Enter your LCSC API Secret in the second field
- By default, the secret is hidden (shows as ***)
- Check "Show API Secret" if you want to see what you're typing

**API Base URL:**
- Default value: `https://api.lcsc.com/v1`
- Usually you don't need to change this
- Only modify if LCSC provides a different endpoint

#### 2. Configure Network Settings (Optional)

**Your IP Address:**
- Enter your public IP address (needed for LCSC IP whitelisting)
- Click **"Detect My IP"** button to automatically fill this field
- The system will fetch your public IP from https://api.ipify.org

**Request Timeout:**
- Default: 30 seconds
- How long to wait for API responses
- Increase if you have a slow connection

#### 3. Configure Application Settings (Optional)

**Match Threshold:**
- Default: 70%
- Controls how strict the fuzzy matching is
- Higher = more strict matching
- Lower = more lenient matching

#### 4. Test Your Credentials (Recommended)

**Before saving**, click the **"Test Connection"** button to verify:
- ✅ Your API Key and Secret are correct
- ✅ The API URL is reachable
- ✅ Your IP is whitelisted (if required)
- ✅ Network connectivity is working

**If successful:** You'll see "Successfully connected to LCSC API!" message
**If failed:** You'll see an error message explaining what went wrong

#### 5. Save and Continue

Once you're satisfied with your settings:
1. Click **"Save & Continue"** button
2. Your settings will be saved to the `.env` file
3. The wizard will close
4. The main application window will open

### What Happens When You Save

When you click "Save & Continue":
1. All fields are validated (API Key, Secret, and URL are required)
2. Settings are written to `C:\Projects\LCSC_API\.env`
3. The file is formatted with sections and comments
4. Configuration is reloaded
5. The wizard closes
6. Main application initializes with your credentials

## Common Scenarios

### Scenario 1: Don't Have API Credentials Yet

If you don't have LCSC API credentials yet:
1. Visit: https://www.lcsc.com/agent
2. Apply for API access
3. Wait for approval (may take time)
4. You'll receive your API Key and Secret
5. Come back and enter them in the wizard

**Note:** You cannot skip the first-run setup. The application requires credentials to function.

### Scenario 2: Want to Test Before Committing

1. Fill in your API Key and Secret
2. Click **"Test Connection"** button
3. Wait for the result (usually takes 1-5 seconds)
4. If successful, proceed to save
5. If failed, check your credentials and try again

### Scenario 3: Not Sure About IP Address

1. Click **"Detect My IP"** button
2. The system will fetch your public IP automatically
3. A popup will show your detected IP address
4. The field will be filled automatically
5. Make sure to whitelist this IP in LCSC portal

### Scenario 4: Want to Change Settings Later

After initial setup, you can always change settings:
1. Open the application
2. Go to menu: **Tools > Settings**
3. The same dialog appears (not first-run mode)
4. Modify any values
5. Test connection if needed
6. Click **"Save"**

## Validation Rules

The wizard validates your input:

**Required Fields:**
- ✅ API Key cannot be empty
- ✅ API Secret cannot be empty
- ✅ API Base URL cannot be empty
- ✅ API Base URL must start with http:// or https://

**Optional Fields:**
- IP Address (recommended for whitelisting)
- Request Timeout (has sensible default)
- Match Threshold (has sensible default)

If validation fails, you'll see a warning message and the field will be focused.

## Troubleshooting

### "Test Connection" Button Does Nothing
- Make sure you filled in API Key and Secret
- Check that the URL is valid
- Look for error messages in the console

### "Connection Failed" Error
Possible reasons:
- ❌ Wrong API credentials
- ❌ IP not whitelisted in LCSC portal
- ❌ Network connectivity issues
- ❌ LCSC API is down
- ❌ Wrong API URL

**Solutions:**
1. Double-check your API Key and Secret (copy-paste carefully)
2. Verify your IP is whitelisted in LCSC portal
3. Check your internet connection
4. Try clicking "Detect My IP" and whitelist the detected IP

### Cannot See What I'm Typing in Secret Field
- Check the **"Show API Secret"** checkbox
- The field will show the actual characters
- Uncheck when done for security

### Made a Mistake After Saving
No problem! 
1. Close the wizard (or let it proceed)
2. Go to **Tools > Settings** in the main window
3. Correct your values
4. Save again

## File Location

Your settings are saved to:
```
C:\Projects\LCSC_API\.env
```

You can also edit this file directly with a text editor if needed, but using the GUI is recommended.

## Next Steps After Setup

Once setup is complete:
1. Main application window opens
2. API client is initialized with your credentials
3. You can start using the application
4. Load your BOM Excel file
5. Match components with LCSC parts
6. Export enhanced BOM

---

**Need Help?**
- Check `docs/USER_GUIDE.md` for full documentation
- Check `docs/API_DOCUMENTATION.md` for LCSC API details
- Review the log file: `lhatolcsc.log` for errors
