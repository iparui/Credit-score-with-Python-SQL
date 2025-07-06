# Credit Score Calculator with Python & MySQL

This project calculates synthetic credit scores from user financial behavior data using Python and stores the results in a MySQL database. It’s designed to demonstrate data handling, SQL integration, and logic implementation — ideal for backend or data engineering portfolio projects.

---

## Overview

The calculator models a simplified credit scoring system based on industry-weighted components:

- Payment History (35%)
- Credit Utilization (30%)
- Credit History Length (15%)
- Credit Mix (10%)
- New Credit Inquiries (10%)

It processes dummy data through these metrics, computes a raw score (0–100), then scales it to the standard 300–850 range.

---

## Technologies Used

- Python 3
- Pandas
- MySQL
- mysql-connector-python

---

## How It Works

1. Loads dummy financial behavior data into a Pandas DataFrame.
2. Calculates each credit score component using simple formulas.
3. Combines weighted components into a final scaled score.
4. Connects to a MySQL database and alters the table schema if needed.
5. Inserts the final results into the SQL table.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/credit-score-sql.git
cd credit-score-sql
```

### 2. Create Virtual Environment and Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate       # or .venv\Scripts\activate on Windows
pip install pandas mysql-connector-python
```

### 3. Set Up MySQL

Create the database and table:

```sql
CREATE DATABASE credit_score;

CREATE TABLE credit_score_table_output (
    user_name VARCHAR(255)
);
```

Additional columns will be added automatically by the script.

### 4. Configure the Database Connection

Inside `main.py`, set your credentials:

```python
cnx = mysql.connector.connect(
    user='root',
    host='127.0.0.1',
    database='credit_score'
)
```

### 5. Run the Script

```bash
python main.py
```

---

## Sample Output

```
Database Connected
Column count: 2
Row count: 0
Column count after altering: 11
4 record(s) inserted.
Row count after: 4
```

---

## File Structure

```
├── main.py           # Main script for scoring and SQL upload
├── README.md         # Project documentation
├── requirements.txt  # Python dependencies
└── .venv/            # Virtual environment (excluded from version control)
```

---

## Future Enhancements

- Add user input via a web UI (Streamlit or Flask)
- Support file upload for batch credit scoring
- Add PDF/CSV export for credit score reports
- Refactor for use as a reusable Python package

---

## Author

**Dr. Ishita Parui**\
Website: [ishitaparui.com](https://ishitaparui.com)\
Location: Freiburg, Germany

---

## License

This project is open-source and available for educational and non-commercial use.

