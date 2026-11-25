#  Price Tracker

Ένα εργαλείο γραμμής εντολών (CLI) σε **Python** για την παρακολούθηση τιμών προϊόντων από ηλεκτρονικά καταστήματα, την αποθήκευση του ιστορικού τιμών σε βάση δεδομένων **SQLite** και την αποστολή ειδοποίησης μέσω **Email** όταν πέφτει η τιμή.

## Λειτουργίες

- **Αυτόματο Web Scraping:** Ανακτά αυτόματα τον τίτλο και την τιμή του προϊόντος από το URL διαβάζοντας δομημένα δεδομένα (`application/ld+json`) και Open Graph meta tags (`og:title`, `og:price:amount`).
- **Χειροκίνητη Καταχώρηση (Fallback):** Αν η ιστοσελίδα μπλοκάρει την αυτόματη ανάγνωση (anti-bot protection), το πρόγραμμα επιτρέπει στον χρήστη να πληκτρολογήσει χειροκίνητα τον τίτλο και την τρέχουσα τιμή.
- **Ιστορικό Τιμών σε SQLite:** Αποθηκεύει τα προϊόντα και κάθε νέα μέτρηση τιμής (με ημερομηνία και ώρα) στην τοπική βάση δεδομένων `price_tracker.db`.
- **Σύγκριση Τιμών:** Ελέγχει την τρέχουσα τιμή σε σχέση με την τελευταία καταχωρημένη και ενημερώνει αν η τιμή ανέβηκε, έπεσε ή έμεινε ίδια.
- **Ειδοποιήσεις Email (Gmail SMTP):** Όταν εντοπιστεί πτώση τιμής, στέλνει αυτόματα email ειδοποίησης με τη νέα τιμή και το link του προϊόντος.

---

## Τεχνολογίες & Βιβλιοθήκες

- [Python 3](https://www.python.org/)
- [Requests](https://pypi.org/project/requests/) — Αποστολή HTTP αιτημάτων
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) — Ανάλυση HTML και εξαγωγή δεδομένων
- **SQLite (`sqlite3`)** — Τοπική βάση δεδομένων (ενσωματωμένη στην Python)
- **SMTP (`smtplib` & `email`)** — Αποστολή ειδοποιήσεων μέσω email (ενσωματωμένες στην Python)

---

##  Εγκατάσταση & Εκτέλεση

### Προαπαιτούμενα
- **Python 3.8+**
- **Λογαριασμός Gmail με App Password** (αν θέλεις να λειτουργούν οι ειδοποιήσεις email).

### Βήματα

1. **Κλωνοποίηση του repository:**
   ```bash
   git clone [https://github.com/mariach26/](https://github.com/mariach26/)<repository-name>.git
   cd <repository-name>
   2. **Εγκατάσταση εξαρτήσεων:**
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Ρύθμιση Email (Προαιρετικό για ειδοποιήσεις):**
   Άνοιξε το αρχείο `app.py` και συμπλήρωσε τα στοιχεία σου στη συνάρτηση `send_email_alert`:
   ```python
   sender_email = "your_email@gmail.com"
   receiver_email = "your_email@gmail.com"
   password = "your_gmail_app_password"
   ```
   > **Σημείωση:** Για το Gmail χρειάζεται να δημιουργηθεί ένα **App Password** από τις ρυθμίσεις ασφαλείας του Google λογαριασμού.

4. **Εκτέλεση της εφαρμογής:**
   ```bash
   python app.py
   ```
   Επικόλλησε το URL του προϊόντος που θέλεις να παρακολουθήσεις και πάτησε `Enter`.

---

##  Δομή Βάσης Δεδομένων (`price_tracker.db`)

Η βάση δημιουργείται αυτόματα κατά την πρώτη εκτέλεση με 2 πίνακες:
- **`products`**: Αποθηκεύει τα μοναδικά προϊόντα (`id`, `title`, `url`).
- **`price_history`**: Αποθηκεύει το ιστορικό των τιμών ανά προϊόν (`id`, `product_id`, `price`, `date`).

---

##  Δομή Project

```text
<repository-name>/
├── app.py              # Κύριο script (scraping, SQLite, email alerts)
├── price_tracker.db    # Βάση δεδομένων SQLite (δημιουργείται αυτόματα)
└── README.md           # Τεκμηρίωση του project
```
