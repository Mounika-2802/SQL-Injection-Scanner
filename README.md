# 🔐 SQL Injection Scanner

## 📌 Description

A Python-based tool that detects SQL Injection vulnerabilities by sending crafted payloads to web inputs and analyzing responses.

This project was built as part of cybersecurity learning and tested on controlled environments like DVWA.

---

## 🚀 Features

* Detects common SQL Injection patterns
* Sends crafted payload requests
* Identifies vulnerability indicators
* Logs results for analysis
* Supports basic concurrency
* Includes rate limiting to avoid server overload

---

## ⚙️ Technologies Used

* Python 3.11+
* Requests library
* XAMPP (Apache, MySQL, PHP)
* DVWA (Damn Vulnerable Web Application)

---

## 🛠️ Setup & Installation (Step-by-Step)

### 1️⃣ Install Python

* Install Python 3.11+
* Verify installation:

```bash
python --version
```

---

### 2️⃣ Install XAMPP

* Install XAMPP (Apache + MySQL + PHP)
* Start Apache and MySQL from XAMPP Control Panel

---

### 3️⃣ Install DVWA

```bash
cd C:\xampp\htdocs
git clone https://github.com/digininja/DVWA.git
cd DVWA\config
```

* Edit `config.inc.php`
* Update database settings:

  * DB Server: 127.0.0.1
  * Username: root
  * Password: (leave empty)

---

### 4️⃣ Setup DVWA Database

* Open browser:

```
http://localhost/DVWA/setup.php
```

* Click **Create / Reset Database**

---

### 5️⃣ Set DVWA Security Level

```
http://localhost/DVWA/security.php
```

* Set security level to **Low**

---

### 6️⃣ Install Dependencies

```bash
pip install requests
```

---

### 7️⃣ Run the Scanner

```bash
python sqli_scanner.py
```

---

## 📊 Output

* Generates log files:

  * `sqli.log`
  * `results.json`
* Displays detected vulnerabilities in terminal

---

## ⚠️ Disclaimer

This tool is developed for educational and ethical testing purposes only.

⚠️ Do NOT use on unauthorized websites.

Only test on:

* DVWA
* Local applications
* Authorized environments

---

## 📂 Project Structure

SQL_Injection_Scanner/

│
├── sqli_scanner.py

├── README.md

🔥 IMPORTANT TO NOTE

sqli_logs/ folder is automatically created upon running the sqli_scanner.py file.
