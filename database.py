"""
Database handler for storing user data
Supports both SQLite (local) and PostgreSQL (cloud)
"""
import os
import json

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

import sqlite3

class Database:
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        
        if self.db_url and HAS_POSTGRES:
            self.db_type = 'postgres'
            self._init_postgres()
        else:
            self.db_type = 'sqlite'
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('discord_bot.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_links (
                discord_id TEXT PRIMARY KEY,
                leetcode_username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        print("✓ SQLite database initialized")
    
    def _init_postgres(self):
        """Initialize PostgreSQL database"""
        if self.db_url.startswith('postgres://'):
            self.db_url = self.db_url.replace('postgres://', 'postgresql://', 1)
        
        self.conn = psycopg2.connect(self.db_url)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_links (
                discord_id TEXT PRIMARY KEY,
                leetcode_username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        print("✓ PostgreSQL database initialized")
    
    def save_link(self, discord_id: str, leetcode_username: str):
        """Save or update a Discord ID to LeetCode username mapping"""
        cursor = self.conn.cursor()
        
        if self.db_type == 'sqlite':
            cursor.execute('''
                INSERT OR REPLACE INTO user_links (discord_id, leetcode_username, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (str(discord_id), leetcode_username))
        else:  # postgres
            cursor.execute('''
                INSERT INTO user_links (discord_id, leetcode_username, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (discord_id) 
                DO UPDATE SET leetcode_username = EXCLUDED.leetcode_username, 
                              updated_at = CURRENT_TIMESTAMP
            ''', (str(discord_id), leetcode_username))
        
        self.conn.commit()
    
    def get_link(self, discord_id: str):
        """Get LeetCode username for a Discord ID"""
        cursor = self.conn.cursor()
        
        if self.db_type == 'sqlite':
            cursor.execute('SELECT leetcode_username FROM user_links WHERE discord_id = ?', (str(discord_id),))
        else:  # postgres
            cursor.execute('SELECT leetcode_username FROM user_links WHERE discord_id = %s', (str(discord_id),))
        
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_all_links(self):
        """Get all Discord ID to LeetCode username mappings"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT discord_id, leetcode_username FROM user_links')
        
        results = cursor.fetchall()
        return {row[0]: row[1] for row in results}
    
    def migrate_from_json(self, json_file='user_data.json'):
        """Migrate data from old JSON file to database"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            for discord_id, leetcode_username in data.items():
                self.save_link(discord_id, leetcode_username)
            
            print(f"✓ Migrated {len(data)} users from {json_file} to database")
            return True
        except FileNotFoundError:
            print(f"No {json_file} found to migrate")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

db = None

def get_db():
    """Get or create database instance"""
    global db
    if db is None:
        db = Database()
        db.migrate_from_json()
    return db
