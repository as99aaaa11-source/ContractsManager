import streamlit as st
import sqlite3
from datetime import datetime

# ضبط إعدادات الصفحة
st.set_page_config(page_title="نظام إدارة العقود", layout="wide")

# --- 1. إنشاء/الاتصال بقاعدة البيانات ---
DB_NAME = "contracts_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            contract_date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            completed_at TEXT,
            duration TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# دوال التعامل مع قاعدة البيانات
def add_contract_to_db(name, unit, contract_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO contracts (name, unit, contract_date, created_at, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (name, unit, str(contract_date), created_at))
    conn.commit()
    conn.close()

def get_contracts_from_db(status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, unit, contract_date, created_at, completed_at, duration
        FROM contracts WHERE status = ? ORDER BY id DESC
    """, (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def complete_contract_in_db(contract_id, duration):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE contracts 
        SET status = 'completed', completed_at = ?, duration = ?
        WHERE id = ?
    """, (completed_at, duration, contract_id))
    conn.commit()
    conn.close()

# دالة لحساب الوقت المنقضي
def calculate_elapsed_time(start_time_str):
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    diff = now - start_time
    
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} يوم")
    if hours > 0:
        time_parts.append(f"{hours} ساعة")
    if minutes > 0:
        time_parts.append(f"{minutes} دقيقة")
    time_parts.append(f"{seconds} ثانية")
    
    return " و ".join(time_parts)

# --- 2. الخلفية والتنسيقات CSS ---
background_image_url = "https://i.postimg.cc/C51pKGdK/Whats-App-Image-2026-09-27-at-12-42-52.jpg"

base_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}
.stMarkdown, h1, h2, h3, h4, h5, h6, p, label {{
    color: #ffffff !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}}

/* تصميم كارت خلفية شفاف للعنوان والنصوص العلوية */
.header-box {{
    background-color: rgba(0, 0, 0, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    text-align: center;
}}

/* تصميم حاوية خلفية القائمة الرئيسية الشفافة للأزرار */
.menu-box {{
    background-color: rgba(15, 15, 15, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 16px;
    padding: 25px 30px;
    box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
}}

.contract-card {{
    background-color: rgba(20, 20, 20, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    text-align: right;
}}
.badge-pending {{
    background-color: #ff9800;
    color: #fff;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: bold;
}}
.badge-completed {{
    background-color: #4caf50;
    color: #fff;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: bold;
}}
.inline-badge {{
    background-color: rgba(0, 0, 0, 0.65);
    border: 1.5px solid #ff9800;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 1.1rem;
    font-weight: bold;
    display: inline-block;
    color: #ffeb3b !important;
}}
</style>
"""

st.markdown(base_css, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "welcome"

# --- 3. التنقل بين الصفحات ---

# 1. الصفحة الترحيبية
if st.session_state.page == "welcome":
    st.markdown("""
    <div class="header-box" style="margin-top: 80px;">
        <h1 style="margin: 0;">أهلاً بك في نظام إدارة العقود</h1>
        <h4 style="margin-top: 10px;">المنصة الإلكترونية لمتابعة وتسجيل حالة العقود </h4>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 الدخول للبرنامج", use_container_width=True):
            st.session_state.page = "main_menu"
            st.rerun()

# 2. القائمة الرئيسية (تم وضع خلفية شفافة للعنوان وللأزرار)
elif st.session_state.page == "main_menu":
    # خلفية شفافة للعنوان الرئيسي العلوي
    st.markdown("""
    <div class="header-box">
        <h1 style="margin: 0;">📑 القائمة الرئيسية</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # خلفية شفافة للحاوية الخاصة بالأزرار والنصوص
        st.markdown('<div class="menu-box">', unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>اختر الصفحة التي تريد الانتقال إليها:</h3>", unsafe_allow_html=True)
        
        if st.button("📝 تسجيل عقد جديد", use_container_width=True, type="primary"):
            st.session_state.page = "add_contract"
            st.rerun()
            
        st.write("")
        if st.button("⏳ العقود غير المكتملة", use_container_width=True):
            st.session_state.page = "pending_contracts"
            st.rerun()
            
        st.write("")
        if st.button("✅ العقود المكتملة", use_container_width=True):
            st.session_state.page = "completed_contracts"
            st.rerun()

        st.write("---")
        if st.button("← العودة للشاشة الترحيبية", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# 3. صفحة تسجيل عقد جديد
elif st.session_state.page == "add_contract":
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { direction: rtl; text-align: right; }
    .stMarkdown, h1, h2, h3, h4, h5, h6, p, label, .stTextInput label, .stDateInput label { text-align: right !important; }
    input { text-align: right !important; direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

    col_title, col_back = st.columns([5, 1])
    with col_title:
        st.markdown('<div class="header-box" style="text-align: right;"><h1 style="margin:0;">📝 تسجيل بيانات العقد الجديد</h1></div>', unsafe_allow_html=True)
    with col_back:
        if st.button("رجوع للقائمة ←"):
            st.session_state.page = "main_menu"
            st.rerun()

    st.write("---")

    with st.form("add_contract_form", clear_on_submit=True):
        name = st.text_input("الاسم الرباعي:")
        unit = st.text_input("كود الوحدة:")
        contract_date = st.date_input("تاريخ العقد:")
        
        submit = st.form_submit_button("حفظ العقد")
        if submit:
            if name.strip() and unit.strip():
                add_contract_to_db(name, unit, contract_date)
                st.success("تم حفظ العقد بنجاح في قاعدة البيانات!")
            else:
                st.error("يرجى إدخال كافة البيانات المطلوبة!")

# 4. صفحة العقود غير المكتملة
elif st.session_state.page == "pending_contracts":
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

    @st.fragment(run_every=1)
    def render_pending_page():
        pending_contracts = get_contracts_from_db('pending')
        total_pending = len(pending_contracts)

        col_header, col_back = st.columns([5, 1])
        with col_header:
            st.markdown(f"""
            <div class="header-box" style="display: flex; align-items: center; justify-content: space-between; margin-bottom:0;">
                <h1 style="margin: 0;">⏳ قائمة العقود غير المكتملة</h1>
                <div class="inline-badge">📊 إجمالي العقود: {total_pending}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_back:
            if st.button("رجوع للقائمة ←"):
                st.session_state.page = "main_menu"
                st.rerun()

        st.write("---")

        if not pending_contracts:
            st.info("لا توجد عقود غير مكتملة حالياً.")
        else:
            for item in pending_contracts:
                c_id, name, unit, contract_date, created_at, _, _ = item
                elapsed_time = calculate_elapsed_time(created_at)
                
                st.markdown(f"""
                <div class="contract-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin:0; color: #ffeb3b !important;">👤 {name}</h3>
                        <span class="badge-pending">⏳ قيد الانتظار</span>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                    <p style="margin: 5px 0;">🏢 <b>كود الوحدة:</b> {unit} | 📅 <b>تاريخ العقد:</b> {contract_date}</p>
                    <p style="margin: 5px 0; color: #00e676 !important;">⏱️ <b>الوقت المنقضي حتى الآن:</b> {elapsed_time}</p>
                    <p style="margin: 5px 0; font-size: 0.85rem; opacity: 0.8;">🕒 وقت الإضافة: {created_at}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_right, col_btn = st.columns([4, 1])
                with col_btn:
                    if st.button("✍️ تم إمضاء العقد", key=f"btn_{c_id}"):
                        complete_contract_in_db(c_id, elapsed_time)
                        st.success("تم نقل العقد إلى قائمة العقود المكتملة!")
                        st.rerun()
                st.write("")

    render_pending_page()

# 5. صفحة العقود المكتملة
elif st.session_state.page == "completed_contracts":
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

    completed_contracts = get_contracts_from_db('completed')
    total_completed = len(completed_contracts)

    col_header, col_back = st.columns([5, 1])
    with col_header:
        st.markdown(f"""
        <div class="header-box" style="display: flex; align-items: center; justify-content: space-between; margin-bottom:0;">
            <h1 style="margin: 0;">✅ قائمة العقود المكتملة</h1>
            <div class="inline-badge" style="border-color: #4caf50; color: #4caf50 !important;">📊 إجمالي العقود المكتملة: {total_completed}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_back:
        if st.button("رجوع للقائمة ←"):
            st.session_state.page = "main_menu"
            st.rerun()

    st.write("---")

    if not completed_contracts:
        st.info("لا توجد عقود مكتملة حتى الآن.")
    else:
        for item in completed_contracts:
            c_id, name, unit, contract_date, created_at, completed_at, duration = item
            st.markdown(f"""
            <div class="contract-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin:0; color: #4caf50 !important;">✅ {name}</h3>
                    <span class="badge-completed">مكتمل</span>
                </div>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                <p style="margin: 5px 0;">🏢 <b>كود الوحدة:</b> {unit} | 📅 <b>تاريخ العقد:</b> {contract_date}</p>
                <p style="margin: 5px 0; color: #00e676 !important;">⏱️ <b>إجمالي وقت الإنجاز:</b> {duration}</p>
                <p style="margin: 5px 0; font-size: 0.85rem; opacity: 0.8;">✍️ وقت الإمضاء: {completed_at}</p>
            </div>
            """, unsafe_allow_html=True)