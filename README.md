# 📧 Email Automation System

Professional email automation system for course enrollment management with rate limiting and beautiful UI.

![Django](https://img.shields.io/badge/Django-5.2.1-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📤 **Drag & Drop Upload** - Easy Excel file upload
- ⏱️ **Rate Limiting** - 20 emails per hour (Gmail safe)
- ✉️ **HTML Email Templates** - Professional gradient design
- 📊 **Real-time Statistics** - Track sent/pending emails
- 🎨 **Beautiful UI** - Animated gradient background
- 🗑️ **Delete Management** - Remove individual or all records
- 🔔 **Admin Notifications** - Get notified on link clicks
- 📱 **Responsive Design** - Works on all devices

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/email-automation.git
cd email-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Email Settings

Edit `email_project/settings.py`:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Note:** Use Gmail App Password, not regular password. [How to create App Password](https://support.google.com/accounts/answer/185833)

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

### 7. Open Browser

```
http://127.0.0.1:8000/
```

## 📋 Excel File Format

Your Excel file must have these columns:

| Name | Email | Course Name | Link |
|------|-------|-------------|------|
| John Doe | john@example.com | Python Programming | https://example.com/python |
| Jane Smith | jane@example.com | Web Development | https://example.com/web |

## ⏱️ Rate Limiting

- **20 emails per hour** - Safe for Gmail
- **3 minutes delay** between emails
- **Automatic management** - No manual intervention needed
- **Pending tracking** - See how many emails waiting

### How It Works:

1. Upload Excel file → First 20 students get emails
2. Remaining marked as "Pending"
3. Click "Send All Emails" after 1 hour → Next 20 sent
4. Repeat until all sent

## 🎨 UI Features

- **Animated Background** - Moving dot pattern
- **Circular Action Buttons** - Beautiful icons with hover effects
- **Rate Limit Banner** - Pulsing gradient notification
- **Status Badges** - Visual email status (Sent/Pending)
- **Loading Indicators** - Professional UX
- **Success/Error Alerts** - Real-time feedback

## 📧 Email Configuration

### Gmail SMTP Settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Gmail Limits:

- **Free Account:** 500 emails/day
- **Google Workspace:** 2,000 emails/day

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with UI |
| `/api/upload/` | POST | Upload Excel file |
| `/api/students/` | GET | Get all students |
| `/api/send-emails/` | POST | Send pending emails (20/hour) |
| `/api/send-email/<id>/` | POST | Send to specific student |
| `/api/notify-admin/<id>/` | POST | Send admin notification |
| `/api/delete-student/<id>/` | DELETE | Delete student |
| `/api/delete-all/` | DELETE | Delete all students |

## 📱 Admin Panel

Access: `http://127.0.0.1:8000/admin/`

Features:
- View all students
- Edit student data
- Check email status
- Manual management

## 🛠️ Tech Stack

- **Backend:** Django 5.2.1
- **API:** Django REST Framework
- **Database:** SQLite (default)
- **Email:** SMTP (Gmail)
- **Frontend:** HTML, CSS, JavaScript
- **Excel:** pandas, openpyxl

## 📦 Dependencies

```
Django==5.2.1
djangorestframework==3.15.2
pandas==2.2.3
openpyxl==3.1.5
```

## 🔐 Security Notes

- Never commit `settings.py` with real credentials
- Use environment variables for production
- Keep `SECRET_KEY` secure
- Use App Passwords for Gmail

## 🚀 Deployment

### For Production:

1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Use environment variables
4. Set up proper database (PostgreSQL)
5. Configure static files
6. Use professional email service (SendGrid, Mailgun)

## 📝 License

MIT License - Feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

## 🎯 Use Cases

- Course enrollment campaigns
- Newsletter distribution
- Event invitations
- Marketing campaigns
- Student notifications
- Bulk email management

## ⚡ Performance

- Handles 1000+ students efficiently
- Rate limiting prevents Gmail blocks
- Automatic retry on failures
- Real-time status tracking

## 🎉 Credits

Built with ❤️ using Django and modern web technologies.

---

**Happy Emailing! 📧**
