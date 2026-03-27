import sqlite3
import os

USERS_DB = r'c:\VSCode_Proj\Dify\login-app\data\users.db'

def update_test_data():
    conn = sqlite3.connect(USERS_DB)
    cur = conn.cursor()
    
    # Add columns if not exist (redundant but safe)
    contact_fields = ["phone", "ext", "email", "wechat"]
    for field in contact_fields:
        try:
            cur.execute(f'ALTER TABLE users ADD COLUMN {field} TEXT DEFAULT ""')
        except sqlite3.OperationalError:
            pass
            
    # Update existing test users
    test_data = {
        'A123': ('0912345678', '101', 'a123@example.com', 'wechat_a123'),
        'B123': ('0922345678', '102', 'b123@example.com', 'wechat_b123'),
        'C123': ('0932345678', '103', 'c123@example.com', 'wechat_c123'),
        'admin': ('', '', 'admin@example.com', '')
    }
    
    for uid, (phone, ext, email, wechat) in test_data.items():
        cur.execute('''
            UPDATE users 
            SET phone=?, ext=?, email=?, wechat=? 
            WHERE userid=?
        ''', (phone, ext, email, wechat, uid))
        
    conn.commit()
    print("Test data updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_test_data()
