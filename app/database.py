"""SQLite database layer for swim pool membership management."""

import os
import sqlite3
from datetime import datetime


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "swimpool.db")

FIELD_LABELS = {
    "name": "姓名",
    "phone": "手机号",
    "gender": "性别",
    "member_type": "会员类型",
    "remaining": "剩余次数",
    "notes": "备注",
}


class Database:
    """Handles all database operations for the swim pool app."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS members (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                phone       TEXT NOT NULL,
                gender      TEXT DEFAULT '',
                member_type TEXT DEFAULT '次卡',
                remaining   INTEGER DEFAULT 0,
                notes       TEXT DEFAULT '',
                avatar_path TEXT DEFAULT '',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS modification_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id   TEXT NOT NULL,
                field_name  TEXT NOT NULL,
                old_value   TEXT,
                new_value   TEXT,
                timestamp   TEXT NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def generate_member_id(self):
        """Generate next member ID in SP000001 format."""
        row = self.conn.execute(
            "SELECT id FROM members ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row:
            last_num = int(row["id"][2:])
            return f"SP{last_num + 1:06d}"
        return "SP000001"

    def add_member(self, name, phone, gender, member_type, remaining, notes="", avatar_path=""):
        """Insert a new member. Returns the new member's ID."""
        mid = self.generate_member_id()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            """INSERT INTO members
               (id, name, phone, gender, member_type, remaining, notes, avatar_path, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (mid, name, phone, gender, member_type, remaining, notes, avatar_path, now, now),
        )
        self.conn.commit()
        return mid

    def get_member(self, member_id):
        """Return a member dict by ID, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM members WHERE id = ?", (member_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_all_members(self, search=""):
        """Return list of member dicts, optionally filtered by name/phone search."""
        if search:
            pattern = f"%{search}%"
            rows = self.conn.execute(
                """SELECT * FROM members
                   WHERE name LIKE ? OR phone LIKE ? OR id LIKE ?
                   ORDER BY id DESC""",
                (pattern, pattern, pattern),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM members ORDER BY id DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def update_member(self, member_id, **kwargs):
        """Update member fields. Only changed fields are written and logged.

        Returns list of changed field names (Chinese labels) or empty list.
        """
        old = self.get_member(member_id)
        if not old:
            return []

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        changed = []

        for field, new_val in kwargs.items():
            if field not in old:
                continue
            old_val = str(old[field]) if old[field] is not None else ""
            new_str = str(new_val) if new_val is not None else ""
            if old_val == new_str:
                continue

            self.conn.execute(
                f"UPDATE members SET {field} = ?, updated_at = ? WHERE id = ?",
                (new_val, now, member_id),
            )
            self.conn.execute(
                """INSERT INTO modification_log
                   (member_id, field_name, old_value, new_value, timestamp)
                   VALUES (?, ?, ?, ?, ?)""",
                (member_id, field, old_val, new_str, now),
            )
            changed.append(FIELD_LABELS.get(field, field))

        self.conn.commit()
        return changed

    def add_visit(self, member_id, delta):
        """Quickly add or subtract remaining visits for a member.

        Positive delta = increase, negative = decrease.
        Clamps remaining to >= 0.
        Returns new remaining count or None if member not found.
        """
        member = self.get_member(member_id)
        if not member:
            return None

        new_val = max(0, member["remaining"] + delta)
        self.update_member(member_id, remaining=new_val)
        return new_val

    def change_member_type(self, member_id, new_type):
        """Quickly change member type. Returns True if changed."""
        member = self.get_member(member_id)
        if not member or member["member_type"] == new_type:
            return False
        self.update_member(member_id, member_type=new_type)
        return True

    def get_modification_log(self, member_id):
        """Return all modification log entries for a member, newest first."""
        rows = self.conn.execute(
            """SELECT * FROM modification_log
               WHERE member_id = ?
               ORDER BY id DESC""",
            (member_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def delete_member(self, member_id):
        """Delete a member and all their logs."""
        self.conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.conn.commit()

    def get_field_label(self, field_name):
        """Return Chinese display label for a field name."""
        return FIELD_LABELS.get(field_name, field_name)

    def close(self):
        self.conn.close()
