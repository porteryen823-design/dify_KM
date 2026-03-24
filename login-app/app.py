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
USERS_FILE = os.path.join(DATA_DIR, 'users.json')   # legacy, used only for migration
USERS_DB   = os.path.join(DATA_DIR, 'users.db')     # SQLite DB
APPS_FILE = os.path.join(DATA_DIR, 'apps.json')
TOKEN_LOG_FILE = os.path.join(DATA_DIR, 'token_log.json')

# In-memory token store: token -> entry dict
_token_store: dict = {}

# ======================== HELPERS ========================

def get_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ---- SQLite user DB helpers ----

def get_db_conn():
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
            sort_order  INTEGER DEFAULT 0,
            is_active   INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT ''
        )
    ''')
    conn.commit()

    # Migration: Users
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0 and os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                old_users = json.load(f)
            for u in old_users:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cur.execute(
                    'INSERT OR IGNORE INTO users (userid, username, pwd, remark, is_admin, is_active, created_at) VALUES (?,?,?,?,?,?,?)',
                    (u.get('userid'), u.get('username'), u.get('pwd'), u.get('remark',''),
                     1 if u.get('is_admin') else 0, 1, now)
                )
            conn.commit()
            app.logger.info('Migrated users.json -> users.db')
        except Exception as exc:
            app.logger.warning(f'User migration skipped: {exc}')

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
                    'INSERT INTO apps (appname, slug, app_address, remark, use_token, sort_order, created_at) VALUES (?,?,?,?,?,?,?)',
                    (a.get('appname'), a.get('slug',''), a.get('app_address'), a.get('remark',''),
                     1 if a.get('use_token') else 0, i*10, now)
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
                    'INSERT INTO apps (appname, slug, app_address, remark, use_token, sort_order, created_at) VALUES (?,?,?,?,?,?,?)',
                    (name, slug, addr, rem, tok, i*10, now)
                )
            conn.commit()
            app.logger.info('Seed apps inserted.')

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

def db_add_user(userid, username, pwd_plain, remark, is_admin):
    hashed = get_hash(pwd_plain)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    try:
        conn.execute(
            'INSERT INTO users (userid, username, pwd, remark, is_admin, is_active, created_at) VALUES (?,?,?,?,?,1,?)',
            (userid, username, hashed, remark, 1 if is_admin else 0, now)
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

def db_update_user(userid, username, remark, is_admin, is_active):
    conn = get_db_conn()
    conn.execute(
        'UPDATE users SET username=?, remark=?, is_admin=?, is_active=? WHERE userid=?',
        (username, remark, 1 if is_admin else 0, 1 if is_active else 0, userid)
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

def db_get_app(app_id: int):
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM apps WHERE id=?', (app_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def db_get_app_by_slug(slug: str):
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM apps WHERE slug=?', (slug,)).fetchone()
    conn.close()
    return dict(row) if row else None

def db_add_app(appname, slug, app_address, remark, use_token, sort_order=0):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_conn()
    cur = conn.execute(
        'INSERT INTO apps (appname, slug, app_address, remark, use_token, sort_order, created_at) VALUES (?,?,?,?,?,?,?)',
        (appname, slug, app_address, remark, 1 if use_token else 0, sort_order, now)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def db_update_app(app_id, appname, slug, app_address, remark, use_token, sort_order, is_active):
    conn = get_db_conn()
    conn.execute(
        'UPDATE apps SET appname=?, slug=?, app_address=?, remark=?, use_token=?, sort_order=?, is_active=? WHERE id=?',
        (appname, slug, app_address, remark, 1 if use_token else 0, sort_order, 1 if is_active else 0, app_id)
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

def generate_access_token(userid: str, username: str, appname: str) -> str:
    """Generate a UUID token and persist to token_log.json."""
    token = uuid.uuid4().hex  # 32-char hex string
    entry = {
        "token": token,
        "userid": userid,
        "username": username,
        "appname": appname,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    _token_store[token] = entry
    # Persist (keep last 2000 records)
    logs = read_json(TOKEN_LOG_FILE)
    if not isinstance(logs, list):
        logs = []
    logs.insert(0, entry)
    trimmed: list = logs[:2000]
    write_json(TOKEN_LOG_FILE, trimmed)
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
        hashed_pwd = get_hash(pwd)

        users = db_get_all_users()
        user = next((u for u in users if u.get('userid') == userid
                     and u.get('pwd') == hashed_pwd
                     and u.get('is_active', 1)), None)

        if user:
            session['userid'] = user['userid']
            session['username'] = user['username']
            session['is_admin'] = bool(user.get('is_admin', False))
            return redirect(PORTAL_PREFIX + '/embedded_chat')
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
    conversation_id = data.get('conversation_id', '')
    userid = session.get('userid', 'unknown')

    api_url = "http://api:5001/v1/chat-messages"
    api_key = "app-acUsw5zh3rZRqXrUJxyQ5v4d"

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
        
        # Clean <think> tags from deepseek or other reasoning models if present
        import re
        answer_text = re.sub(r'<think>.*?</think>\s*', '', answer_text, flags=re.DOTALL)

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
    api_key = "app-acUsw5zh3rZRqXrUJxyQ5v4d"
    
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
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Error sending Dify feedback: {e}")
        return jsonify({"error": str(e)}), 500

@app.route(PORTAL_PREFIX + '/logout')
def logout():
    session.clear()
    return redirect(PORTAL_PREFIX + '/login')

@app.route(PORTAL_PREFIX + '/apps')
@login_required
def apps_list():
    apps = db_get_all_apps(only_active=True)
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
    
    sep = '&' if '?' in path else '?'
    # 還原：使用 Dify 最原始支援的 user 參數，這會自動填入 Dify 的系統變數 sys.user_id
    final_path = f"{path}{sep}user={userid}"
    
    # Redirect to the embedded chat UI
    return redirect(url_for('embedded_chat'), code=302)

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
    logs = read_json(TOKEN_LOG_FILE)
    return render_template('admin/token_log.html', logs=logs, session=session, portal_prefix=PORTAL_PREFIX)

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
            is_admin = request.form.get('is_admin') == 'on'
            ok, err = db_add_user(userid, username, pwd, remark, is_admin)
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
            is_admin = request.form.get('is_admin') == 'on'
            is_active = request.form.get('is_active') == 'on'
            db_update_user(uid, username, remark, is_admin, is_active)
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
    cw = csv.DictWriter(si, fieldnames=['userid', 'username', 'remark', 'is_admin', 'is_active', 'created_at'])
    cw.writeheader()
    for u in users:
        cw.writerow({k: u.get(k, '') for k in ['userid', 'username', 'remark', 'is_admin', 'is_active', 'created_at']})
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
                               row.get('remark', existing['remark']), is_admin, is_active)
            else:
                pwd_raw = row.get('pwd', 'changeme')
                db_add_user(uid, row.get('username', uid).strip(), pwd_raw,
                            row.get('remark', ''), is_admin)
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
            sort = int(request.form.get('sort_order', 0))
            db_add_app(app_name, slug, addr, rem, tok, sort)
            flash("新增應用程式成功", "success")
        elif action == 'edit':
            aid = int(request.form.get('id'))
            app_name = request.form.get('appname', '').strip()
            slug = request.form.get('slug', '').strip()
            addr = request.form.get('app_address', '').strip()
            rem = request.form.get('remark', '')
            tok = request.form.get('use_token') == 'on'
            sort = int(request.form.get('sort_order', 0))
            active = request.form.get('is_active') == 'on'
            db_update_app(aid, app_name, slug, addr, rem, tok, sort, active)
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
    cw = csv.DictWriter(si, fieldnames=['id', 'appname', 'slug', 'app_address', 'remark', 'use_token', 'sort_order', 'is_active', 'created_at'])
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
            aname = row.get('appname', '').strip()
            if not aname: continue
            slug = row.get('slug', '').strip()
            addr = row.get('app_address', '').strip()
            rem = row.get('remark', '')
            tok = str(row.get('use_token', '')).lower() in ['true', '1', 'yes']
            sort = int(row.get('sort_order', 0))
            
            # Simple merge: add if not exists
            db_add_app(aname, slug, addr, rem, tok, sort)
            count += 1
        flash(f"成功匯入 {count} 筆應用程式", "success")
    except Exception as e:
        flash(f"匯入失敗: {e}", "danger")
    return redirect(PORTAL_PREFIX + '/admin/apps')

if __name__ == '__main__':
    ensure_data_dir()
    init_users_db()
    app.run(host='0.0.0.0', port=5050, debug=True)
