import os
import json
import csv
import uuid
import hashlib
import sqlite3
import requests
from io import StringIO
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash, Response, jsonify, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-dev-secret-key-1234')

PORTAL_PREFIX = '/portal'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
USERS_DB = os.path.join(DATA_DIR, 'users.db')
APPS_FILE = os.path.join(DATA_DIR, 'apps.json')
TOKEN_LOG_FILE = os.path.join(DATA_DIR, 'token_log.json')

# In-memory token store: token -> entry dict
_token_store: dict = {}

APP_VERSION = os.environ.get('APP_VERSION', 'v1.0.3')

@app.context_processor
def inject_version():
    return dict(app_version=APP_VERSION)

# ======================== HELPERS ========================

def get_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ---- SQLite user DB helpers ----

def get_db_conn():
    """取得 SQLite 連線並設定為字典模式"""
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    """Initialise (or migrate) SQLite database."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_db_conn()
    cur = conn.cursor()
    # Users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid      TEXT PRIMARY KEY,
            username    TEXT NOT NULL,
            pwd         TEXT NOT NULL,
            remark      TEXT DEFAULT '',
            phone       TEXT DEFAULT '',
            ext         TEXT DEFAULT '',
            email       TEXT DEFAULT '',
            wechat      TEXT DEFAULT '',
            is_admin    INTEGER DEFAULT 0,
            is_active   INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT ''
        )
    ''')
    # Apps table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            appname     TEXT NOT NULL,
            slug        TEXT DEFAULT '',
            app_address TEXT NOT NULL,
            remark      TEXT DEFAULT '',
            use_token   INTEGER DEFAULT 0,
            api_key     TEXT DEFAULT '',
            sort_order  INTEGER DEFAULT 0,
            is_active   INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT ''
        )
    ''')
    # Token log table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS token_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            token       TEXT UNIQUE NOT NULL,
            userid      TEXT NOT NULL,
            username    TEXT,
            appname     TEXT,
            created_at  TEXT DEFAULT ''
        )
    ''')
    # User-App Access table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_app_access (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            userid   TEXT NOT NULL,
            app_id   INTEGER NOT NULL,
            UNIQUE(userid, app_id)
        )
    ''')
    # User-Conversation mapping: persist Dify conversation_id per user per app
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_conversations (
            userid          TEXT NOT NULL,
            app_slug        TEXT NOT NULL,
            conversation_id TEXT NOT NULL,
            updated_at      TEXT DEFAULT '',
            PRIMARY KEY (userid, app_slug)
        )
    ''')
    # Message feedback content (Dify API does not return content in history)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS message_feedback (
            message_id  TEXT PRIMARY KEY,
            rating      TEXT NOT NULL,
            content     TEXT DEFAULT '',
            created_at  TEXT DEFAULT ''
        )
    ''')
    # --- 自動升級舊版資料庫欄位 (Migration) ---
    contact_fields = ["phone", "ext", "email", "wechat"]
    for field in contact_fields:
        try:
            cur.execute(f'ALTER TABLE users ADD COLUMN {field} TEXT DEFAULT ""')
            conn.commit()
        except sqlite3.OperationalError:
            pass # 欄位已存在

    try:
        cur.execute('ALTER TABLE apps ADD COLUMN api_key TEXT DEFAULT ""')
        conn.commit()
    except sqlite3.OperationalError:
        pass # 欄位已存在
        
    # 確保 TSC 機器人有預設金鑰 (若為空則補上)
    cur.execute('UPDATE apps SET api_key="app-Xkr1f443jaCxO1LEKkNguawm" WHERE slug="tsc_app" AND (api_key IS NULL OR api_key = "")')
    conn.commit()

    # Migration: Users
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    old_users = json.load(f)
                for u in old_users:
                    cur.execute(
                        'INSERT OR IGNORE INTO users (userid, username, pwd, remark, is_admin, is_active, created_at) VALUES (?,?,?,?,?,?,?)',
                        (u.get('userid'), u.get('username'), u.get('pwd'), u.get('remark',''),
                         1 if u.get('is_admin') else 0, 1, now)
                    )
                conn.commit()
                app.logger.info('Migrated users.json -> users.db')
            except Exception as exc:
                app.logger.warning(f'User migration skipped: {exc}')
        
        # 確保有預設的測試帳號 A123, B123, C123
        hashed = get_hash('1234')
        test_users = [
            ('A123', 'UserA (全權限)', hashed, '測試用，全 App', '0912345678', '101', 'a123@example.com', 'wechat_a123', 0, 1, now),
            ('B123', 'UserB (半權限)', hashed, '測試用，前 4 個 App', '0922345678', '102', 'b123@example.com', 'wechat_b123', 0, 1, now),
            ('C123', 'UserC (單權限)', hashed, '測試用，單一 App', '0932345678', '103', 'c123@example.com', 'wechat_c123', 0, 1, now),
            ('admin', 'Administrator', hashed, '系統管理員', '', '', 'admin@example.com', '', 1, 1, now)
        ]
        for u in test_users:
            cur.execute('INSERT OR IGNORE INTO users (userid, username, pwd, remark, phone, ext, email, wechat, is_admin, is_active, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)', u)
        conn.commit()

    # Migration & Seed: Apps
    cur.execute('SELECT COUNT(*) FROM apps')
    if cur.fetchone()[0] == 0:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Check if legacy apps.json exists
        legacy_apps = []
        if os.path.exists(APPS_FILE):
            try:
                with open(APPS_FILE, 'r', encoding='utf-8') as f:
                    legacy_apps = json.load(f)
            except: pass
        
        if legacy_apps:
            for i, a in enumerate(legacy_apps):
                cur.execute(
                    'INSERT INTO apps (appname, slug, app_address, remark, use_token, api_key, sort_order, created_at) VALUES (?,?,?,?,?,?,?,?)',
                    (a.get('appname'), a.get('slug',''), a.get('app_address'), a.get('remark',''),
                     1 if a.get('use_token') else 0, a.get('api_key', ''), i*10, now)
                )
            conn.commit()
            app.logger.info('Migrated apps.json -> users.db')
        else:
            # Insert 8 dummy apps as requested
            seeds = [
                ("TSC 機器人", "tsc_app", "http://localhost:8080/chatbot/8hX6JrWtbF4PtgOm", "TSC 問答機器人 (正式)", 1),
                ("TSC 機器人 (測試)", "tsc_app_test", "http://localhost:8080/chatbot/8hX6JrWtbF4PtgOm", "TSC 測試環境", 1),
                ("TSC 機器人 (備援)", "tsc_app_bak", "http://localhost:8080/chatbot/8hX6JrWtbF4PtgOm", "TSC 備援位址", 1),
                ("TSC 機器人 (舊版)", "tsc_app_v1", "http://localhost:8080/chatbot/8hX6JrWtbF4PtgOm", "TSC 歷史版本", 1),
                ("桃花源 文學助手", "peach_app", "http://localhost:8080/chat/Bz1Fu6QocQG8EUIY", "桃花源 文學助手 (正式)", 0),
                ("桃花源 (測試版)", "peach_app_test", "http://localhost:8080/chat/Bz1Fu6QocQG8EUIY", "文學助手 測試", 0),
                ("桃花源 (備援)", "peach_app_bak", "http://localhost:8080/chat/Bz1Fu6QocQG8EUIY", "文學助手 備援", 0),
                ("桃花源 (舊版)", "peach_app_v1", "http://localhost:8080/chat/Bz1Fu6QocQG8EUIY", "文學助手 歷史", 0),
            ]
            for i, (name, slug, addr, rem, tok) in enumerate(seeds):
                cur.execute(
                    'INSERT INTO apps (appname, slug, app_address, remark, use_token, api_key, sort_order, created_at) VALUES (?,?,?,?,?,?,?,?)',
                    (name, slug, addr, rem, tok, 'app-Xkr1f443jaCxO1LEKkNguawm' if slug == 'tsc_app' else '', i*10, now)
                )
            conn.commit()
            app.logger.info('Seed apps inserted.')
            
            # 給予測試帳號特定 App 權限
            all_apps = cur.execute('SELECT id FROM apps ORDER BY sort_order, id').fetchall()
            app_ids = [row[0] for row in all_apps]
            if app_ids:
                # A123: all
                for aid in app_ids:
                    cur.execute('INSERT OR IGNORE INTO user_app_access (userid, app_id) VALUES (?,?)', ('A123', aid))
                # B123: first 4
                for aid in app_ids[:4]:
                    cur.execute('INSERT OR IGNORE INTO user_app_access (userid, app_id) VALUES (?,?)', ('B123', aid))
                # C123: first 1
                cur.execute('INSERT OR IGNORE INTO user_app_access (userid, app_id) VALUES (?,?)', ('C123', app_ids[0]))
            conn.commit()

    # Migration: Token Logs
    cur.execute('SELECT COUNT(*) FROM token_log')
    if cur.fetchone()[0] == 0 and os.path.exists(TOKEN_LOG_FILE):
        try:
            with open(TOKEN_LOG_FILE, 'r', encoding='utf-8') as f:
                old_logs = json.load(f)
            if isinstance(old_logs, list):
                for log in old_logs:
                    cur.execute(
                        'INSERT OR IGNORE INTO token_log (token, userid, username, appname, created_at) VALUES (?,?,?,?,?)',
                        (log.get('token'), log.get('userid'), log.get('username'), log.get('appname'), log.get('timestamp'))
                    )
                conn.commit()
                app.logger.info('Migrated token_log.json -> users.db')
        except Exception as exc:
            app.logger.warning(f'Token log migration skipped: {exc}')

    conn.close()

def db_get_all_users():
    conn = get_db_conn()
    rows = conn.execute('SELECT * FROM users ORDER BY created_at').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_get_user(userid: str):
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM users WHERE userid=?', (userid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def db_add_user(userid, username, pwd_plain, remark, is_admin, phone='', ext='', email='', wechat=''):
    hashed = get_hash(pwd_plain)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    try:
        conn.execute(
            'INSERT INTO users (userid, username, pwd, remark, phone, ext, email, wechat, is_admin, is_active, created_at) VALUES (?,?,?,?,?,?,?,?,?,1,?)',
            (userid, username, hashed, remark, phone, ext, email, wechat, 1 if is_admin else 0, now)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, f'帳號 {userid} 已存在'
    finally:
        conn.close()

def db_delete_user(userid: str):
    conn = get_db_conn()
    conn.execute('DELETE FROM users WHERE userid=?', (userid,))
    conn.commit()
    conn.close()

def db_update_user(userid, username, remark, is_admin, is_active, phone='', ext='', email='', wechat=''):
    conn = get_db_conn()
    conn.execute(
        'UPDATE users SET username=?, remark=?, is_admin=?, is_active=?, phone=?, ext=?, email=?, wechat=? WHERE userid=?',
        (username, remark, 1 if is_admin else 0, 1 if is_active else 0, phone, ext, email, wechat, userid)
    )
    conn.commit()
    conn.close()

def db_reset_password(userid: str, pwd_plain: str):
    hashed = get_hash(pwd_plain)
    conn = get_db_conn()
    conn.execute('UPDATE users SET pwd=? WHERE userid=?', (hashed, userid))
    conn.commit()
    conn.close()

# ---- SQLite app DB helpers ----

def db_get_all_apps(only_active=True):
    conn = get_db_conn()
    if only_active:
        rows = conn.execute('SELECT * FROM apps WHERE is_active=1 ORDER BY sort_order ASC, id ASC').fetchall()
    else:
        rows = conn.execute('SELECT * FROM apps ORDER BY sort_order ASC, id ASC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_get_apps_for_user(userid: str):
    """
    實作白名單邏輯：
    1. 針對特定網域 Email，強制繼承 A123 的權限設定。
    2. 檢查該 user 是否有任何授權設定。
    3. 若有設定，僅列出有授權且 is_active=1 的 App。
    4. 若無設定（沙盒模式），列出所有 is_active=1 的 App。
    """
    effective_userid = userid
    # 特定網域 Email 使用 A123 的權限範本
    if userid and "@" in userid and (userid.endswith("@gyro.com.tw") or userid.endswith("@gyrobot.com")):
        effective_userid = 'A123'

    conn = get_db_conn()
    
    # 檢查是否有任何授權記錄
    count_row = conn.execute('SELECT COUNT(*) FROM user_app_access WHERE userid=?', (effective_userid,)).fetchone()
    has_rules = count_row[0] > 0
    
    if has_rules:
        query = '''
            SELECT a.* FROM apps a
            INNER JOIN user_app_access uaa ON a.id = uaa.app_id
            WHERE uaa.userid = ? AND a.is_active = 1
            ORDER BY a.sort_order ASC, a.id ASC
        '''
        rows = conn.execute(query, (effective_userid,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM apps WHERE is_active=1 ORDER BY sort_order ASC, id ASC').fetchall()
        
    conn.close()
    return [dict(r) for r in rows]

def db_get_user_app_ids(userid: str):
    """取得某位使用者的所有授權 App ID 清單"""
    conn = get_db_conn()
    rows = conn.execute('SELECT app_id FROM user_app_access WHERE userid=?', (userid,)).fetchall()
    conn.close()
    return [r[0] for r in rows]

def db_set_user_apps(userid: str, app_id_list: list):
    """全量覆寫使用者的授權清單"""
    conn = get_db_conn()
    conn.execute('DELETE FROM user_app_access WHERE userid=?', (userid,))
    for aid in app_id_list:
        try:
            conn.execute('INSERT INTO user_app_access (userid, app_id) VALUES (?,?)', (userid, int(aid)))
        except (ValueError, sqlite3.IntegrityError):
            continue
    conn.commit()
    conn.close()

def db_get_app(app_id: int):
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM apps WHERE id=?', (app_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def db_save_message_feedback(message_id: str, rating: str, content: str = ''):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    conn.execute(
        'INSERT INTO message_feedback (message_id, rating, content, created_at) VALUES (?,?,?,?) '
        'ON CONFLICT(message_id) DO UPDATE SET rating=excluded.rating, content=excluded.content, created_at=excluded.created_at',
        (message_id, rating, content, now)
    )
    conn.commit()
    conn.close()

def db_get_message_feedbacks(message_ids: list) -> dict:
    """回傳 {message_id: {rating, content}} mapping"""
    if not message_ids:
        return {}
    conn = get_db_conn()
    placeholders = ','.join('?' * len(message_ids))
    rows = conn.execute(
        f'SELECT message_id, rating, content FROM message_feedback WHERE message_id IN ({placeholders})',
        message_ids
    ).fetchall()
    conn.close()
    return {r['message_id']: {'rating': r['rating'], 'content': r['content']} for r in rows}

def db_get_conversation_id(userid: str, app_slug: str) -> str:
    conn = get_db_conn()
    row = conn.execute(
        'SELECT conversation_id FROM user_conversations WHERE userid=? AND app_slug=?',
        (userid, app_slug)
    ).fetchone()
    conn.close()
    return row['conversation_id'] if row else ''

def db_save_conversation_id(userid: str, app_slug: str, conversation_id: str):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    conn.execute(
        'INSERT INTO user_conversations (userid, app_slug, conversation_id, updated_at) VALUES (?,?,?,?) '
        'ON CONFLICT(userid, app_slug) DO UPDATE SET conversation_id=excluded.conversation_id, updated_at=excluded.updated_at',
        (userid, app_slug, conversation_id, now)
    )
    conn.commit()
    conn.close()

def db_get_app_by_slug(slug: str):
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM apps WHERE slug=?', (slug,)).fetchone()
    conn.close()
    return dict(row) if row else None

def db_add_app(appname, slug, app_address, remark, use_token, api_key='', sort_order=0):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    cur = conn.execute(
        'INSERT INTO apps (appname, slug, app_address, remark, use_token, api_key, sort_order, created_at) VALUES (?,?,?,?,?,?,?,?)',
        (appname, slug, app_address, remark, 1 if use_token else 0, api_key, sort_order, now)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def db_update_app(app_id, appname, slug, app_address, remark, use_token, api_key, sort_order, is_active):
    conn = get_db_conn()
    conn.execute(
        'UPDATE apps SET appname=?, slug=?, app_address=?, remark=?, use_token=?, api_key=?, sort_order=?, is_active=? WHERE id=?',
        (appname, slug, app_address, remark, 1 if use_token else 0, api_key, sort_order, 1 if is_active else 0, app_id)
    )
    conn.commit()
    conn.close()

def db_delete_app(app_id):
    conn = get_db_conn()
    conn.execute('DELETE FROM apps WHERE id=?', (app_id,))
    conn.commit()
    conn.close()

# ---- JSON helpers (apps / token_log) ----

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(APPS_FILE):
        with open(APPS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(TOKEN_LOG_FILE):
        with open(TOKEN_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def read_json(filepath):
    ensure_data_dir()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_json(filepath, data):
    ensure_data_dir()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_dify_answer(text: str) -> str:
    """移除 Dify workflow 洩漏的系統 prompt 前綴（如 'We need to answer again...'）"""
    import re
    # 移除開頭至 "Just answer." 之間的系統指令段落
    text = re.sub(r'^.*?Just answer\.\s*', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除 <think>...</think>（deepseek 等推理模型）
    text = re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)
    return text.strip()

def generate_access_token(userid: str, username: str, appname: str) -> str:
    """Generate a UUID token and persist to database."""
    token = uuid.uuid4().hex
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. Store in memory for immediate hot lookup
    entry = {
        "token": token,
        "userid": userid,
        "username": username,
        "appname": appname,
        "timestamp": now
    }
    _token_store[token] = entry

    # 2. Persist to DB
    conn = get_db_conn()
    try:
        conn.execute(
            'INSERT INTO token_log (token, userid, username, appname, created_at) VALUES (?,?,?,?,?)',
            (token, userid, username, appname, now)
        )
        conn.commit()
    except Exception as e:
        app.logger.error(f"Error persisting token: {e}")
    finally:
        conn.close()
    
    return token

# ======================== DECORATORS ========================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            next_url = request.full_path if request.query_string else request.path
            return redirect(f"{PORTAL_PREFIX}/login?next={next_url}")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session or not session.get('is_admin'):
            flash("權限不足，需要管理員權限", "danger")
            return redirect(PORTAL_PREFIX + '/apps')
        return f(*args, **kwargs)
    return decorated_function

# ======================== PUBLIC ROUTES ========================

@app.route('/')
@app.route(PORTAL_PREFIX)
@app.route(PORTAL_PREFIX + '/')
def index():
    if 'userid' in session:
        return redirect(PORTAL_PREFIX + '/apps')
    return redirect(PORTAL_PREFIX + '/login')

@app.route(PORTAL_PREFIX + '/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next', PORTAL_PREFIX + '/apps')
    if request.method == 'POST':
        userid = request.form.get('userid', '').strip()
        pwd = request.form.get('pwd', '')

        # 特定網域 Email 登入邏輯：不需要檢查資料庫，也不需填寫密碼，權限同 A123
        if "@" in userid:
            if userid.endswith("@gyro.com.tw") or userid.endswith("@gyrobot.com"):
                session['userid'] = userid
                session['username'] = userid  # 改為使用完整 Email
                session['is_admin'] = False
                return redirect(next_url)
            else:
                flash("登入錯誤：目前僅提供 @gyro.com.tw 或 @gyrobot.com 網址", "danger")
                return render_template('login.html', portal_prefix=PORTAL_PREFIX, next_url=next_url)

        hashed_pwd = get_hash(pwd)
        users = db_get_all_users()
        user = next((u for u in users if u.get('userid') == userid
                     and u.get('pwd') == hashed_pwd
                     and u.get('is_active', 1)), None)

        if user:
            session['userid'] = user['userid']
            session['username'] = user['username']
            session['is_admin'] = bool(user.get('is_admin', False))
            
            # 修正：登入成功後導向原本想去的頁面 (next_url)
            return redirect(next_url)
        else:
            flash("帳號或密碼錯誤，或帳號已被停用", "danger")

    return render_template('login.html', portal_prefix=PORTAL_PREFIX, next_url=next_url)

@app.route(PORTAL_PREFIX + '/embedded_chat')
@login_required
def embedded_chat():
    """Embedded Dify Chatbot page - rendered after login."""
    return render_template(
        'chat.html',
        portal_prefix=PORTAL_PREFIX,
        userid=session.get('userid', ''),
        username=session.get('username', '')
    )

@app.route(PORTAL_PREFIX + '/chat/send', methods=['POST'])
@login_required
def chat_send():
    """
    Proxy to call Dify Chat API
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    query = data.get('query', '')
    userid = session.get('userid', 'unknown')

    # 優先用前端傳來的 conversation_id；否則從 DB 取回上次的對話
    conversation_id = data.get('conversation_id', '') or db_get_conversation_id(userid, 'tsc_app')

    api_url = "http://api:5001/v1/chat-messages"
    # 優先取 session 中的 API Key，無則動態從 DB 撈 tsc_app 的金鑰
    api_key = session.get('app_api_key')
    if not api_key:
        tsc = db_get_app_by_slug('tsc_app')
        api_key = tsc.get('api_key', '') if tsc else ''
        if api_key:
            session['app_api_key'] = api_key  # 補存進 session
        else:
            return jsonify({"error": "API Key 未設定，請至後台設定 tsc_app 的 API Key"}), 400

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "user": userid
    }
    
    if conversation_id:
        payload["conversation_id"] = conversation_id

    try:
        response = requests.post(api_url, json=payload, headers=headers, stream=True, timeout=120)
        response.raise_for_status()

        answer_text = ""
        conv_id = conversation_id
        msg_id = None

        import json as json_lib
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        data_chunk = json_lib.loads(decoded_line[6:])
                        event_type = data_chunk.get('event')
                        
                        # capture conversation id and message id if available
                        if 'conversation_id' in data_chunk:
                            conv_id = data_chunk['conversation_id']
                        if 'message_id' in data_chunk:
                            msg_id = data_chunk['message_id']

                        if event_type == 'message':
                            answer_text += data_chunk.get('answer', '')
                        elif event_type == 'text_chunk':
                            answer_text += data_chunk.get('data', {}).get('text', '')
                        elif event_type == 'workflow_finished':
                            outputs = data_chunk.get('data', {}).get('outputs', {})
                            if not answer_text and 'answer' in outputs:
                                answer_text = outputs['answer']

                    except json_lib.JSONDecodeError:
                        pass
        
        answer_text = clean_dify_answer(answer_text)

        # 將 Dify 回傳的 conversation_id 持久化到 DB，確保下次登入仍繼續同一對話
        if conv_id and conv_id != conversation_id:
            db_save_conversation_id(userid, 'tsc_app', conv_id)

        return jsonify({
            "answer": answer_text,
            "conversation_id": conv_id,
            "message_id": msg_id
        })
    except Exception as e:
        app.logger.error(f"Error calling Dify API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route(PORTAL_PREFIX + '/chat/feedback', methods=['POST'])
@login_required
def chat_feedback():
    """
    Proxy to send rating (like/dislike) and reason (content) to Dify
    """
    data = request.get_json()
    if not data or not data.get('message_id'):
        return jsonify({"error": "Missing message_id"}), 400

    message_id = data.get('message_id')
    rating = data.get('rating') # 'like' or 'dislike'
    content = data.get('content', '')
    userid = session.get('userid', 'unknown')

    api_url = f"http://api:5001/v1/messages/{message_id}/feedbacks"
    api_key = session.get('app_api_key')
    if not api_key:
        tsc = db_get_app_by_slug('tsc_app')
        api_key = tsc.get('api_key', '') if tsc else ''
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "rating": rating,
        "user": userid
    }
    if content:
        payload["content"] = content

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        # 本地存一份，因 Dify /v1/messages 不回傳 feedback content
        db_save_message_feedback(message_id, rating, content)
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Error sending Dify feedback: {e}")
        return jsonify({"error": str(e)}), 500

@app.route(PORTAL_PREFIX + '/chat/history', methods=['GET'])
@login_required
def chat_history():
    """Proxy to fetch conversation history from Dify"""
    userid = session.get('userid', 'unknown')
    conv_id = db_get_conversation_id(userid, 'tsc_app')

    if not conv_id:
        return jsonify({"messages": [], "conversation_id": ""})

    api_key = session.get('app_api_key')
    if not api_key:
        tsc = db_get_app_by_slug('tsc_app')
        api_key = tsc.get('api_key', '') if tsc else ''
        if api_key:
            session['app_api_key'] = api_key

    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"conversation_id": conv_id, "user": userid, "limit": 50}

    try:
        response = requests.get(
            "http://api:5001/v1/messages",
            headers=headers, params=params, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        messages = data.get("data", [])
        for msg in messages:
            if msg.get("answer"):
                msg["answer"] = clean_dify_answer(msg["answer"])

        # 補入本地儲存的 feedback content（Dify API 不回傳 content）
        msg_ids = [m["id"] for m in messages if m.get("id")]
        local_fb = db_get_message_feedbacks(msg_ids)
        for msg in messages:
            mid = msg.get("id")
            if mid and mid in local_fb:
                if msg.get("feedback") is None:
                    msg["feedback"] = {}
                msg["feedback"]["content"] = local_fb[mid].get("content", "")

        return jsonify({
            "messages": messages,
            "conversation_id": conv_id,
            "has_more": data.get("has_more", False)
        })
    except Exception as e:
        app.logger.error(f"Error fetching Dify history: {e}")
        return jsonify({"messages": [], "conversation_id": conv_id, "error": str(e)})

@app.route(PORTAL_PREFIX + '/logout')
def logout():
    session.clear()
    return redirect(PORTAL_PREFIX + '/login')

@app.route(PORTAL_PREFIX + '/apps')
@login_required
def apps_list():
    userid = session.get('userid')
    apps = db_get_apps_for_user(userid)
    return render_template('apps.html', apps=apps, session=session, portal_prefix=PORTAL_PREFIX)

# ======================== GATEWAY ROUTES ========================

@app.route(PORTAL_PREFIX + '/goto/tsc_app')
@login_required
def goto_tsc_app():
    """
    Gateway for tsc_app: verifies login, generates a UUID token,
    logs the token->userid mapping, and redirects to the Dify Chat URL.
    """
    apps = db_get_all_apps()
    # Find the app whose slug key is 'tsc_app'
    target = next((a for a in apps if a.get('slug') == 'tsc_app'), None)
    if not target:
        flash("找不到 TSC 機器人設定，請在後台新增 slug=tsc_app 的 App。", "danger")
        return redirect(PORTAL_PREFIX + '/apps')

    dify_url = target.get('app_address', '')
    if not dify_url:
        flash("TSC 機器人的 Chat URL 尚未設定，請在後台更新。", "danger")
        return redirect(PORTAL_PREFIX + '/apps')

    # 直接使用 userid（如 A123）作為 Dify 的 user 參數
    # 這會讓 Dify 日誌的「使用者或賬戶」欄位顯示真實帳號而非 UUID
    # 注意：此方式讓使用者在技術上可以修改 URL，後續可再加 Token 安全層
    # 直接使用 userid (例如 A123) 作為 Dify 的 user 參數
    # 這會讓 Dify 日誌的「使用者或賬戶」欄位顯示真實帳號
    # 使用相對路徑跳轉，讓瀏覽器處理 Host 和 Port 防止 502/404 衝突
    # 解析出相對路徑，優先處理 /chatbot/，再處理 /chat/
    path = ""
    if "/chatbot/" in dify_url:
        path = f"/chatbot/{dify_url.split('/chatbot/')[-1]}"
    elif "/chat/" in dify_url:
        path = f"/chat/{dify_url.split('/chat/')[-1]}"
    else:
        # 如果是絕對路徑但包含 localhost，嘗試轉為相對
        path = dify_url.replace("http://localhost:8080", "").replace("http://localhost", "")

    userid = session.get('userid', 'unknown')
    username = session.get('username', 'unknown')
    generate_access_token(userid, username, target['appname'])
    
    # 將對應 App 的 API Key 存入 Session 供後續聊天調用
    session['app_api_key'] = target.get('api_key', '')

    sep = '&' if '?' in path else '?'
    # 還原：使用 Dify 最原始支援的 user 參數，這會自動填入 Dify 的系統變數 sys.user_id
    final_path = f"{path}{sep}user={userid}"
    
    # Redirect to the embedded chat UI
    return redirect(url_for('embedded_chat'), code=302)

@app.route(PORTAL_PREFIX + '/go/<slug>')
@login_required
def goto_app_by_slug(slug):
    """
    通用 Slug 入口：透過 Slug 找到對應 App 並執行跳轉。
    範例：/portal/go/tsc_app
    """
    if slug == 'tsc_app':
        return redirect(url_for('goto_tsc_app'))
    
    app_record = db_get_app_by_slug(slug)
    if not app_record:
        flash(f"找不到應用程式代碼: {slug}", "danger")
        return redirect(PORTAL_PREFIX + '/apps')
    
    # 這裡可以根據 app_record 的設定決定如何跳轉
    target_addr = app_record['app_address']
    
    # 如果是 Dify 相關網址，自動補上身分參數 (非 Token 模式)
    if not app_record.get('use_token'):
        sep = '&' if '?' in target_addr else '?'
        userid = session.get('userid', 'unknown')
        username = session.get('username', 'unknown')
        target_addr = f"{target_addr}{sep}user={userid}"

    return redirect(target_addr)

@app.route(PORTAL_PREFIX + '/verify_token')
def verify_token():
    """
    Enhanced verification: Supports both token=UUID and user=UserID.
    Used by Dify HTTP node to identify current user.
    """
    token = request.args.get('token')
    user_id = request.args.get('user')  # Direct userid lookup
    
    # 1. Try Token lookup first
    if token and token in _token_store:
        entry = _token_store[token]
        return jsonify({
            "valid": True,
            "userid": entry['userid'],
            "username": entry['username'],
            "appname": entry['appname']
        })
    
    # 1.5 Try DB lookup if not in memory (e.g. after server restart)
    if token:
        conn = get_db_conn()
        row = conn.execute('SELECT * FROM token_log WHERE token=?', (token,)).fetchone()
        conn.close()
        if row:
            # Re-cache to memory
            _token_store[token] = {
                "userid": row['userid'],
                "username": row['username'],
                "appname": row['appname'],
                "timestamp": row['created_at']
            }
            return jsonify({
                "valid": True,
                "userid": row['userid'],
                "username": row['username'],
                "appname": row['appname']
            })
    
    # 2. If no token, try direct UserID lookup (for Dify integration)
    if user_id:
        user = db_get_user(user_id)
        if user:
            return jsonify({
                "valid": True,
                "userid": user['userid'],
                "username": user['username'],
                "appname": "TSC_Dify"
            })
            
    return jsonify({"valid": False, "error": "Invalid token or user"}), 4014

# ======================== ADMIN ROUTES ========================

@app.route(PORTAL_PREFIX + '/admin')
@admin_required
def admin_index():
    return render_template('admin/index.html', session=session, portal_prefix=PORTAL_PREFIX)

@app.route(PORTAL_PREFIX + '/admin/token_log')
@admin_required
def admin_token_log():
    conn = get_db_conn()
    rows = conn.execute('SELECT * FROM token_log ORDER BY id DESC LIMIT 2000').fetchall()
    conn.close()
    logs = [dict(r) for r in rows]
    # Rename created_at to timestamp for template compatibility
    for l in logs:
        l['timestamp'] = l['created_at']
    return render_template('admin/token_log.html', logs=logs, session=session, portal_prefix=PORTAL_PREFIX)

@app.route(PORTAL_PREFIX + '/admin/user_apps', methods=['GET', 'POST'])
@admin_required
def admin_user_apps():
    users = db_get_all_users()
    apps = db_get_all_apps()
    
    # 預設選取第一位使用者 (或由 query 參數指定)
    target_userid = request.args.get('userid') or (users[0]['userid'] if users else None)
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update':
            target_userid = request.form.get('userid')
            # 取得被勾選的所有 app_id 陣列
            selected_apps = request.form.getlist('app_ids')
            db_set_user_apps(target_userid, selected_apps)
            flash(f'已更新使用者 {target_userid} 的 App 存取權限', 'success')
            return redirect(PORTAL_PREFIX + f'/admin/user_apps?userid={target_userid}')
            
    # 取得目標用目前的授權 app_id 清單
    user_app_ids = db_get_user_app_ids(target_userid) if target_userid else []
            
    return render_template('admin/user_apps.html', 
                           users=users, 
                           apps=apps, 
                           target_userid=target_userid,
                           user_app_ids=user_app_ids,
                           session=session, 
                           portal_prefix=PORTAL_PREFIX)

@app.route(PORTAL_PREFIX + '/admin/users', methods=['GET', 'POST'])
@admin_required
def admin_users():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            userid   = request.form.get('userid', '').strip()
            username = request.form.get('username', '').strip()
            pwd      = request.form.get('pwd', '')
            remark   = request.form.get('remark', '')
            phone    = request.form.get('phone', '')
            ext      = request.form.get('ext', '')
            email    = request.form.get('email', '')
            wechat   = request.form.get('wechat', '')
            is_admin = request.form.get('is_admin') == 'on'
            ok, err = db_add_user(userid, username, pwd, remark, is_admin, phone, ext, email, wechat)
            flash('新增使用者成功' if ok else err, 'success' if ok else 'danger')

        elif action == 'delete':
            uid = request.form.get('userid')
            if uid == 'admin':
                flash('無法刪除預設管理員', 'danger')
            else:
                db_delete_user(uid)
                flash('刪除使用者成功', 'success')

        elif action == 'edit':
            uid      = request.form.get('userid')
            username = request.form.get('username', '').strip()
            remark   = request.form.get('remark', '')
            phone    = request.form.get('phone', '')
            ext      = request.form.get('ext', '')
            email    = request.form.get('email', '')
            wechat   = request.form.get('wechat', '')
            is_admin = request.form.get('is_admin') == 'on'
            is_active = request.form.get('is_active') == 'on'
            db_update_user(uid, username, remark, is_admin, is_active, phone, ext, email, wechat)
            flash('使用者資料已更新', 'success')

        elif action == 'reset_pwd':
            uid = request.form.get('userid')
            new_pwd = request.form.get('new_pwd', '')
            if not new_pwd:
                flash('密碼不得為空', 'danger')
            else:
                db_reset_password(uid, new_pwd)
                flash(f'帳號 {uid} 密碼已重設', 'success')

        return redirect(PORTAL_PREFIX + '/admin/users')

    users = db_get_all_users()
    return render_template('admin/users.html', users=users, session=session, portal_prefix=PORTAL_PREFIX)

@app.route(PORTAL_PREFIX + '/admin/users/export')
@admin_required
def export_users():
    users = db_get_all_users()
    si = StringIO()
    fieldnames = ['userid', 'username', 'remark', 'phone', 'ext', 'email', 'wechat', 'is_admin', 'is_active', 'created_at']
    cw = csv.DictWriter(si, fieldnames=fieldnames)
    cw.writeheader()
    for u in users:
        cw.writerow({k: u.get(k, '') for k in fieldnames})
    output = si.getvalue().encode('utf-8-sig')
    return Response(output, mimetype='text/csv', headers={'Content-disposition': 'attachment; filename=users.csv'})

@app.route(PORTAL_PREFIX + '/admin/users/import', methods=['POST'])
@admin_required
def import_users():
    file = request.files.get('file')
    if not file:
        flash('未上傳檔案', 'danger')
        return redirect(PORTAL_PREFIX + '/admin/users')
    try:
        stream = StringIO(file.stream.read().decode('utf-8-sig'))
        reader = csv.DictReader(stream)
        count = 0
        for row in reader:
            uid = row.get('userid', '').strip()
            if not uid:
                continue
            existing = db_get_user(uid)
            is_admin  = str(row.get('is_admin', '')).lower() in ['true', '1', 'yes']
            is_active = str(row.get('is_active', '1')).lower() not in ['false', '0', 'no']
            if existing:
                db_update_user(uid, row.get('username', existing['username']).strip(),
                               row.get('remark', existing['remark']), is_admin, is_active,
                               row.get('phone', existing['phone']), row.get('ext', existing['ext']),
                               row.get('email', existing['email']), row.get('wechat', existing['wechat']))
            else:
                pwd_raw = row.get('pwd', 'changeme')
                db_add_user(uid, row.get('username', uid).strip(), pwd_raw,
                            row.get('remark', ''), is_admin,
                            row.get('phone', ''), row.get('ext', ''),
                            row.get('email', ''), row.get('wechat', ''))
            count += 1
        flash(f'成功匯入/更新 {count} 筆使用者資料', 'success')
    except Exception as e:
        flash(f'匯入失敗: {e}', 'danger')
    return redirect(PORTAL_PREFIX + '/admin/users')

@app.route(PORTAL_PREFIX + '/admin/apps', methods=['GET', 'POST'])
@admin_required
def admin_apps():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            app_name = request.form.get('appname', '').strip()
            slug = request.form.get('slug', '').strip()
            addr = request.form.get('app_address', '').strip()
            rem = request.form.get('remark', '')
            tok = request.form.get('use_token') == 'on'
            key = request.form.get('api_key', '').strip()
            sort = int(request.form.get('sort_order', 0))
            db_add_app(app_name, slug, addr, rem, tok, key, sort)
            flash("新增應用程式成功", "success")
        elif action == 'edit':
            aid = int(request.form.get('id'))
            app_name = request.form.get('appname', '').strip()
            slug = request.form.get('slug', '').strip()
            addr = request.form.get('app_address', '').strip()
            rem = request.form.get('remark', '')
            tok = request.form.get('use_token') == 'on'
            key = request.form.get('api_key', '').strip()
            sort = int(request.form.get('sort_order', 0))
            active = request.form.get('is_active') == 'on'
            db_update_app(aid, app_name, slug, addr, rem, tok, key, sort, active)
            flash("更新應用程式成功", "success")
        elif action == 'delete':
            aid = request.form.get('id')
            if aid:
                db_delete_app(int(aid))
                flash("刪除應用程式成功", "success")
        return redirect(PORTAL_PREFIX + '/admin/apps')
    
    apps = db_get_all_apps(only_active=False)
    return render_template('admin/apps.html', apps=apps, session=session, portal_prefix=PORTAL_PREFIX)

@app.route(PORTAL_PREFIX + '/admin/apps/export')
@admin_required
def export_apps():
    apps = db_get_all_apps(only_active=False)
    si = StringIO()
    cw = csv.DictWriter(si, fieldnames=['id', 'appname', 'slug', 'app_address', 'remark', 'use_token', 'api_key', 'sort_order', 'is_active', 'created_at'])
    cw.writeheader()
    cw.writerows(apps)
    output = si.getvalue().encode('utf-8-sig')
    return Response(output, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=apps.csv"})

@app.route(PORTAL_PREFIX + '/admin/apps/import', methods=['POST'])
@admin_required
def import_apps():
    file = request.files.get('file')
    if not file:
        flash("未上傳檔案", "danger")
        return redirect(PORTAL_PREFIX + '/admin/apps')
    try:
        stream = StringIO(file.stream.read().decode("utf-8-sig"))
        reader = csv.DictReader(stream)
        count = 0
        for row in reader:
            aname = (row.get('appname') or '').strip()
            if not aname: continue
            slug = (row.get('slug') or '').strip()
            addr = (row.get('app_address') or '').strip()
            rem = (row.get('remark') or '').strip()
            tok = str(row.get('use_token', '')).lower() in ['true', '1', 'yes']
            key = (row.get('api_key') or '').strip()
            sort = int(row.get('sort_order', 0))
            
            # Simple merge: add if not exists
            db_add_app(aname, slug, addr, rem, tok, key, sort)
            count += 1
        flash(f"成功匯入 {count} 筆應用程式", "success")
    except Exception as e:
        flash(f"匯入失敗: {e}", "danger")
    return redirect(PORTAL_PREFIX + '/admin/apps')

# ======================== ADMIN: CHAT HISTORY ========================

def _fetch_app_messages(api_key: str, app_slug: str, days: int, user_ids: list) -> list:
    """
    透過 Dify /v1/conversations 再 /v1/messages 分頁抓取指定天數內的問答紀錄。
    因 Dify API 強隔離 user，必須針對所有已知 user_id 逐一查詢。
    回傳 list[dict]，每筆含 query, answer, created_at, from_account_id, from_end_user_id, message_id。
    """
    import time
    from datetime import timezone

    cutoff_ts = time.time() - days * 86400
    results = []
    headers = {"Authorization": f"Bearer {api_key}"}
    api_base = "http://api:5001/v1"

    for uid in user_ids:
        # 步驟 1：取所有 conversations（分頁）
        conv_ids = []
        last_id = ""
        for _ in range(5):  # 每個 user 最多查 5 頁對話
            params = {"limit": 100, "user": uid}
            if last_id:
                params["last_id"] = last_id
            try:
                resp = requests.get(f"{api_base}/conversations", headers=headers, params=params, timeout=10)
                if resp.status_code != 200:
                    break
                data = resp.json()
                convs = data.get("data", [])
                if not convs:
                    break
                for c in convs:
                    # 如果對話的最後更新時間已經早於 cutoff_ts，可以提早跳過（Dify 返回依更新時間遞減排序）
                    if c.get("updated_at", 0) < cutoff_ts:
                        continue
                    conv_ids.append(c["id"])
                if not data.get("has_more"):
                    break
                last_id = convs[-1]["id"]
            except Exception:
                break

        # 步驟 2：對每個 conversation 抓 messages
        for conv_id in conv_ids:
            last_msg_id = ""
            for _ in range(5):  # 每個對話最多查 5 頁訊息
                params = {"conversation_id": conv_id, "limit": 50, "user": uid}
                if last_msg_id:
                    params["first_id"] = last_msg_id
                try:
                    resp = requests.get(f"{api_base}/messages", headers=headers, params=params, timeout=10)
                    if resp.status_code != 200:
                        break
                    data = resp.json()
                    msgs = data.get("data", [])
                    for m in msgs:
                        ct = m.get("created_at", 0)
                        if ct < cutoff_ts:
                            continue
                        
                        # 讀取 Dify 原生的評分 (如果有)
                        dify_fb = m.get("feedback")
                        dify_rating = dify_fb.get("rating") if dify_fb else None

                        results.append({
                            "message_id": m.get("id", ""),
                            "conversation_id": conv_id,
                            "query": m.get("query", ""),
                            "answer": clean_dify_answer(m.get("answer", "")),
                            "created_at": datetime.fromtimestamp(ct).strftime("%Y-%m-%d %H:%M:%S") if ct else "",
                            "from_account_id": uid, # Dify API 直接使用我們給的 user
                            "from_end_user_id": m.get("from_end_user_id", "") or "",
                            "rating": dify_rating,
                            "dislike_reason": "",
                            "app_name": "",
                            "app_slug": app_slug,
                        })
                    if not data.get("has_more"):
                        break
                    if msgs:
                        last_msg_id = msgs[-1]["id"]
                    else:
                        break
                except Exception:
                    break

    return results


def _get_all_known_userids() -> list:
    """取得系統中所有出現過的 user_id (包含手動建檔與透過 Token/Domain 登入的紀錄)"""
    conn = get_db_conn()
    userids = set()
    try:
        # 從 users 取得
        for r in conn.execute('SELECT userid FROM users').fetchall():
            userids.add(r['userid'])
        # 從 user_conversations 取得 (可能有未建檔但已對話的使用者)
        for r in conn.execute('SELECT userid FROM user_conversations').fetchall():
            userids.add(r['userid'])
        # 從 token_log 取得
        for r in conn.execute('SELECT userid FROM token_log').fetchall():
            userids.add(r['userid'])
    finally:
        conn.close()
    return list(userids)


@app.route(PORTAL_PREFIX + '/admin/chat_history')
@admin_required
def admin_chat_history():
    """問答歷史查詢頁面：跨所有已設 api_key 的 App，查詢指定天數內的問答。"""
    days = int(request.args.get('days', 3))
    app_slug = request.args.get('app_slug', '').strip()
    rating_filter = request.args.get('rating_filter', '').strip()
    user_filter = request.args.get('user_filter', '').strip()
    keyword = request.args.get('keyword', '').strip()

    available_apps = [a for a in db_get_all_apps(only_active=False) if a.get('api_key')]
    all_messages = []
    error = None

    target_apps = [a for a in available_apps if a['slug'] == app_slug] if app_slug else available_apps
    all_known_users = _get_all_known_userids()

    for target_app in target_apps:
        try:
            msgs = _fetch_app_messages(target_app['api_key'], target_app['slug'], days, all_known_users)
            for m in msgs:
                m['app_name'] = target_app['appname']
            all_messages.extend(msgs)
        except Exception as e:
            error = f"App [{target_app['appname']}] 查詢失敗: {e}"

    # 依時間降冪排序
    all_messages.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    # 補入本地 SQLite 的 feedback（rating + dislike reason）
    msg_ids = [m['message_id'] for m in all_messages if m.get('message_id')]
    local_fb = db_get_message_feedbacks(msg_ids)
    for m in all_messages:
        mid = m.get('message_id', '')
        if mid and mid in local_fb:
            # 本地紀錄優先 (因為含有不滿意原因)，若本地無評分才用 Dify 的
            if local_fb[mid].get('rating'):
                m['rating'] = local_fb[mid]['rating']
            m['dislike_reason'] = local_fb[mid].get('content', '')

    # 評分篩選
    if rating_filter == 'like':
        all_messages = [m for m in all_messages if m.get('rating') == 'like']
    elif rating_filter == 'dislike':
        all_messages = [m for m in all_messages if m.get('rating') == 'dislike']
    elif rating_filter == 'none':
        all_messages = [m for m in all_messages if not m.get('rating')]

    # 使用者篩選
    if user_filter:
        all_messages = [m for m in all_messages if user_filter.lower() in (m.get('from_account_id') or '').lower()]
    
    # 問題關鍵字篩選
    if keyword:
        all_messages = [m for m in all_messages if keyword.lower() in (m.get('query') or '').lower()]

    return render_template(
        'admin/chat_history.html',
        messages=all_messages,
        available_apps=available_apps,
        days=days,
        app_slug=app_slug,
        rating_filter=rating_filter,
        user_filter=user_filter,
        keyword=keyword,
        error=error,
        session=session,
        portal_prefix=PORTAL_PREFIX
    )


@app.route(PORTAL_PREFIX + '/admin/chat_history/export')
@admin_required
def export_chat_history():
    """將問答歷史匯出為 CSV（UTF-8 BOM，可直接以 Excel 開啟）。"""
    days = int(request.args.get('days', 3))
    app_slug = request.args.get('app_slug', '').strip()
    rating_filter = request.args.get('rating_filter', '').strip()
    user_filter = request.args.get('user_filter', '').strip()
    keyword = request.args.get('keyword', '').strip()

    available_apps = [a for a in db_get_all_apps(only_active=False) if a.get('api_key')]
    target_apps = [a for a in available_apps if a['slug'] == app_slug] if app_slug else available_apps
    all_messages = []
    all_known_users = _get_all_known_userids()

    for target_app in target_apps:
        try:
            msgs = _fetch_app_messages(target_app['api_key'], target_app['slug'], days, all_known_users)
            for m in msgs:
                m['app_name'] = target_app['appname']
            all_messages.extend(msgs)
        except Exception:
            pass

    all_messages.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    msg_ids = [m['message_id'] for m in all_messages if m.get('message_id')]
    local_fb = db_get_message_feedbacks(msg_ids)
    for m in all_messages:
        mid = m.get('message_id', '')
        if mid and mid in local_fb:
            if local_fb[mid].get('rating'):
                m['rating'] = local_fb[mid]['rating']
            m['dislike_reason'] = local_fb[mid].get('content', '')

    if rating_filter == 'like':
        all_messages = [m for m in all_messages if m.get('rating') == 'like']
    elif rating_filter == 'dislike':
        all_messages = [m for m in all_messages if m.get('rating') == 'dislike']
    elif rating_filter == 'none':
        all_messages = [m for m in all_messages if not m.get('rating')]

    if user_filter:
        all_messages = [m for m in all_messages if user_filter.lower() in (m.get('from_account_id') or '').lower()]
    if keyword:
        all_messages = [m for m in all_messages if keyword.lower() in (m.get('query') or '').lower()]

    si = StringIO()
    fieldnames = ['created_at', 'app_name', 'from_account_id', 'from_end_user_id', 'query', 'answer', 'rating', 'dislike_reason', 'message_id']
    cw = csv.DictWriter(si, fieldnames=fieldnames, extrasaction='ignore')
    cw.writeheader()
    for m in all_messages:
        cw.writerow({k: m.get(k, '') for k in fieldnames})
    output = si.getvalue().encode('utf-8-sig')
    filename = f"chat_history_{days}days.csv"
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename={filename}'})


# ======================== EXTERNAL API FOR DIFY ========================
@app.route('/api/v1/user-query', methods=['GET'])
def api_user_query():
    """
    提供給 Dify 工具呼叫的聯絡人查詢 API
    - q: 模糊搜尋
    - userid: 精確搜尋帳號
    - wechat: 精確搜尋 WeChat
    """
    # 簡單金鑰驗證 (如有環境變數 SYSTEM_API_KEY 才啟用)
    api_key = os.environ.get('SYSTEM_API_KEY')
    if api_key:
        auth_header = request.headers.get('Authorization', '')
        if auth_header != f"Bearer {api_key}" and request.args.get('api_key') != api_key:
            return jsonify({"error": "Unauthorized"}), 401
            
    query = request.args.get('q', '').strip()
    userid = request.args.get('userid', '').strip()
    wechat = request.args.get('wechat', '').strip()
    
    conn = get_db_conn()
    data = []
    
    try:
        if userid:
            # userID 精確搜尋 (忽略大小寫)
            row = conn.execute('SELECT userid, username, phone, ext, email, wechat, remark, is_active FROM users WHERE userid LIKE ?', (userid,)).fetchone()
            if row: data.append(dict(row))
        elif wechat:
            # wechat 精確搜尋
            rows = conn.execute('SELECT userid, username, phone, ext, email, wechat, remark, is_active FROM users WHERE wechat LIKE ?', (wechat,)).fetchall()
            for r in rows: data.append(dict(r))
        elif query:
            # 模糊搜尋
            like_q = f'%{query}%'
            rows = conn.execute('''
                SELECT userid, username, phone, ext, email, wechat, remark, is_active 
                FROM users 
                WHERE userid LIKE ? OR username LIKE ? OR phone LIKE ? OR ext LIKE ? OR wechat LIKE ? OR email LIKE ?
            ''', (like_q, like_q, like_q, like_q, like_q, like_q)).fetchall()
            for r in rows: data.append(dict(r))
    finally:
        conn.close()
        
    return jsonify({
        "status": "success",
        "count": len(data),
        "data": data
    })

@app.route('/api/v1/sql-query', methods=['POST'])
def api_sql_query():
    """
    提供給 Dify LLM 執行 SQL 查詢（限 SELECT 語句，僅限 users 資料表）
    Body: { "sql": "SELECT ... FROM users WHERE ..." }
    """
    # 簡單金鑰驗證 (如有環境變數 SYSTEM_API_KEY 才啟用)
    api_key = os.environ.get('SYSTEM_API_KEY')
    if api_key:
        auth_header = request.headers.get('Authorization', '')
        if auth_header != f"Bearer {api_key}":
            return jsonify({"error": "Unauthorized"}), 401
            
    body = request.get_json(silent=True) or {}
    sql = body.get('sql', '').strip()
    
    # 安全白名單驗證
    sql_upper = sql.upper()
    if not sql_upper.startswith('SELECT'):
        return jsonify({"error": "Only SELECT statements are allowed"}), 400
    for forbidden in ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'ATTACH']:
        if forbidden in sql_upper:
            return jsonify({"error": f"Forbidden keyword: {forbidden}"}), 400
    
    conn = get_db_conn()
    data = []
    try:
        rows = conn.execute(sql).fetchall()
        data = [dict(r) for r in rows]
        return jsonify({"status": "success", "count": len(data), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    ensure_data_dir()
    init_users_db()
    app.run(host='0.0.0.0', port=5050, debug=True)
