import os
import random
import sqlite3


def create_database():
    os.makedirs('data', exist_ok=True)
    db_path = 'data/josaa.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE institutes (
            institute_id INTEGER PRIMARY KEY,
            institute_name TEXT NOT NULL,
            institute_type TEXT NOT NULL,
            state TEXT,
            base_rank INTEGER
        );
        CREATE TABLE branches (
            branch_id INTEGER PRIMARY KEY,
            branch_name TEXT NOT NULL,
            branch_code TEXT,
            competitiveness REAL
        );
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL,
            multiplier REAL
        );
        CREATE TABLE cutoffs (
            cutoff_id INTEGER PRIMARY KEY,
            institute_id INTEGER,
            branch_id INTEGER,
            category_id INTEGER,
            year INTEGER,
            opening_rank INTEGER,
            closing_rank INTEGER,
            FOREIGN KEY (institute_id) REFERENCES institutes(institute_id),
            FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );
        CREATE INDEX idx_cutoffs_lookup ON cutoffs(institute_id, branch_id, category_id, year);
        CREATE INDEX idx_cutoffs_rank ON cutoffs(closing_rank);
    """)

    institutes = [
        (1, 'Indian Institute of Technology Bombay', 'IIT', 'Maharashtra', 44),
        (2, 'Indian Institute of Technology Delhi', 'IIT', 'Delhi', 63),
        (3, 'Indian Institute of Technology Madras', 'IIT', 'Tamil Nadu', 89),
        (4, 'Indian Institute of Technology Kanpur', 'IIT', 'Uttar Pradesh', 134),
        (5, 'Indian Institute of Technology Kharagpur', 'IIT', 'West Bengal', 178),
        (6, 'Indian Institute of Technology Roorkee', 'IIT', 'Uttarakhand', 251),
        (7, 'Indian Institute of Technology Guwahati', 'IIT', 'Assam', 421),
        (8, 'Indian Institute of Technology Hyderabad', 'IIT', 'Telangana', 892),
        (9, 'Indian Institute of Technology Indore', 'IIT', 'Madhya Pradesh', 1453),
        (10, 'Indian Institute of Technology BHU Varanasi', 'IIT', 'Uttar Pradesh', 687),
        (11, 'National Institute of Technology Tiruchirappalli', 'NIT', 'Tamil Nadu', 4523),
        (12, 'National Institute of Technology Warangal', 'NIT', 'Telangana', 5234),
        (13, 'National Institute of Technology Karnataka Surathkal', 'NIT', 'Karnataka', 5891),
        (14, 'National Institute of Technology Calicut', 'NIT', 'Kerala', 7234),
        (15, 'National Institute of Technology Rourkela', 'NIT', 'Odisha', 8976),
        (16, 'National Institute of Technology Jaipur', 'NIT', 'Rajasthan', 12456),
        (17, 'National Institute of Technology Kurukshetra', 'NIT', 'Haryana', 11234),
        (18, 'National Institute of Technology Silchar', 'NIT', 'Assam', 18765),
        (19, 'National Institute of Technology Durgapur', 'NIT', 'West Bengal', 16543),
        (20, 'National Institute of Technology Allahabad', 'NIT', 'Uttar Pradesh', 14321),
        (21, 'Indian Institute of Information Technology Hyderabad', 'IIIT', 'Telangana', 1234),
        (22, 'Indian Institute of Information Technology Allahabad', 'IIIT', 'Uttar Pradesh', 9876),
        (23, 'Indian Institute of Information Technology Bangalore', 'IIIT', 'Karnataka', 2876),
        (24, 'Indian Institute of Information Technology Gwalior', 'IIIT', 'Madhya Pradesh', 11234),
        (25, 'Indian Institute of Information Technology Jabalpur', 'IIIT', 'Madhya Pradesh', 15678),
        (26, 'Birla Institute of Technology Mesra', 'GFTI', 'Jharkhand', 21345),
        (27, 'Indian Institute of Engineering Science and Technology Shibpur', 'GFTI', 'West Bengal', 18234),
        (28, 'Sant Longowal Institute of Engineering and Technology', 'GFTI', 'Punjab', 25678),
    ]
    cursor.executemany("INSERT INTO institutes VALUES (?, ?, ?, ?, ?)", institutes)

    branches = [
        (1, 'Computer Science and Engineering', 'CSE', 1.0),
        (2, 'Artificial Intelligence', 'AI', 0.92),
        (3, 'Data Science and Engineering', 'DS', 0.95),
        (4, 'Electronics and Communication Engineering', 'ECE', 1.43),
        (5, 'Electrical Engineering', 'EE', 1.89),
        (6, 'Mechanical Engineering', 'ME', 2.34),
        (7, 'Civil Engineering', 'CE', 3.12),
        (8, 'Chemical Engineering', 'CHE', 2.67),
        (9, 'Aerospace Engineering', 'AE', 1.78),
        (10, 'Biotechnology', 'BT', 2.89),
        (11, 'Metallurgical and Materials Engineering', 'MME', 3.45),
        (12, 'Engineering Physics', 'EP', 2.12)
    ]
    cursor.executemany("INSERT INTO branches VALUES (?, ?, ?, ?)", branches)

    categories = [
        (1, 'OPEN', 1.0),
        (2, 'EWS', 1.28),
        (3, 'OBC-NCL', 1.73),
        (4, 'SC', 3.41),
        (5, 'ST', 4.67)
    ]
    cursor.executemany("INSERT INTO categories VALUES (?, ?, ?)", categories)

    cutoffs = []
    cutoff_id = 1
    year_trends = {2022: 1.08, 2023: 1.04, 2024: 1.0}
    for inst_id, _, inst_type, _, base_rank in institutes:
        for branch_id, _, _, branch_comp in branches:
            for cat_id, _, cat_mult in categories:
                for year, year_trend in year_trends.items():
                    opening = int(base_rank * branch_comp * cat_mult * year_trend * random.uniform(0.978, 1.033))
                    if inst_type == 'IIT' and inst_id <= 7:
                        closing_mult = random.uniform(1.30, 1.47)
                    elif inst_type == 'IIT':
                        closing_mult = random.uniform(1.44, 1.71)
                    elif inst_type == 'NIT':
                        closing_mult = random.uniform(1.78, 2.20)
                    elif inst_type == 'IIIT':
                        closing_mult = random.uniform(1.6, 1.94)
                    else:
                        closing_mult = random.uniform(1.84, 2.44)
                    closing = int(opening * closing_mult)
                    if opening >= closing:
                        closing = opening + random.randint(45, 175)
                    cutoffs.append((
                        cutoff_id, inst_id, branch_id, cat_id, year, opening, closing
                    ))
                    cutoff_id += 1
    cursor.executemany("INSERT INTO cutoffs VALUES (?, ?, ?, ?, ?, ?, ?)", cutoffs)

    conn.commit()
    print("\n[INFO] DATABASE CREATED SUCCESSFULLY")
    conn.close()


if __name__ == '__main__':
    create_database()
