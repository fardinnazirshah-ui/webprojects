import sqlite3
import os


class Database:
    def __init__(self, db_path="data/josaa.db"):
        if not os.path.exists(db_path):
            print("DB file missing — maybe run init_db.py?")
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_predictions(self, rank, exam_type, category):
        inst_types = ("IIT",) if exam_type == "Advanced" else ("NIT", "IIIT", "GFTI")
        placeholders = ",".join("?" for _ in inst_types)

        query = f"""
        SELECT i.institute_id, i.institute_name, i.institute_type,
               b.branch_id, b.branch_name,
               c.opening_rank, c.closing_rank, c.year
        FROM cutoffs c
        JOIN institutes i ON c.institute_id = i.institute_id
        JOIN branches b ON c.branch_id = b.branch_id
        JOIN categories cat ON c.category_id = cat.category_id
        WHERE i.institute_type IN ({placeholders})
          AND cat.category_name = ?
        """

        conn = self._connect()
        cur = conn.cursor()
        rows = cur.execute(query, (*inst_types, category)).fetchall()

        grouped = {}
        for row in rows:
            key = (row["institute_id"], row["branch_id"])
            if key not in grouped:
                grouped[key] = {
                    "institute": row["institute_name"],
                    "branch": row["branch_name"],
                    "opens": [],
                    "closes": [],
                    "years": {}
                }

            g = grouped[key]
            g["opens"].append(row["opening_rank"])
            g["closes"].append(row["closing_rank"])
            g["years"][row["year"]] = row["closing_rank"]

        results = []

        for _, data in grouped.items():
            opens = data["opens"]
            closes = data["closes"]

            avg_open = sum(opens) // len(opens) if opens else 0
            if closes:
                avg_close = sum(closes) // len(closes)
                best = min(closes)
                worst = max(closes)
            else:
                avg_close = best = worst = 0

            prob = self._probability(rank, avg_open, avg_close)
            if prob >= 50:
                results.append({
                    "institute": data["institute"],
                    "branch": data["branch"],
                    "avg_opening": avg_open,
                    "avg_closing": avg_close,
                    "best_closing": best,
                    "worst_closing": worst,
                    "probability": round(prob, 1),
                    "status": self._label(prob),
                    "years": data["years"]
                })

        results.sort(key=lambda x: x["avg_closing"])
        conn.close()
        return results[:100]

    def _probability(self, user_rank, open_rank, close_rank):
        if open_rank < 1 or open_rank > close_rank:
            open_rank = int(close_rank * 0.3)

        if user_rank <= open_rank:
            return 100.0
        elif user_rank > close_rank:
            diff = user_rank - close_rank
            return 50 - diff / 2 if diff < 100 else 0.0

        span = close_rank - open_rank or 1
        val = 100 - ((user_rank - open_rank) / span) * 100
        return val if val > 50 else 50.0

    def _label(self, p):
        if p >= 90:
            return "Highly Probable"
        if p >= 75:
            return "Probable"
        if p >= 60:
            return "Moderate"
        return "Low Probability"

    def get_stats(self):
        conn = self._connect()
        cur = conn.cursor()
        try:
            totals = {
                "total_cutoffs": cur.execute("SELECT COUNT(*) FROM cutoffs").fetchone()[0],
                "total_institutes": cur.execute(
                    "SELECT COUNT(DISTINCT institute_name) FROM institutes"
                ).fetchone()[0],
                "total_branches": cur.execute(
                    "SELECT COUNT(DISTINCT branch_name) FROM branches"
                ).fetchone()[0],
                "years_covered": cur.execute(
                    "SELECT COUNT(DISTINCT year) FROM cutoffs"
                ).fetchone()[0],
            }
            conn.close()
            return totals
        except Exception:
            conn.close()
            return {"total_cutoffs": 0, "total_institutes": 0, "total_branches": 0, "years_covered": 0}

