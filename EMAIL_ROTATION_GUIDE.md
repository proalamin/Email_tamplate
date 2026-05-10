# Email Account Rotation System

## Problem
Gmail has strict sending limits:
- **Free Gmail**: ~100-500 emails per day
- **Google Workspace**: ~2,000 emails per day

## Solution
This system automatically rotates between multiple Gmail accounts to bypass daily limits.

---

## 🚀 How It Works

1. **Multiple Accounts**: Configure multiple Gmail accounts in `settings.py`
2. **Automatic Rotation**: System automatically switches to the next account when one reaches its limit
3. **Daily Reset**: Counters reset automatically every 24 hours
4. **Rate Limiting**: Built-in delays between emails to avoid triggering spam filters

---

## ⚙️ Configuration

### Step 1: Add Multiple Gmail Accounts

Edit `email_project/settings.py` and add your accounts:

```python
EMAIL_ACCOUNTS = [
    {
        'email': 'your-first-email@gmail.com',
        'password': 'your-app-password-1',
        'daily_limit': 450,  # Safe limit (Gmail allows ~500/day)
        'sent_today': 0,
    },
    {
        'email': 'your-second-email@gmail.com',
        'password': 'your-app-password-2',
        'daily_limit': 450,
        'sent_today': 0,
    },
    {
        'email': 'your-third-email@gmail.com',
        'password': 'your-app-password-3',
        'daily_limit': 450,
        'sent_today': 0,
    },
]
```

### Step 2: Get Gmail App Passwords

For each Gmail account:

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google account
3. Create a new app password
4. Copy the 16-character password
5. Add it to `EMAIL_ACCOUNTS` in settings.py

### Step 3: Adjust Sending Delay (Optional)

```python
EMAIL_SEND_DELAY = 1  # Seconds between emails (default: 1)
```

- **Lower delay** = Faster sending (but higher risk of being flagged)
- **Higher delay** = Slower sending (but safer)

---

## 📊 Monitoring Email Usage

### Check Email Statistics

**Endpoint**: `GET /api/email-stats/`

**Response Example**:
```json
{
  "accounts": [
    {
      "email": "account1@gmail.com",
      "sent_today": 245,
      "daily_limit": 450,
      "remaining": 205,
      "percentage_used": 54.44
    },
    {
      "email": "account2@gmail.com",
      "sent_today": 0,
      "daily_limit": 450,
      "remaining": 450,
      "percentage_used": 0
    }
  ],
  "total_sent_today": 245,
  "total_remaining": 655,
  "total_capacity": 900
}
```

---

## 💡 Capacity Planning

### Example Scenarios:

| Accounts | Daily Limit Each | Total Capacity |
|----------|------------------|----------------|
| 1        | 450              | 450/day        |
| 2        | 450              | 900/day        |
| 3        | 450              | 1,350/day      |
| 5        | 450              | 2,250/day      |
| 10       | 450              | 4,500/day      |

**Recommendation**: 
- For 1,000 emails/day → Use 3 accounts
- For 2,000 emails/day → Use 5 accounts
- For 5,000 emails/day → Use 12 accounts

---

## 🔄 How Rotation Works

1. System checks which account has available quota
2. Sends email using that account
3. Increments counter for that account
4. When account reaches limit, automatically switches to next account
5. If all accounts reach limit, returns error message
6. Counters reset automatically at midnight

---

## ⚠️ Important Notes

### Gmail Best Practices:
1. **Don't exceed 500 emails/day per account** (we use 450 as safe limit)
2. **Add 1-2 second delay** between emails to avoid spam filters
3. **Warm up new accounts** - Start with 50 emails/day, gradually increase
4. **Use professional content** - Avoid spam trigger words
5. **Enable 2FA** on all Gmail accounts for security

### Avoiding Spam Filters:
- ✅ Use real "From" names
- ✅ Include unsubscribe links
- ✅ Personalize emails with recipient names
- ✅ Avoid ALL CAPS and excessive punctuation!!!
- ✅ Test emails before bulk sending

---

## 🛠️ Troubleshooting

### Problem: "All email accounts have reached their daily limit"

**Solution**: 
- Add more Gmail accounts to `EMAIL_ACCOUNTS`
- Wait until midnight for counters to reset
- Check `/api/email-stats/` to see current usage

### Problem: Emails going to spam

**Solution**:
- Increase `EMAIL_SEND_DELAY` to 2-3 seconds
- Reduce daily limit to 300-400 per account
- Improve email content (avoid spam words)
- Add SPF/DKIM records (for custom domains)

### Problem: "Authentication failed"

**Solution**:
- Verify app passwords are correct
- Enable "Less secure app access" (if using old Gmail)
- Use App Passwords (recommended)
- Check if 2FA is enabled

---

## 🚀 Alternative Solutions

### For Higher Volume (1000+ emails/day):

1. **SendGrid** (Free: 100/day, Paid: 40,000+/month)
   ```python
   EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
   SENDGRID_API_KEY = 'your-api-key'
   ```

2. **Mailgun** (Free: 5,000/month, Paid: unlimited)
   ```python
   EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
   MAILGUN_API_KEY = 'your-api-key'
   ```

3. **Amazon SES** (Very cheap: $0.10 per 1,000 emails)
   ```python
   EMAIL_BACKEND = 'django_ses.SESBackend'
   AWS_SES_REGION_NAME = 'us-east-1'
   ```

4. **Brevo (Sendinblue)** (Free: 300/day, Paid: unlimited)
   ```python
   EMAIL_BACKEND = 'anymail.backends.sendinblue.EmailBackend'
   SENDINBLUE_API_KEY = 'your-api-key'
   ```

---

## 📝 Testing

### Test with a single email:
```bash
curl -X POST http://127.0.0.1:8000/api/send-template/ \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Email",
    "message": "Hello {name}, this is a test for {course_name}. {link}"
  }'
```

### Check statistics:
```bash
curl http://127.0.0.1:8000/api/email-stats/
```

---

## 📞 Support

If you need help:
1. Check `/api/email-stats/` for current usage
2. Review Django logs for error messages
3. Test with a single email first
4. Verify Gmail app passwords are correct

---

## ✅ Quick Setup Checklist

- [ ] Create multiple Gmail accounts
- [ ] Enable 2FA on each account
- [ ] Generate app passwords for each account
- [ ] Add accounts to `EMAIL_ACCOUNTS` in settings.py
- [ ] Set appropriate `daily_limit` (recommended: 450)
- [ ] Set `EMAIL_SEND_DELAY` (recommended: 1-2 seconds)
- [ ] Test with `/api/email-stats/` endpoint
- [ ] Send test email to verify rotation works
- [ ] Monitor usage during bulk sending

---

**Current Configuration**: 1 account with 450 emails/day capacity
**To increase capacity**: Add more accounts to `EMAIL_ACCOUNTS` in settings.py
