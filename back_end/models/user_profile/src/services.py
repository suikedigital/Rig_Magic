import json
from src.database import get_connection
from src.models import BaseUser, TradeUser, CustomerUser

def save_user(user: BaseUser):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT OR REPLACE INTO users (user_id, role, yacht_ids, telephone, address, subscription_status, payment_info, company_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user.user_id,
        user.role,
        json.dumps(user.yacht_ids),
        user.telephone,
        json.dumps(user.address.dict()) if user.address else None,
        user.subscription_status,
        json.dumps(user.payment_info.dict()) if user.payment_info else None,
        getattr(user, 'company_name', None)
    ))
    conn.commit()
    conn.close()

def get_user(user_id: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None

    data = dict(row)
    data['yacht_ids'] = json.loads(data['yacht_ids']) if data['yacht_ids'] else []
    data['address'] = json.loads(data['address']) if data['address'] else None
    data['payment_info'] = json.loads(data['payment_info']) if data['payment_info'] else None

    if data['role'] == 'trade':
        return TradeUser(**data)
    else:
        return CustomerUser(**data)

def list_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    users = []
    for row in rows:
        data = dict(row)
        data['yacht_ids'] = json.loads(data['yacht_ids']) if data['yacht_ids'] else []
        data['address'] = json.loads(data['address']) if data['address'] else None
        data['payment_info'] = json.loads(data['payment_info']) if data['payment_info'] else None
        if data['role'] == 'trade':
            users.append(TradeUser(**data))
        else:
            users.append(CustomerUser(**data))
    return users
