# PlusNWipe
If you like order and cleanliness, and want to keep your terminal clean, this package is for you.  The module counts the number of times the terminal is running and cleans the terminal when it reaches the value you specify.

# CountFlushTerm

## 🌐 Language / Til
[🇬🇧 English](#english) | [🇺🇿 O'zbek](#uzbek)

---

## 🇬🇧 English

### 📌 About the Function

`CountFlushTerm` is a Python function that tracks how many times a script has been run in the terminal and automatically clears the terminal when it reaches a specified count.

### 🚀 Installation

Once the package is uploaded to PyPI, it can be installed using the following command:

```sh
pip install CountFlushTerm
```

Or install it manually:

```sh
git clone https://github.com/username/CountFlushTerm.git
cd CountFlushTerm
python setup.py install
```

### 🔹 Usage

```python
from CountFlushTerm import CountFlushTerm

# Clears the terminal after 5 runs
CountFlushTerm(5)
```

**Output:**
```
📢 `main.py` has been run 3 times in this terminal!
```
(After the 5th run)
```
🔄 Terminal cleared after 5 runs!
```

### 🔧 How It Works

1. Detects the script file where the function is called.
2. Saves the run count in a `.json` file.
3. Clears the terminal when the count reaches `auto_wipe`.
4. Displays the run count every time the script is executed.

### 🛠 Supported Systems

✅ **Windows** (`cls` to clear)
✅ **Linux & Mac** (`clear` to clear)
✅ **PyCharm & VS Code** (ANSI codes for clearing)

### 📜 License

MIT License

### 👨‍💻 Author

**Your Name** — [GitHub](https://github.com/username) | [LinkedIn](https://linkedin.com/in/username)

---

## 🇺🇿 O'zbek

### 📌 Funksiya haqida

`CountFlushTerm` — Python skripti terminalda nechchi marta ishga tushirilganini hisoblab boruvchi va belgilangan soniga yetganda terminalni avtomatik tozalovchi funksiya.

### 🚀 O'rnatish

Paket PyPI'ga yuklangandan keyin quyidagi buyruq orqali o'rnatish mumkin:

```sh
pip install CountFlushTerm
```

Yoki **manually** yuklab olish va o'rnatish:

```sh
git clone https://github.com/username/CountFlushTerm.git
cd CountFlushTerm
python setup.py install
```

### 🔹 Foydalanish

```python
from CountFlushTerm import CountFlushTerm

# Har 5-marta ishga tushganda terminalni tozalaydi
CountFlushTerm(5)
```

**Natija:**
```
📢 `main.py` ushbu terminalda 3-marta ishga tushirildi!
```
(5-marta ishga tushganda)
```
🔄 5-marta ishga tushdi va terminal tozalandi!
```

### 🔧 Ishlash mantig‘i

1. Funksiya chaqirilgan faylni aniqlaydi.
2. Ishga tushirishlar sonini `.json` faylga saqlaydi.
3. Agar hisoblagich `auto_wipe` qiymatiga yetsa, terminal avtomatik tozalanadi.
4. Har safar ishga tushganda terminalda ishga tushirilish sonini ko'rsatadi.

### 🛠 Qo'llab-quvvatlaydigan tizimlar

✅ **Windows** (`cls` bilan tozalaydi)
✅ **Linux & Mac** (`clear` bilan tozalaydi)
✅ **PyCharm & VS Code** (ANSI kodlar bilan tozalaydi)

### 📜 Litsenziya

MIT License

### 👨‍💻 Muallif

**Your Name** — [GitHub](https://github.com/username) | [LinkedIn](https://linkedin.com/in/username)

---

🚀 If you find this project useful, don’t forget to leave a star (`⭐`)!
🚀 Agar ushbu loyiha sizga foydali bo'lsa, yulduzcha (`⭐`) bosishni unutmang!

