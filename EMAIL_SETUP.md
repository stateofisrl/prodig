# Email Setup Guide

## Gmail Configuration for Email Notifications

This application sends email notifications for:
- Password reset requests
- Deposit approvals/rejections
- Withdrawal status updates

### Step 1: Generate Gmail App Password

1. **Enable 2-Factor Authentication** on your Gmail account:
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification" and follow the setup

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Tesla Investment Platform"
   - Click "Generate"
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 2: Configure Environment Variables

#### For Local Development:

Create a `.env` file in the project root:

```env
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop  # 16-char app password (no spaces)
DEFAULT_FROM_EMAIL=youremail@gmail.com
```

#### For Render Production:

Add these environment variables in Render dashboard:

1. Go to your service → Environment
2. Add these variables:
   ```
   EMAIL_HOST_USER = youremail@gmail.com
   EMAIL_HOST_PASSWORD = abcdefghijklmnop
   DEFAULT_FROM_EMAIL = youremail@gmail.com
   ```

### Step 3: Test Email Functionality

#### Test Password Reset:
1. Go to http://127.0.0.1:8001/forgot-password/
2. Enter a registered user's email
3. Click "Send Reset Link"
4. Check the email inbox for reset link

#### Test Deposit Notification:
1. Login as admin at http://127.0.0.1:8001/admin/
2. Go to Deposits
3. Approve or reject a deposit
4. User will receive an email notification

#### Test Withdrawal Notification:
1. Login as admin
2. Go to Withdrawals
3. Update status to "completed" or "rejected"
4. User will receive an email notification

### Email Limits

**Gmail Free Account:**
- 500 emails per day
- Perfect for small-medium platforms

**Google Workspace:**
- 2,000 emails per day
- Professional `@yourdomain.com` address

### Troubleshooting

**Email not sending:**
1. Verify 2FA is enabled on Gmail
2. Check app password is correct (16 characters, no spaces)
3. Ensure `EMAIL_HOST_USER` and `DEFAULT_FROM_EMAIL` match
4. Check terminal/logs for error messages

**"Less secure app" error:**
- Use App Password (not your regular Gmail password)
- App passwords bypass "less secure app" restrictions

**Password reset link not working:**
- Check that `ALLOWED_HOSTS` includes your domain
- Verify link format in email
- Token expires after 24 hours

### Email Templates

All email templates are in `apps/users/emails.py`:
- `send_password_reset_email()` - Password reset
- `send_deposit_notification()` - Deposit updates
- `send_withdrawal_notification()` - Withdrawal updates

You can customize the HTML templates to match your branding.

### Alternative Email Providers

If you need more than 500 emails/day:

**SendGrid (Recommended):**
- Free tier: 100 emails/day forever
- Paid: From $15/month for 50,000 emails
- Change `EMAIL_HOST` to `smtp.sendgrid.net`

**Mailgun:**
- Free tier: 5,000 emails/month for 3 months
- Paid: $35/month for 50,000 emails
- Change `EMAIL_HOST` to `smtp.mailgun.org`

**AWS SES:**
- $0.10 per 1,000 emails
- Most cost-effective for high volume
- Requires AWS setup

### Production Checklist

Before deploying to production:

- ✅ Gmail 2FA enabled
- ✅ App password generated
- ✅ Environment variables set in Render
- ✅ `DEFAULT_FROM_EMAIL` set to professional address
- ✅ Email templates tested
- ✅ Password reset flow tested
- ✅ Deposit/withdrawal notifications tested

### Security Notes

**Never commit email credentials to Git!**
- Use environment variables only
- `.env` is in `.gitignore`
- Rotate app passwords if exposed

**Email best practices:**
- Use App Passwords, not regular Gmail password
- Rotate app passwords every 90 days
- Monitor daily send limits
- Set up SPF/DKIM for custom domains
