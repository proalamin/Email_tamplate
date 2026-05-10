# 📧 Email Account Management - বাংলা গাইড

## ✨ নতুন ফিচার

এখন আপনি homepage থেকে সরাসরি আপনার email account add/manage করতে পারবেন!

---

## 🚀 কিভাবে ব্যবহার করবেন

### ধাপ ১: Email Accounts বাটনে ক্লিক করুন

1. Homepage এ যান: http://127.0.0.1:8000/
2. **"📧 Email Accounts"** বাটনে ক্লিক করুন
3. Email Account Management section খুলে যাবে

### ধাপ ২: নতুন Email Account যোগ করুন

**প্রয়োজনীয় তথ্য:**
- **Email Address**: আপনার Gmail address (যেমন: yourname@gmail.com)
- **App Password**: Gmail এর App Password (16 digit)
- **Daily Limit**: প্রতিদিন কতটি email পাঠাবেন (সুপারিশ: 450)

**App Password কিভাবে পাবেন:**
1. যান: https://myaccount.google.com/apppasswords
2. আপনার Google account এ login করুন
3. "Select app" থেকে "Mail" select করুন
4. "Select device" থেকে "Other" select করুন
5. একটি name দিন (যেমন: "Email Template System")
6. "Generate" button এ ক্লিক করুন
7. 16 digit password copy করুন
8. এই password টি "App Password" field এ paste করুন

### ধাপ ৩: Account Add করুন

1. সব তথ্য fill up করুন
2. **"➕ Add Account"** button এ ক্লিক করুন
3. Success message দেখাবে
4. আপনার account list এ দেখা যাবে

---

## 📊 Account Statistics দেখুন

প্রতিটি account এর জন্য দেখতে পারবেন:
- **Sent Today**: আজ কতটি email পাঠানো হয়েছে
- **Daily Limit**: সর্বোচ্চ কতটি পাঠাতে পারবেন
- **Remaining**: আর কতটি পাঠাতে পারবেন
- **Usage Percentage**: কত % ব্যবহার হয়েছে
- **Progress Bar**: Visual representation

**রঙের অর্থ:**
- 🟢 **সবুজ** (0-50%): নিরাপদ, আরও email পাঠাতে পারবেন
- 🟠 **কমলা** (50-80%): সতর্ক থাকুন, limit এর কাছাকাছি
- 🔴 **লাল** (80-100%): প্রায় শেষ, নতুন account add করুন

---

## 🔄 কিভাবে কাজ করে

### Automatic Rotation System:

1. **Email পাঠানোর সময়:**
   - System automatically সবচেয়ে কম ব্যবহৃত account select করে
   - সেই account দিয়ে email পাঠায়
   - Counter বাড়ায় (sent_today++)

2. **Limit পৌঁছালে:**
   - যখন একটি account এর limit শেষ (450/450)
   - System automatically পরবর্তী available account use করে
   - কোন manual intervention লাগে না!

3. **Daily Reset:**
   - প্রতিদিন midnight এ counter automatically reset হয়
   - আবার 0 থেকে শুরু হয়
   - নতুন দিন, নতুন limit!

---

## 💡 উদাহরণ

### Scenario 1: একটি Account দিয়ে

```
Account 1: yourmail@gmail.com
- Daily Limit: 450
- Sent Today: 0
- Remaining: 450

✅ আজ 450টি email পাঠাতে পারবেন
```

### Scenario 2: তিনটি Account দিয়ে

```
Account 1: mail1@gmail.com
- Sent: 450/450 (100%) 🔴 FULL

Account 2: mail2@gmail.com  
- Sent: 320/450 (71%) 🟠 ACTIVE

Account 3: mail3@gmail.com
- Sent: 0/450 (0%) 🟢 READY

Total Capacity: 1,350 emails/day
Total Sent Today: 770
Total Remaining: 580

✅ আজ আরও 580টি email পাঠাতে পারবেন
```

---

## 🗑️ Account Delete করা

1. যে account delete করতে চান তার **"🗑️ Delete"** button এ ক্লিক করুন
2. Confirmation dialog আসবে
3. "OK" ক্লিক করলে delete হবে

**⚠️ সতর্কতা:** Delete করলে সেই account এর সব data মুছে যাবে!

---

## 📈 Capacity Planning

### কতগুলো Account লাগবে?

| প্রতিদিন Email | প্রয়োজনীয় Accounts | Total Capacity |
|----------------|---------------------|----------------|
| 500            | 2                   | 900/day        |
| 1,000          | 3                   | 1,350/day      |
| 2,000          | 5                   | 2,250/day      |
| 5,000          | 12                  | 5,400/day      |

**সূত্র:** `প্রয়োজনীয় Accounts = (Total Emails ÷ 450) + 1`

---

## ⚙️ Best Practices

### ✅ করণীয়:

1. **Multiple Accounts ব্যবহার করুন**
   - কমপক্ষে 2-3টি account রাখুন
   - একটি full হলে অন্যটি use হবে

2. **Daily Limit 450 রাখুন**
   - Gmail এর limit 500, কিন্তু 450 নিরাপদ
   - Spam filter এড়াতে সাহায্য করে

3. **নিয়মিত Check করুন**
   - Email Accounts section এ গিয়ে usage দেখুন
   - 80% এর বেশি হলে নতুন account add করুন

4. **App Password ব্যবহার করুন**
   - কখনও actual Gmail password ব্যবহার করবেন না
   - শুধুমাত্র App Password ব্যবহার করুন

### ❌ করণীয় নয়:

1. **একটি Account এ নির্ভর করবেন না**
   - Limit শেষ হলে email পাঠানো বন্ধ হবে

2. **500+ Daily Limit দেবেন না**
   - Gmail block করতে পারে
   - Account suspend হতে পারে

3. **Password Share করবেন না**
   - Security risk
   - Account compromise হতে পারে

---

## 🔧 Troubleshooting

### সমস্যা: "All email accounts have reached their daily limit"

**সমাধান:**
1. Email Accounts section এ যান
2. সব account এর usage check করুন
3. নতুন account add করুন
4. অথবা পরের দিন পর্যন্ত অপেক্ষা করুন (midnight এ reset হবে)

### সমস্যা: Email পাঠানো হচ্ছে না

**সমাধান:**
1. Check করুন কোন active account আছে কিনা
2. App Password সঠিক আছে কিনা verify করুন
3. Gmail account এ 2FA enable আছে কিনা check করুন
4. Account suspend হয়নি তো check করুন

### সমস্যা: Account add হচ্ছে না

**সমাধান:**
1. Email এবং Password field খালি আছে কিনা check করুন
2. Valid email format ব্যবহার করুন
3. App Password এ space থাকলে remove করুন
4. Browser console এ error check করুন

---

## 🎯 Quick Tips

1. **সকালে Check করুন**: প্রতিদিন সকালে একবার usage check করুন
2. **Backup Account রাখুন**: সবসময় 1-2টি extra account ready রাখুন
3. **Monitor করুন**: বড় campaign এর আগে capacity check করুন
4. **Test করুন**: নতুন account add করার পর test email পাঠান

---

## 📞 সাহায্য প্রয়োজন?

যদি কোন সমস্যা হয়:
1. Email Accounts section এ গিয়ে statistics check করুন
2. Browser console এ error message দেখুন
3. Django server logs check করুন
4. Documentation পড়ুন: `EMAIL_ROTATION_GUIDE.md`

---

## ✅ সফলতার চেকলিস্ট

- [ ] Gmail account তৈরি করেছি
- [ ] 2FA enable করেছি
- [ ] App Password generate করেছি
- [ ] Email Accounts section এ account add করেছি
- [ ] Account list এ দেখতে পাচ্ছি
- [ ] Test email পাঠিয়ে verify করেছি
- [ ] Statistics দেখতে পাচ্ছি
- [ ] Multiple accounts add করেছি (recommended)

---

**🎉 এখন আপনি ready! Email পাঠানো শুরু করুন!**

**Homepage:** http://127.0.0.1:8000/
**Email Accounts:** Click করুন "📧 Email Accounts" button
