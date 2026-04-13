# 📧 Email Automation System

Professional email automation system with **background processing** for course enrollment management.

![Django](https://img.shields.io/badge/Django-5.2.1-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## ✨ Key Features

### 🚀 Background Email Processing (NEW!)
- **Instant Upload** - File upload completes in 5 seconds
- **Automatic Sending** - Background system sends emails continuously
- **Zero Wait Time** - No need to wait during upload
- **Smart Queue** - Processes 20 emails per hour automatically
- **Auto-Restart** - Checks for pending emails every 5 minutes

### 📧 Email Management
- Professional HTML email templates
- Gmail SMTP with TLS encryption
- Rate limiting (20 emails/hour - Gmail safe)
- Plain text fallback for compatibility
- Personalized content with student details

### 📊 Data Management
- Excel file upload with drag & drop
- Flexible column detection (case-insensitive)
- Real-time statistics dashboard
- Delete individual or all records
- Mobile number storage for future use

### 🎨 Beautiful UI
- Animated gradient background
- Circular action buttons with hover effects
- Real-time status tracking
- Responsive design for all devices
- Success/error notifications

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email
Edit `email_project/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Get App Password:** https://myaccount.google.com/apppasswords

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Open Browser
```
http://127.0.0.1:8000/
```

---

## 📋 Excel File Format

| Name | Email | Mobile | Course Name | Link |
|------|-------|--------|-------------|------|
| John Doe | john@example.com | 01712345678 | Python | https://... |
| Jane Smith | jane@example.com | 01812345678 | Web Dev | https://... |

**Required Columns:** Name, Email, Course Name, Link  
**Optional Column:** Mobile

**Note:** Column names are flexible (case-insensitive)

---

## 🤖 How Background System Works

### Upload Process
```
1. Upload Excel file → Done in 5 seconds ✅
2. All students saved to database
3. Response returned immediately
```

### Background Process (Automatic)
```
Server running → Background thread active
   ↓
Every 5 minutes: Check for pending emails
   ↓
If pending found:
   - Send 20 emails
   - 3 minute delay between each
   - Mark as sent
   - Repeat
```

### Timeline Example
```
10:00 → Upload 100 students (5 sec)
10:00 → Email 1 sent (background)
10:03 → Email 2 sent (background)
10:06 → Email 3 sent (background)
...
10:57 → Email 20 sent (background)
11:00 → Email 21 sent (background)
...continues automatically...
```

**Result:** 100 emails sent in 5 hours, fully automatic!

---

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main UI page |
| `/api/upload/` | POST | Upload Excel (instant) |
| `/api/students/` | GET | Get all students |
| `/api/send-emails/` | POST | Manual send (optional) |
| `/api/send-email/<id>/` | POST | Send to specific student |
| `/api/notify-admin/<id>/` | POST | Admin notification |
| `/api/delete-student/<id>/` | DELETE | Delete student |
| `/api/delete-all/` | DELETE | Delete all students |

---

## 📊 Performance

- **Upload Speed:** 100 rows in < 5 seconds
- **Email Rate:** 20 per hour (automatic)
- **Database:** Handles 1000+ students
- **Response Time:** < 1 second for queries

---

## 🔐 Security

- TLS encryption for emails
- App Password authentication
- Input validation
- Error handling
- .gitignore configured

---

## 🛠️ Tech Stack

- **Backend:** Django 5.2.1, Django REST Framework
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Email:** Gmail SMTP
- **Background:** Python Threading
- **Frontend:** HTML5, CSS3, JavaScript
- **Data:** pandas, openpyxl

---

## 📝 Usage

### 1. Upload Excel File
- Drag & drop or click to select
- File validates automatically
- Upload completes instantly

### 2. Monitor Progress
- Check statistics dashboard
- View pending count
- Track sent emails

### 3. Manage Data
- View all students in table
- Delete individual records
- Clear all data

### 4. Background System
- Runs automatically
- No manual intervention needed
- Sends 20 emails/hour

---

## ⚡ Rate Limiting

### Why 20 Emails Per Hour?
- **Gmail Limit:** 500 emails/day for free accounts
- **Safety:** Prevents account suspension
- **Natural Pattern:** Looks like human sending
- **Reliable:** Avoids spam filters

### Timeline
- **20 emails:** 1 hour
- **100 emails:** 5 hours
- **500 emails:** 25 hours (1 day)

---

## 🎨 UI Features

- Animated dot pattern background
- Circular action buttons
- Status badges (Sent/Pending)
- Real-time statistics
- Loading indicators
- Success/error alerts
- Mobile responsive

---

## 📚 Documentation

- **README.md** - This file
- **TECHNICAL_DOCUMENTATION.md** - Complete technical details
- **LICENSE** - MIT License

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables
- [ ] Setup PostgreSQL
- [ ] Configure static files
- [ ] Use Gunicorn + Nginx
- [ ] Setup SSL certificate

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📧 Support

**Repository:** https://github.com/Raihanroo/Email_tamplate  
**Developer:** Raihan  
**Email:** raihanroo21@gmail.com

For issues or questions, open an issue on GitHub.

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 🎯 Use Cases

- Course enrollment campaigns
- Event invitations
- Newsletter distribution
- Marketing campaigns
- Student notifications
- Bulk email management

---

## ⭐ Features Highlight

✅ Background email processing  
✅ Instant file upload  
✅ Automatic rate limiting  
✅ Professional HTML emails  
✅ Real-time tracking  
✅ Beautiful UI  
✅ Mobile responsive  
✅ Error handling  
✅ Flexible column detection  
✅ Production ready  

---

**Happy Emailing! 📧**

*Built with ❤️ using Django and modern web technologies*
