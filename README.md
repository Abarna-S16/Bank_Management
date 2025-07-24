# 💰 Bank Management System (Python CLI Project)

### A console-based Bank Management System written in Python that supports user registration, login authentication, deposit/withdraw transactions, and a full-featured admin dashboard to manage users.
Developed using PyCharm
---

## 🛠️ Features

### 👤 User Functionalities
- Register new account with password validation
- Secure login system (with 3 password attempts)
- Deposit and withdraw money with minimum balance enforcement
- View account balance
- Transaction history (with timestamps and running balance)
- Edit name or change password
- Persistent data storage in `users.json`

### 👑 Admin Functionalities
- View all active user accounts (tabulated format)
- Delete user accounts (soft delete to recovery bin)
- Recover deleted accounts
- Change admin password
- Admin account auto-created on first run (`Admin@123`)

---

## 🔐 Password Validation Rules

When creating or changing a password, it must:
- Be **6 to 25 characters** long
- Contain **at least 1 uppercase letter**
- Include **at least 1 number**
- Include **at least 1 special character** (`@ # $ % ^ & + = !`)

---

## 🗃️ Data Storage Format

All user data is stored in `users.json` with the following structure:

```json
{
  "next_account_id": 1001,
  "admin": {
    "name": "Admin",
    "password": "Admin@123"
  },
  "active_users": {
    "username1": {
      "name": "John",
      "password": "Pass@123",
      "account_id": 1001,
      "balance": 5000,
      "transactions": []
    }
  },
  "deleted_users": {
    ...
  }
}
```

---

## 📦 Technologies Used

- Python 3
- `pandas` and `tabulate` for displaying data
- `json` for data storage
- `datetime` and `time` for transaction logging and delays
- `getpass` for secure password input
- `re` for password regex validation

---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bank-management-system.git
cd bank-management-system
```

### 2. Install Requirements

```bash
pip install pandas tabulate
```

### 3. Run the Program

```bash
python "Bank System.py"
```

---

## 📝 Project Structure

```
Bank System.py       # Main Python program
users.json           # Auto-created on first run for data persistence
README.md            # Project documentation
```

---

## ✅ Sample Admin Credentials

- **Username:** `admin`
- **Password:** `Admin@123`

(You will be prompted to change it after login.)

---

## 🙌 Author

Developed by [Abarna](https://github.com/Abarna-S16)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
