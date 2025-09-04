import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import uuid
from datetime import datetime, timedelta
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="IT Ticketing System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, human-friendly design
st.markdown("""
<style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Custom font family */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Modern, clean header */
    .main-header {
        background: white;
        color: #1f2937;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border-bottom: 3px solid #3b82f6;
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: #3b82f6;
        border-radius: 2px;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.03em;
        color: #111827;
        background: linear-gradient(135deg, #1f2937 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 1rem 0 0 0;
        color: #6b7280;
        font-weight: 400;
    }
    
    /* Clean sidebar styling */
    .css-1d391kg {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
        margin-bottom: 0.5rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Clean form styling */
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    
    .stTextInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Remove ALL default browser focus outlines and styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stTextInput > div > div > input:focus,
    .stTextInput > div > div > input:focus-visible,
    .stTextInput > div > div > input:active,
    .stTextArea > div > div > textarea:focus,
    .stTextArea > div > div > textarea:focus-visible,
    .stTextArea > div > div > textarea:active,
    /* Target Streamlit input containers */
    .stTextInput > div,
    .stTextInput > div > div,
    .stTextArea > div,
    .stTextArea > div > div,
    .stSelectbox > div,
    .stSelectbox > div > div {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Clean focus styling - only blue border on input itself */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 1px solid #3b82f6 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Ensure no red validation styling */
    .stTextInput > div > div > input:invalid,
    .stTextArea > div > div > textarea:invalid {
        border: 1px solid #d1d5db !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Modern alert styling */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: none;
        color: #155724;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(21, 87, 36, 0.1);
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: none;
        color: #721c24;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(114, 28, 36, 0.1);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: none;
        color: #0c5460;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(12, 84, 96, 0.1);
    }
    
    /* Clean metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        border-radius: 12px 12px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    /* Clean ticket cards */
    .ticket-card {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .ticket-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        width: 3px;
        background: #3b82f6;
        border-radius: 0 2px 2px 0;
    }
    
    .ticket-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Clean status badges */
    .status-open { 
        background: #10b981; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-in-progress { 
        background: #f59e0b; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-pending { 
        background: #3b82f6; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-resolved { 
        background: #6b7280; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-closed { 
        background: #374151; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Clean priority badges */
    .priority-low { 
        background: #10b981; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .priority-medium { 
        background: #f59e0b; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .priority-high { 
        background: #f97316; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .priority-critical { 
        background: #ef4444; 
        color: white; 
        padding: 0.4rem 0.8rem; 
        border-radius: 6px; 
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Clean expander styling */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.5rem;
    }
    
    .streamlit-expanderContent {
        background: white;
        border-radius: 0 0 8px 8px;
        border: 1px solid #e5e7eb;
        border-top: none;
        padding: 1.25rem;
    }
    
    /* Login page styling */
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid #f1f5f9;
    }
    
    /* Clean sidebar header */
    .css-1d391kg .css-1v0mbdj {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    /* Compact sidebar styling */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Make logout button look like text */
    .stButton > button[data-testid="baseButton-secondary"][aria-label="Click to logout"] {
        background: transparent;
        color: #ef4444;
        border: none;
        box-shadow: none;
        font-weight: 400;
        padding: 0.25rem 0.5rem;
        margin: 0;
    }
    
    .stButton > button[data-testid="baseButton-secondary"][aria-label="Click to logout"]:hover {
        background: #fef2f2;
        color: #dc2626;
        transform: none;
        box-shadow: none;
    }
    
    /* Reduce button spacing */
    .stButton > button {
        margin-bottom: 0.25rem;
    }
    
    /* Red delete button styling - more specific */
    div[data-testid="column"] .stButton > button[data-testid="baseButton-primary"] {
        background: #ef4444 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2) !important;
    }
    
    div[data-testid="column"] .stButton > button[data-testid="baseButton-primary"]:hover {
        background: #dc2626 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'it_staff', 'user')),
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Priorities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS priorities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            level INTEGER UNIQUE NOT NULL,
            color TEXT NOT NULL
        )
    ''')
    
    # Statuses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_number TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status_id INTEGER,
            priority_id INTEGER,
            category_id INTEGER,
            requester_id INTEGER,
            assignee_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            sla_response_due TIMESTAMP,
            sla_resolution_due TIMESTAMP,
            first_response_at TIMESTAMP,
            escalated_at TIMESTAMP,


            FOREIGN KEY (status_id) REFERENCES statuses(id),
            FOREIGN KEY (priority_id) REFERENCES priorities(id),
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (requester_id) REFERENCES users(id),
            FOREIGN KEY (assignee_id) REFERENCES users(id)
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            is_internal BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Time tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            description TEXT,
            time_spent_minutes INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    

    # Knowledge base table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            category_id INTEGER,
            tags TEXT,
            is_public BOOLEAN DEFAULT TRUE,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Insert default data
    cursor.execute('''
        INSERT OR IGNORE INTO categories (name, description) VALUES 
        ('Hardware', 'Issues related to computer hardware, printers, etc.'),
        ('Software', 'Software installation, configuration, or bugs'),
        ('Network', 'Network connectivity and infrastructure issues'),
        ('Email', 'Email client and server issues'),
        ('Security', 'Security-related concerns and access issues'),
        ('Account', 'User account management and access'),
        ('Other', 'Miscellaneous issues')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO priorities (name, level, color) VALUES 
        ('Low', 1, '#10B981'),
        ('Medium', 2, '#F59E0B'),
        ('High', 3, '#EF4444'),
        ('Critical', 4, '#DC2626')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO statuses (name, description) VALUES 
        ('Open', 'New ticket awaiting assignment'),
        ('In Progress', 'Ticket is being worked on'),
        ('Pending User', 'Waiting for user response'),
        ('Pending Vendor', 'Waiting for vendor response'),
        ('Resolved', 'Issue has been resolved'),
        ('Closed', 'Ticket is closed')
    ''')
    
    # Create demo users for all roles
    admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
    it_staff_password = hashlib.sha256('itstaff123'.encode()).hexdigest()
    user_password = hashlib.sha256('user123'.encode()).hexdigest()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, email, full_name, role, department) 
        VALUES 
        ('admin', ?, 'admin@company.com', 'Admin User', 'admin', 'IT'),
        ('itstaff', ?, 'itstaff@company.com', 'IT Staff User', 'it_staff', 'IT'),
        ('user', ?, 'user@company.com', 'Regular User', 'user', 'Sales')
    ''', (admin_password, it_staff_password, user_password))
    

    
    # Insert default knowledge base entries (only if they don't exist)
    cursor.execute('''
        INSERT OR IGNORE INTO knowledge_base (title, content, category_id, tags, created_by) VALUES 
        ('How to Reset Your Password', 'To reset your password:\n1. Go to the login page\n2. Click "Forgot Password"\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link and create a new password', 6, 'password,reset,login', 1),
        ('Common Printer Issues', 'Common printer problems and solutions:\n\n1. Printer not responding:\n   - Check power and USB connections\n   - Restart the printer\n   - Reinstall printer drivers\n\n2. Print quality issues:\n   - Clean print heads\n   - Replace ink/toner cartridges\n   - Check paper quality', 1, 'printer,hardware,troubleshooting', 1),
        ('VPN Connection Guide', 'How to connect to company VPN:\n\n1. Download VPN client from IT portal\n2. Install and launch the application\n3. Enter your credentials\n4. Select appropriate server location\n5. Click Connect\n\nIf issues persist, contact IT support.', 3, 'vpn,network,remote', 1)
    ''')
    
    # Clean up any existing duplicate knowledge base entries
    cursor.execute('''
        DELETE FROM knowledge_base 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM knowledge_base 
            GROUP BY title
        )
    ''')
    

    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def authenticate_user(username, password):
    """Authenticate a user and return user data if successful"""
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, role, department 
        FROM users WHERE username = ? AND password_hash = ?
    ''', (username, hash_password(password)))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[3],
            'role': user[4],
            'department': user[5]
        }
    return None

def generate_ticket_number():
    """Generate a unique ticket number"""
    return f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

def calculate_sla_dates(priority_id):
    """Calculate SLA response and resolution due dates based on priority"""
    now = datetime.now()
    
    # SLA rules (in hours)
    sla_rules = {
        1: {'response': 24, 'resolution': 72},  # Low
        2: {'response': 8, 'resolution': 24},   # Medium  
        3: {'response': 4, 'resolution': 12},   # High
        4: {'response': 1, 'resolution': 4}     # Critical
    }
    
    if priority_id in sla_rules:
        response_hours = sla_rules[priority_id]['response']
        resolution_hours = sla_rules[priority_id]['resolution']
        
        response_due = now + timedelta(hours=response_hours)
        resolution_due = now + timedelta(hours=resolution_hours)
        
        return response_due, resolution_due
    
    return None, None

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('tickets.db')

# Initialize database
init_database()

# Session state management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

def login_page():
    """Display login page"""
    st.title("IT Ticketing System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"  # Always go to dashboard after login
                    st.success(f"Welcome, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("---")
        st.info("**Demo Credentials:**")
        
        # Create horizontal layout for demo credentials
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Admin Account:**
            - Username: `admin`
            - Password: `admin123`
            - Access: Full system control, user management, all tickets
            """)
        
        with col2:
            st.markdown("""
            **IT Staff Account:**
            - Username: `itstaff`
            - Password: `itstaff123`
            - Access: All tickets, time tracking, reports (no user management)
            """)
        
        with col3:
            st.markdown("""
            **Regular User Account:**
            - Username: `user`
            - Password: `user123`
            - Access: Create tickets, view own tickets, knowledge base
            """)

def dashboard_page():
    """Display main dashboard"""
    user = st.session_state.user
    
    # Styled header
    st.markdown(f"""
    <div class="main-header">
        <h1>IT Ticketing System</h1>
        <p>Welcome back, <strong>{user['full_name']}</strong>! ({user['role'].title()})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        # Compact navigation header
        st.markdown("### Navigation")
        
        # Navigation buttons with smaller spacing
        if user['role'] in ['admin', 'it_staff']:
            if st.button("Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            if st.button("All Tickets", use_container_width=True):
                st.session_state.page = "tickets"
                st.rerun()
            if st.button("Create Ticket", use_container_width=True):
                st.session_state.page = "create_ticket"
                st.rerun()
            if st.button("Knowledge Base", use_container_width=True):
                st.session_state.page = "knowledge_base"
                st.rerun()

            if st.button("Time Tracking", use_container_width=True):
                st.session_state.page = "time_tracking"
                st.rerun()
            if user['role'] == 'admin':
                if st.button("User Management", use_container_width=True):
                    st.session_state.page = "user_management"
                    st.rerun()
            if st.button("Reports", use_container_width=True):
                st.session_state.page = "reports"
                st.rerun()
            if st.button("Profile", use_container_width=True):
                st.session_state.page = "profile"
                st.rerun()
        else:
            if st.button("Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            if st.button("My Tickets", use_container_width=True):
                st.session_state.page = "my_tickets"
                st.rerun()
            if st.button("Create Ticket", use_container_width=True):
                st.session_state.page = "create_ticket"
                st.rerun()
            if st.button("Knowledge Base", use_container_width=True):
                st.session_state.page = "knowledge_base"
                st.rerun()
            if st.button("Profile", use_container_width=True):
                st.session_state.page = "profile"
                st.rerun()
        
        # Set current page based on session state
        page = st.session_state.get('page', 'dashboard')
        
        # Compact logout as clickable text
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Logout", key="logout_text", help="Click to logout"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
    
    # Route to appropriate page
    if page == "dashboard":
        show_dashboard()
    elif page == "tickets" or page == "my_tickets":
        if 'selected_ticket' in st.session_state:
            show_ticket_detail(st.session_state.selected_ticket)
        elif 'edit_ticket' in st.session_state:
            show_edit_ticket(st.session_state.edit_ticket)
        else:
            show_tickets_list()
    elif page == "create_ticket":
        show_create_ticket()
    elif page == "knowledge_base":
        show_knowledge_base()

    elif page == "time_tracking" and user['role'] in ['admin', 'it_staff']:
        show_time_tracking()
    elif page == "user_management" and user['role'] == 'admin':
        show_user_management()
    elif page == "reports" and user['role'] in ['admin', 'it_staff']:
        show_reports()
    elif page == "profile":
        show_profile()

def show_dashboard():
    """Show dashboard with statistics"""
    user = st.session_state.user
    
    # Get statistics
    conn = get_db_connection()
    
    # Total tickets
    if user['role'] == 'user':
        total_tickets = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM tickets WHERE requester_id = ?", 
            conn, params=(user['id'],)
        ).iloc[0]['count']
    else:
        total_tickets = pd.read_sql_query("SELECT COUNT(*) as count FROM tickets", conn).iloc[0]['count']
    
    # Status breakdown
    if user['role'] == 'user':
        status_data = pd.read_sql_query('''
            SELECT s.name, COUNT(t.id) as count
            FROM statuses s
            LEFT JOIN tickets t ON s.id = t.status_id AND t.requester_id = ?
            GROUP BY s.id, s.name
            ORDER BY s.id
        ''', conn, params=(user['id'],))
    else:
        status_data = pd.read_sql_query('''
            SELECT s.name, COUNT(t.id) as count
            FROM statuses s
            LEFT JOIN tickets t ON s.id = t.status_id
            GROUP BY s.id, s.name
            ORDER BY s.id
        ''', conn)
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tickets", total_tickets)
    
    with col2:
        open_data = status_data[status_data['name'] == 'Open']
        open_tickets = open_data['count'].iloc[0] if len(open_data) > 0 else 0
        st.metric("Open Tickets", open_tickets)
    
    with col3:
        in_progress_data = status_data[status_data['name'] == 'In Progress']
        in_progress = in_progress_data['count'].iloc[0] if len(in_progress_data) > 0 else 0
        st.metric("In Progress", in_progress)
    
    with col4:
        resolved_data = status_data[status_data['name'] == 'Resolved']
        resolved = resolved_data['count'].iloc[0] if len(resolved_data) > 0 else 0
        st.metric("Resolved", resolved)
    
    # SLA Alerts
    if user['role'] in ['admin', 'it_staff']:
        st.subheader("SLA Alerts")
        
        # Get tickets with SLA violations
        sla_query = '''
            SELECT t.ticket_number, t.title, t.sla_response_due, t.sla_resolution_due, 
                   t.first_response_at, s.name as status, p.name as priority
            FROM tickets t
            JOIN statuses s ON t.status_id = s.id
            JOIN priorities p ON t.priority_id = p.id
            WHERE (t.sla_response_due < datetime('now') AND t.first_response_at IS NULL)
               OR (t.sla_resolution_due < datetime('now') AND s.name NOT IN ('Resolved', 'Closed'))
            ORDER BY t.sla_response_due ASC, t.sla_resolution_due ASC
        '''
        
        sla_violations = pd.read_sql_query(sla_query, conn)
        
        if len(sla_violations) > 0:
            st.warning(f"⚠️ {len(sla_violations)} tickets with SLA violations!")
            for _, violation in sla_violations.iterrows():
                st.write(f"**{violation['ticket_number']}** - {violation['title']} ({violation['priority']})")
        else:
            st.success("✅ No SLA violations")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets by Status")
        # Filter out statuses with 0 tickets
        status_data_filtered = status_data[status_data['count'] > 0]
        if len(status_data_filtered) > 0:
            fig = px.pie(status_data_filtered, values='count', names='name', 
                        title="Ticket Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No tickets found")
    
    with col2:
        st.subheader("Recent Activity")
        conn = get_db_connection()
        if user['role'] == 'user':
            recent_tickets = pd.read_sql_query('''
                SELECT t.ticket_number, t.title, s.name as status, t.created_at
                FROM tickets t
                JOIN statuses s ON t.status_id = s.id
                WHERE t.requester_id = ?
                ORDER BY t.created_at DESC
                LIMIT 5
            ''', conn, params=(user['id'],))
        else:
            recent_tickets = pd.read_sql_query('''
                SELECT t.ticket_number, t.title, s.name as status, t.created_at
                FROM tickets t
                JOIN statuses s ON t.status_id = s.id
                ORDER BY t.created_at DESC
                LIMIT 5
            ''', conn)
        
        if len(recent_tickets) > 0:
            for _, ticket in recent_tickets.iterrows():
                st.write(f"**{ticket['ticket_number']}** - {ticket['title']}")
                st.caption(f"Status: {ticket['status']} | Created: {ticket['created_at']}")
                st.markdown("---")
        else:
            st.info("No recent tickets")
    
    conn.close()

def show_tickets_list():
    """Show list of tickets"""
    user = st.session_state.user
    
    st.subheader("All Tickets" if user['role'] != 'user' else "My Tickets")
    
    # Show completed tickets toggle (all users)
    show_completed = False
    
    # Get count of completed tickets for current user
    conn_temp = get_db_connection()
    if user['role'] == 'user':
        completed_count = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM tickets t 
            JOIN statuses s ON t.status_id = s.id 
            WHERE s.name IN ('Resolved', 'Closed') AND t.requester_id = ?
        """, conn_temp, params=(user['id'],)).iloc[0]['count']
    else:
        completed_count = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM tickets t 
            JOIN statuses s ON t.status_id = s.id 
            WHERE s.name IN ('Resolved', 'Closed')
        """, conn_temp).iloc[0]['count']
    conn_temp.close()
    
    col_toggle, col_info = st.columns([1, 3])
    with col_toggle:
        show_completed = st.checkbox("Show completed tickets", value=False)
    with col_info:
        if not show_completed and completed_count > 0:
            st.caption(f"({completed_count} completed tickets hidden)")
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    conn = get_db_connection()
    
    with col1:
        statuses = pd.read_sql_query("SELECT id, name FROM statuses ORDER BY id", conn)
        status_filter = st.selectbox("Filter by Status", ["All"] + list(statuses['name']))
    
    with col2:
        priorities = pd.read_sql_query("SELECT id, name FROM priorities ORDER BY level", conn)
        priority_filter = st.selectbox("Filter by Priority", ["All"] + list(priorities['name']))
    
    with col3:
        categories = pd.read_sql_query("SELECT id, name FROM categories ORDER BY name", conn)
        category_filter = st.selectbox("Filter by Category", ["All"] + list(categories['name']))
    
    # Build query
    if user['role'] == 'user':
        base_query = '''
            SELECT t.id, t.ticket_number, t.title, t.description, 
                   s.name as status, p.name as priority, c.name as category,
                   t.created_at, u.full_name as requester
            FROM tickets t
            JOIN statuses s ON t.status_id = s.id
            JOIN priorities p ON t.priority_id = p.id
            JOIN categories c ON t.category_id = c.id
            JOIN users u ON t.requester_id = u.id
            WHERE t.requester_id = ?
        '''
        params = [user['id']]
    else:
        base_query = '''
            SELECT t.id, t.ticket_number, t.title, t.description, 
                   s.name as status, p.name as priority, c.name as category,
                   t.created_at, u.full_name as requester, u2.full_name as assignee
            FROM tickets t
            JOIN statuses s ON t.status_id = s.id
            JOIN priorities p ON t.priority_id = p.id
            JOIN categories c ON t.category_id = c.id
            JOIN users u ON t.requester_id = u.id
            LEFT JOIN users u2 ON t.assignee_id = u2.id
            WHERE 1=1
        '''
        params = []
    
    # Apply filters
    if status_filter != "All":
        status_id = statuses[statuses['name'] == status_filter]['id'].iloc[0]
        base_query += " AND t.status_id = ?"
        params.append(status_id)
    elif not show_completed:
        # Hide completed tickets by default for all users
        base_query += " AND s.name NOT IN ('Resolved', 'Closed')"
    
    if priority_filter != "All":
        priority_id = priorities[priorities['name'] == priority_filter]['id'].iloc[0]
        base_query += " AND t.priority_id = ?"
        params.append(priority_id)
    
    if category_filter != "All":
        category_id = categories[categories['name'] == category_filter]['id'].iloc[0]
        base_query += " AND t.category_id = ?"
        params.append(category_id)
    
    base_query += " ORDER BY t.created_at DESC"
    
    # Execute query
    tickets_df = pd.read_sql_query(base_query, conn, params=params)
    
    # Bulk operations (admin/IT staff only)
    if user['role'] in ['admin', 'it_staff'] and len(tickets_df) > 0:
        st.markdown("---")
        st.subheader("Bulk Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Bulk status update
            statuses = pd.read_sql_query("SELECT id, name FROM statuses ORDER BY id", conn)
            bulk_status = st.selectbox("Bulk Update Status", 
                                     options=[None] + list(statuses['id']), 
                                     format_func=lambda x: "Select status..." if x is None else statuses[statuses['id']==x]['name'].iloc[0])
        
        with col2:
            # Bulk priority update
            priorities = pd.read_sql_query("SELECT id, name FROM priorities ORDER BY level", conn)
            bulk_priority = st.selectbox("Bulk Update Priority", 
                                       options=[None] + list(priorities['id']), 
                                       format_func=lambda x: "Select priority..." if x is None else priorities[priorities['id']==x]['name'].iloc[0])
        
        with col3:
            # Bulk assignee update
            users = pd.read_sql_query("SELECT id, full_name FROM users WHERE role IN ('admin', 'it_staff') ORDER BY full_name", conn)
            bulk_assignee = st.selectbox("Bulk Assign", 
                                       options=[None] + list(users['id']), 
                                       format_func=lambda x: "Select assignee..." if x is None else users[users['id']==x]['full_name'].iloc[0])
        
        # Checkboxes for ticket selection
        st.write("Select tickets for bulk operations:")
        selected_tickets = []
        
        for _, ticket in tickets_df.iterrows():
            if st.checkbox(f"{ticket['ticket_number']} - {ticket['title']}", key=f"bulk_{ticket['id']}"):
                selected_tickets.append(ticket['id'])
        
        if selected_tickets and (bulk_status or bulk_priority or bulk_assignee):
            if st.button("Apply Bulk Changes"):
                cursor = conn.cursor()
                updates = []
                params = []
                
                if bulk_status:
                    updates.append("status_id = ?")
                    params.append(bulk_status)
                
                if bulk_priority:
                    updates.append("priority_id = ?")
                    params.append(bulk_priority)
                
                if bulk_assignee:
                    updates.append("assignee_id = ?")
                    params.append(bulk_assignee)
                
                if updates:
                    updates.append("updated_at = CURRENT_TIMESTAMP")
                    query = f"UPDATE tickets SET {', '.join(updates)} WHERE id IN ({','.join(['?'] * len(selected_tickets))})"
                    params.extend(selected_tickets)
                    
                    cursor.execute(query, params)
                    conn.commit()
                    st.success(f"Updated {len(selected_tickets)} tickets!")
                    st.rerun()
    
    # Display tickets
    if len(tickets_df) > 0:
        for _, ticket in tickets_df.iterrows():
            # Create status badge with proper class mapping
            status_mapping = {
                'Open': 'status-open',
                'In Progress': 'status-in-progress', 
                'Pending User': 'status-pending',
                'Pending Vendor': 'status-pending',
                'Resolved': 'status-resolved',
                'Closed': 'status-closed'
            }
            priority_mapping = {
                'Low': 'priority-low',
                'Medium': 'priority-medium',
                'High': 'priority-high',
                'Critical': 'priority-critical'
            }
            
            status_class = status_mapping.get(ticket['status'], 'status-open')
            priority_class = priority_mapping.get(ticket['priority'], 'priority-low')
            
            # Create expander with status indicator in the title
            status_colors = {
                'Open': '#10b981',        # Green - new/open
                'In Progress': '#3b82f6', # Blue - being worked on
                'Pending': '#f59e0b',     # Yellow - waiting
                'Resolved': '#6b7280',    # Gray - completed
                'Closed': '#374151'       # Dark gray - final
            }
            
            status_color = status_colors.get(ticket['status'], '#6b7280')
            
            # Create custom expandable ticket with status in header
            ticket_key = f"ticket_{ticket['id']}"
            is_expanded = st.session_state.get(ticket_key, False)
            
            # Header with status badge and action buttons
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                # Custom header styling
                st.markdown(f'''
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; 
                            padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
                    <div style="font-weight: 500; color: #1f2937;">
                        {ticket['ticket_number']} - {ticket['title']}
                    </div>
                    <span class="{status_class}">{ticket["status"]}</span>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                # View Details button
                if st.button("View", key=f"view_{ticket['id']}"):
                    st.session_state.selected_ticket = ticket['id']
                    st.rerun()
            
            with col3:
                # Delete button in red
                if st.button("Delete", key=f"delete_{ticket['id']}", help="Delete ticket", type="primary"):
                    st.session_state.delete_ticket_id = ticket['id']
                    st.rerun()
    
    # Handle ticket deletion
    if 'delete_ticket_id' in st.session_state:
        st.markdown("---")
        st.subheader("Delete Ticket")
        
        # Get ticket details for confirmation
        conn = get_db_connection()
        ticket_to_delete = pd.read_sql_query('''
            SELECT t.ticket_number, t.title, s.name as status
            FROM tickets t
            JOIN statuses s ON t.status_id = s.id
            WHERE t.id = ?
        ''', conn, params=(st.session_state.delete_ticket_id,)).iloc[0]
        conn.close()
        
        st.warning(f"Are you sure you want to delete ticket: **{ticket_to_delete['ticket_number']}** - {ticket_to_delete['title']}?")
        st.write("**This action cannot be undone!**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Delete Ticket", type="primary"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM tickets WHERE id = ?', (st.session_state.delete_ticket_id,))
                    conn.commit()
                    conn.close()
                    st.success("Ticket deleted successfully!")
                    del st.session_state.delete_ticket_id
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting ticket: {str(e)}")
        
        with col2:
            if st.button("Cancel"):
                del st.session_state.delete_ticket_id
                st.rerun()
    
    # Show "No tickets found" message only if there are no tickets and no deletion in progress
    elif len(tickets_df) == 0:
        st.info("No tickets found matching the criteria")

def show_ticket_detail(ticket_id):
    """Show detailed view of a specific ticket"""
    user = st.session_state.user
    
    # Back button
    if st.button("← Back to Tickets"):
        if 'selected_ticket' in st.session_state:
            del st.session_state.selected_ticket
        st.rerun()
    
    conn = get_db_connection()
    
    # Get ticket details
    ticket_query = '''
        SELECT t.id, t.ticket_number, t.title, t.description, t.created_at, t.updated_at, t.resolved_at,
               t.sla_response_due, t.sla_resolution_due, t.first_response_at, t.escalated_at,
               s.name as status, p.name as priority, c.name as category,
               u.full_name as requester, u.email as requester_email,
               u2.full_name as assignee, u2.email as assignee_email
        FROM tickets t
        JOIN statuses s ON t.status_id = s.id
        JOIN priorities p ON t.priority_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN users u ON t.requester_id = u.id
        LEFT JOIN users u2 ON t.assignee_id = u2.id
        WHERE t.id = ?
    '''
    
    ticket_df = pd.read_sql_query(ticket_query, conn, params=(ticket_id,))
    
    if len(ticket_df) == 0:
        st.error("Ticket not found")
        conn.close()
        return
    
    ticket = ticket_df.iloc[0]
    
    # Check if user has permission to view this ticket
    if user['role'] == 'user' and ticket['requester'] != user['full_name']:
        st.error("You don't have permission to view this ticket")
        conn.close()
        return
    
    st.title(f"Ticket Details: {ticket['ticket_number']}")
    st.markdown("---")
    
    # Ticket information
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ticket Information")
        st.write(f"**Title:** {ticket['title']}")
        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(f"**Category:** {ticket['category']}")
        st.write(f"**Requester:** {ticket['requester']}")
        if ticket['assignee']:
            st.write(f"**Assignee:** {ticket['assignee']}")
        else:
            st.write("**Assignee:** Unassigned")
    
    with col2:
        st.subheader("Timestamps")
        st.write(f"**Created:** {ticket['created_at']}")
        st.write(f"**Last Updated:** {ticket['updated_at']}")
        if ticket['resolved_at']:
            st.write(f"**Resolved:** {ticket['resolved_at']}")
        
        # SLA Information
        if ticket['sla_response_due']:
            st.write(f"**SLA Response Due:** {ticket['sla_response_due']}")
        if ticket['sla_resolution_due']:
            st.write(f"**SLA Resolution Due:** {ticket['sla_resolution_due']}")
        
        # Check SLA status
        now = datetime.now()
        if ticket['sla_response_due'] and not ticket['first_response_at']:
            try:
                # Handle datetime with or without microseconds
                response_due_str = str(ticket['sla_response_due'])
                if '.' in response_due_str:
                    response_due = datetime.strptime(response_due_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    response_due = datetime.strptime(response_due_str, '%Y-%m-%d %H:%M:%S')
                if now > response_due:
                    st.error("⚠️ SLA Response Time Exceeded!")
            except (ValueError, TypeError):
                pass  # Skip if datetime parsing fails
        
        if ticket['sla_resolution_due'] and ticket['status'] not in ['Resolved', 'Closed']:
            try:
                # Handle datetime with or without microseconds
                resolution_due_str = str(ticket['sla_resolution_due'])
                if '.' in resolution_due_str:
                    resolution_due = datetime.strptime(resolution_due_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    resolution_due = datetime.strptime(resolution_due_str, '%Y-%m-%d %H:%M:%S')
                if now > resolution_due:
                    st.error("⚠️ SLA Resolution Time Exceeded!")
            except (ValueError, TypeError):
                pass  # Skip if datetime parsing fails
    
    st.subheader("Description")
    st.write(ticket['description'])
    
    # Time tracking section
    st.subheader("Time Tracking")
    
    # Get time entries for this ticket
    time_entries_query = '''
        SELECT te.description, te.time_spent_minutes, te.created_at, u.full_name as user_name
        FROM time_entries te
        JOIN users u ON te.user_id = u.id
        WHERE te.ticket_id = ?
        ORDER BY te.created_at DESC
    '''
    
    time_entries_df = pd.read_sql_query(time_entries_query, conn, params=(ticket_id,))
    
    if len(time_entries_df) > 0:
        total_time = time_entries_df['time_spent_minutes'].sum()
        st.metric("Total Time Spent", f"{total_time} minutes ({total_time/60:.1f} hours)")
        
        for _, entry in time_entries_df.iterrows():
            st.write(f"**{entry['user_name']}** - {entry['time_spent_minutes']} minutes ({entry['created_at']})")
            if entry['description']:
                st.write(f"*{entry['description']}*")
            st.markdown("---")
    else:
        st.info("No time entries recorded")
    
    # Add time entry (for admin/IT staff)
    if user['role'] in ['admin', 'it_staff']:
        with st.form("add_time_entry_detail_form"):
            description = st.text_input("Description")
            time_spent = st.number_input("Time Spent (minutes)", min_value=1, value=30)
            
            if st.form_submit_button("Add Time Entry"):
                if time_spent:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO time_entries (ticket_id, user_id, description, time_spent_minutes)
                        VALUES (?, ?, ?, ?)
                    ''', (ticket_id, user['id'], description, time_spent))
                    
                    conn.commit()
                    st.success("Time entry added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter time spent")
    
    # Comments section
    st.subheader("Comments")
    
    # Get comments
    comments_query = '''
        SELECT c.content, c.is_internal, c.created_at, u.full_name as author
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.ticket_id = ?
        ORDER BY c.created_at ASC
    '''
    
    comments_df = pd.read_sql_query(comments_query, conn, params=(ticket_id,))
    
    if len(comments_df) > 0:
        for _, comment in comments_df.iterrows():
            with st.container():
                if comment['is_internal'] and user['role'] not in ['admin', 'it_staff']:
                    continue  # Skip internal comments for regular users
                
                st.write(f"**{comment['author']}** ({comment['created_at']})")
                if comment['is_internal']:
                    st.info(f"[Internal] {comment['content']}")
                else:
                    st.write(comment['content'])
                st.markdown("---")
    else:
        st.info("No comments yet")
    
    # Add comment form
    st.subheader("Add Comment")
    with st.form("add_comment_form"):
        comment_content = st.text_area("Comment", placeholder="Add a comment...")
        is_internal = False
        if user['role'] in ['admin', 'it_staff']:
            is_internal = st.checkbox("Internal comment (not visible to requester)")
        
        if st.form_submit_button("Add Comment"):
            if comment_content:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO comments (ticket_id, user_id, content, is_internal)
                    VALUES (?, ?, ?, ?)
                ''', (ticket_id, user['id'], comment_content, is_internal))
                
                # Update ticket's updated_at timestamp
                cursor.execute('''
                    UPDATE tickets SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (ticket_id,))
                
                # Set first_response_at if this is the first response from IT staff
                if user['role'] in ['admin', 'it_staff'] and not is_internal:
                    cursor.execute('''
                        UPDATE tickets SET first_response_at = CURRENT_TIMESTAMP 
                        WHERE id = ? AND first_response_at IS NULL
                    ''', (ticket_id,))
                
                conn.commit()
                st.success("Comment added successfully!")
                st.rerun()
            else:
                st.error("Please enter a comment")
    
    # Admin/IT Staff actions
    if user['role'] in ['admin', 'it_staff']:
        st.subheader("Ticket Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Status update
            current_status = ticket['status']
            statuses = pd.read_sql_query("SELECT id, name FROM statuses ORDER BY id", conn)
            new_status = st.selectbox("Update Status", 
                                    options=statuses['id'], 
                                    index=int(statuses[statuses['name'] == current_status].index[0]),
                                    format_func=lambda x: statuses[statuses['id']==x]['name'].iloc[0])
            
            if st.button("Update Status"):
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tickets SET status_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (new_status, ticket_id))
                
                # Check if status is completed (Resolved or Closed)
                new_status_name = statuses[statuses['id'] == new_status]['name'].iloc[0]
                if new_status_name in ['Resolved', 'Closed']:
                    # Set resolved_at timestamp for completed tickets
                    cursor.execute('''
                        UPDATE tickets SET resolved_at = CURRENT_TIMESTAMP WHERE id = ?
                    ''', (ticket_id,))
                
                conn.commit()
                st.success("Status updated!")
                
                # If status is completed, go back to ticket list
                if new_status_name in ['Resolved', 'Closed']:
                    if 'selected_ticket' in st.session_state:
                        del st.session_state.selected_ticket
                    st.rerun()
                else:
                    st.rerun()
        
        with col2:
            # Assign ticket
            users = pd.read_sql_query("SELECT id, full_name FROM users WHERE role IN ('admin', 'it_staff') ORDER BY full_name", conn)
            current_assignee_id = pd.read_sql_query("SELECT assignee_id FROM tickets WHERE id = ?", conn, params=(ticket_id,)).iloc[0]['assignee_id']
            
            assignee_options = [None] + list(users['id'])
            assignee_labels = ["Unassigned"] + list(users['full_name'])
            
            current_index = 0
            if current_assignee_id:
                current_index = int(assignee_options.index(current_assignee_id))
            
            new_assignee = st.selectbox("Assign to", 
                                      options=assignee_options,
                                      index=current_index,
                                      format_func=lambda x: assignee_labels[assignee_options.index(x)] if x is not None else "Unassigned")
            
            if st.button("Update Assignment"):
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tickets SET assignee_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (new_assignee, ticket_id))
                conn.commit()
                st.success("Assignment updated!")
                st.rerun()
        
        with col3:
            # Priority update
            current_priority = ticket['priority']
            priorities = pd.read_sql_query("SELECT id, name FROM priorities ORDER BY level", conn)
            new_priority = st.selectbox("Update Priority", 
                                      options=priorities['id'], 
                                      index=int(priorities[priorities['name'] == current_priority].index[0]),
                                      format_func=lambda x: priorities[priorities['id']==x]['name'].iloc[0])
            
            if st.button("Update Priority"):
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tickets SET priority_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (new_priority, ticket_id))
                conn.commit()
                st.success("Priority updated!")
                st.rerun()
        

    
    conn.close()

def show_edit_ticket(ticket_id):
    """Show edit ticket form"""
    user = st.session_state.user
    
    # Back button
    if st.button("← Back to Tickets"):
        if 'edit_ticket' in st.session_state:
            del st.session_state.edit_ticket
        st.rerun()
    
    conn = get_db_connection()
    
    # Get ticket details
    ticket_query = '''
        SELECT t.id, t.ticket_number, t.title, t.description, t.created_at, t.updated_at, t.resolved_at,
               t.sla_response_due, t.sla_resolution_due, t.first_response_at, t.escalated_at,
               s.name as status, p.name as priority, c.name as category,
               u.full_name as requester, u.email as requester_email,
               u2.full_name as assignee, u2.email as assignee_email
        FROM tickets t
        JOIN statuses s ON t.status_id = s.id
        JOIN priorities p ON t.priority_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN users u ON t.requester_id = u.id
        LEFT JOIN users u2 ON t.assignee_id = u2.id
        WHERE t.id = ?
    '''
    
    ticket_df = pd.read_sql_query(ticket_query, conn, params=(ticket_id,))
    
    if len(ticket_df) == 0:
        st.error("Ticket not found")
        conn.close()
        return
    
    ticket = ticket_df.iloc[0]
    
    st.subheader(f"Edit Ticket: {ticket['ticket_number']}")
    
    with st.form("edit_ticket_form"):
        # Get current values
        title = st.text_input("Title", value=ticket['title'])
        description = st.text_area("Description", value=ticket['description'], height=150)
        
        # Get categories and priorities
        categories = pd.read_sql_query("SELECT id, name FROM categories ORDER BY name", conn)
        priorities = pd.read_sql_query("SELECT id, name FROM priorities ORDER BY level", conn)
        statuses = pd.read_sql_query("SELECT id, name FROM statuses ORDER BY id", conn)
        
        # Current values
        current_category = categories[categories['name'] == ticket['category']]['id'].iloc[0]
        current_priority = priorities[priorities['name'] == ticket['priority']]['id'].iloc[0]
        current_status = statuses[statuses['name'] == ticket['status']]['id'].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            category_id = st.selectbox("Category", 
                                     options=list(categories['id']), 
                                     index=list(categories['id']).index(current_category),
                                     format_func=lambda x: categories[categories['id']==x]['name'].iloc[0])
            
            priority_id = st.selectbox("Priority", 
                                     options=list(priorities['id']), 
                                     index=list(priorities['id']).index(current_priority),
                                     format_func=lambda x: priorities[priorities['id']==x]['name'].iloc[0])
        
        with col2:
            status_id = st.selectbox("Status", 
                                   options=list(statuses['id']), 
                                   index=list(statuses['id']).index(current_status),
                                   format_func=lambda x: statuses[statuses['id']==x]['name'].iloc[0])
            
            # Assignee selection (admin/IT staff only)
            if user['role'] in ['admin', 'it_staff']:
                users = pd.read_sql_query("SELECT id, full_name FROM users WHERE role IN ('admin', 'it_staff') ORDER BY full_name", conn)
                current_assignee = None
                if ticket['assignee']:
                    current_assignee = users[users['full_name'] == ticket['assignee']]['id'].iloc[0] if len(users[users['full_name'] == ticket['assignee']]) > 0 else None
                
                assignee_options = [None] + list(users['id'])
                assignee_index = 0
                if current_assignee:
                    assignee_index = assignee_options.index(current_assignee)
                
                assignee_id = st.selectbox("Assignee", 
                                         options=assignee_options, 
                                         index=assignee_index,
                                         format_func=lambda x: "Unassigned" if x is None else users[users['id']==x]['full_name'].iloc[0])
            else:
                assignee_id = None
        
        submitted = st.form_submit_button("Update Ticket")
        
        if submitted:
            if title and description:
                cursor = conn.cursor()
                
                # Update ticket
                cursor.execute('''
                    UPDATE tickets 
                    SET title = ?, description = ?, category_id = ?, priority_id = ?, status_id = ?, 
                        assignee_id = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (title, description, category_id, priority_id, status_id, assignee_id, ticket_id))
                
                conn.commit()
                st.success("Ticket updated successfully!")
                
                # Clear edit state and go back to ticket list
                if 'edit_ticket' in st.session_state:
                    del st.session_state.edit_ticket
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    conn.close()

def show_create_ticket():
    """Show create ticket form"""
    st.subheader("Create New Ticket")
    
    conn = get_db_connection()
    

    
    with st.form("create_ticket_form"):
        # Get categories and priorities (put "Other" at the end)
        categories = pd.read_sql_query("SELECT id, name FROM categories ORDER BY CASE WHEN name = 'Other' THEN 1 ELSE 0 END, name", conn)
        priorities = pd.read_sql_query("SELECT id, name FROM priorities ORDER BY level", conn)
        
        col1, col2 = st.columns(2)
        with col1:
            category_id = st.selectbox("Category", 
                                     options=categories['id'], 
                                     format_func=lambda x: categories[categories['id']==x]['name'].iloc[0])
        
        with col2:
            priority_id = st.selectbox("Priority", 
                                     options=priorities['id'], 
                                     format_func=lambda x: priorities[priorities['id']==x]['name'].iloc[0])
        
        # Show SLA information
        response_due, resolution_due = calculate_sla_dates(priority_id)
        if response_due and resolution_due:
            st.info(f"**SLA:** Response due within {response_due.strftime('%Y-%m-%d %H:%M')}, Resolution due within {resolution_due.strftime('%Y-%m-%d %H:%M')}")
        
        title = st.text_input("Title", placeholder="Brief description of the issue")
        description = st.text_area("Description", placeholder="Detailed description of the issue...")
        
        submitted = st.form_submit_button("Create Ticket")
        
        if submitted:
            if title and description:
                ticket_number = generate_ticket_number()
                user = st.session_state.user
                
                # Get default status (Open) - use direct SQL instead of pandas
                cursor_temp = conn.cursor()
                cursor_temp.execute("SELECT id FROM statuses WHERE name = 'Open'")
                status_result = cursor_temp.fetchone()
                if status_result:
                    status_id = status_result[0]
                else:
                    st.error("Error: 'Open' status not found in database")
                    conn.close()
                    return
                
                # Calculate SLA dates
                response_due, resolution_due = calculate_sla_dates(priority_id)
                
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tickets (ticket_number, title, description, status_id, priority_id, category_id, requester_id, sla_response_due, sla_resolution_due)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ticket_number, title, description, status_id, priority_id, category_id, user['id'], response_due, resolution_due))
                
                conn.commit()
                conn.close()
                
                st.success(f"Ticket created successfully! Ticket number: {ticket_number}")
                # Redirect back to main page
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    conn.close()

def show_knowledge_base():
    """Show knowledge base page"""
    st.subheader("Knowledge Base")
    
    conn = get_db_connection()
    
    # Search functionality
    search_term = st.text_input("Search Knowledge Base", placeholder="Enter keywords...")
    
    # Category filter
    categories = pd.read_sql_query("SELECT id, name FROM categories ORDER BY name", conn)
    category_filter = st.selectbox("Filter by Category", ["All"] + list(categories['name']))
    
    # Build query
    base_query = '''
        SELECT kb.id, kb.title, kb.content, kb.tags, kb.created_at, c.name as category, u.full_name as author
        FROM knowledge_base kb
        LEFT JOIN categories c ON kb.category_id = c.id
        LEFT JOIN users u ON kb.created_by = u.id
        WHERE kb.is_public = 1
    '''
    params = []
    
    if search_term:
        base_query += " AND (kb.title LIKE ? OR kb.content LIKE ? OR kb.tags LIKE ?)"
        search_param = f"%{search_term}%"
        params.extend([search_param, search_param, search_param])
    
    if category_filter != "All":
        category_id = categories[categories['name'] == category_filter]['id'].iloc[0]
        base_query += " AND kb.category_id = ?"
        params.append(category_id)
    
    base_query += " ORDER BY kb.created_at DESC"
    
    # Execute query
    kb_articles = pd.read_sql_query(base_query, conn, params=params)
    conn.close()
    
    # Display articles
    if len(kb_articles) > 0:
        for _, article in kb_articles.iterrows():
            with st.expander(f"{article['title']}"):
                st.write(f"**Category:** {article['category'] or 'General'}")
                st.write(f"**Author:** {article['author']}")
                st.write(f"**Created:** {article['created_at']}")
                if article['tags']:
                    st.write(f"**Tags:** {article['tags']}")
                st.markdown("---")
                st.markdown(article['content'])
    else:
        st.info("No articles found matching your criteria")
    
    # Add new article (for admin/IT staff)
    user = st.session_state.user
    if user['role'] in ['admin', 'it_staff']:
        st.markdown("---")
        st.subheader("Add New Article")
        
        with st.form("add_article_form"):
            title = st.text_input("Title")
            content = st.text_area("Content", height=200)
            tags = st.text_input("Tags (comma-separated)")
            
            conn = get_db_connection()
            categories = pd.read_sql_query("SELECT id, name FROM categories ORDER BY name", conn)
            category_id = st.selectbox("Category", 
                                     options=[None] + list(categories['id']), 
                                     format_func=lambda x: "General" if x is None else categories[categories['id']==x]['name'].iloc[0])
            
            if st.form_submit_button("Add Article"):
                if title and content:
                    cursor = conn.cursor()
                    
                    # Check if title already exists
                    cursor.execute('SELECT id FROM knowledge_base WHERE title = ?', (title,))
                    if cursor.fetchone():
                        st.error("An article with this title already exists. Please choose a different title.")
                    else:
                        try:
                            cursor.execute('''
                                INSERT INTO knowledge_base (title, content, category_id, tags, created_by)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (title, content, category_id, tags, user['id']))
                            
                            conn.commit()
                            st.success("Article added successfully!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("An article with this title already exists. Please choose a different title.")
                else:
                    st.error("Please fill in title and content")
            
            conn.close()



def show_time_tracking():
    """Show time tracking page (admin/IT staff only)"""
    st.subheader("Time Tracking")
    
    conn = get_db_connection()
    
    # Get time entries
    time_entries = pd.read_sql_query('''
        SELECT te.id, te.description, te.time_spent_minutes, te.created_at,
               t.ticket_number, t.title, u.full_name as user_name
        FROM time_entries te
        JOIN tickets t ON te.ticket_id = t.id
        JOIN users u ON te.user_id = u.id
        ORDER BY te.created_at DESC
        LIMIT 50
    ''', conn)
    
    if len(time_entries) > 0:
        st.dataframe(time_entries, use_container_width=True)
        
        # Summary
        total_time = time_entries['time_spent_minutes'].sum()
        st.metric("Total Time Tracked", f"{total_time} minutes ({total_time/60:.1f} hours)")
    else:
        st.info("No time entries found")
    
    # Add time entry
    st.markdown("---")
    st.subheader("Add Time Entry")
    
    with st.form("add_time_entry_form"):
        # Get tickets
        tickets = pd.read_sql_query("SELECT id, ticket_number, title FROM tickets ORDER BY created_at DESC", conn)
        ticket_id = st.selectbox("Ticket", 
                               options=tickets['id'], 
                               format_func=lambda x: f"{tickets[tickets['id']==x]['ticket_number'].iloc[0]} - {tickets[tickets['id']==x]['title'].iloc[0]}")
        
        description = st.text_input("Description")
        time_spent = st.number_input("Time Spent (minutes)", min_value=1, value=30)
        
        if st.form_submit_button("Add Time Entry"):
            if ticket_id and time_spent:
                user = st.session_state.user
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO time_entries (ticket_id, user_id, description, time_spent_minutes)
                    VALUES (?, ?, ?, ?)
                ''', (ticket_id, user['id'], description, time_spent))
                
                conn.commit()
                st.success("Time entry added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    conn.close()

def show_user_management():
    """Show user management page (admin only)"""
    st.subheader("User Management")
    
    conn = get_db_connection()
    
    # Get users with additional statistics
    users_query = '''
        SELECT u.id, u.username, u.email, u.full_name, u.role, u.department, u.created_at,
               COUNT(DISTINCT t1.id) as tickets_created,
               COUNT(DISTINCT t2.id) as tickets_assigned,
               COUNT(DISTINCT te.id) as time_entries
        FROM users u
        LEFT JOIN tickets t1 ON u.id = t1.requester_id
        LEFT JOIN tickets t2 ON u.id = t2.assignee_id
        LEFT JOIN time_entries te ON u.id = te.user_id
        GROUP BY u.id, u.username, u.email, u.full_name, u.role, u.department, u.created_at
        ORDER BY u.created_at DESC
    '''
    
    users = pd.read_sql_query(users_query, conn)
    
    if len(users) > 0:
        # Display users in a more detailed format
        for _, user in users.iterrows():
            with st.expander(f"{user['full_name']} ({user['username']}) - {user['role'].title()}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Email:** {user['email']}")
                    st.write(f"**Department:** {user['department'] or 'Not specified'}")
                    st.write(f"**Created:** {user['created_at']}")
                
                with col2:
                    st.write(f"**Tickets Created:** {user['tickets_created']}")
                    st.write(f"**Tickets Assigned:** {user['tickets_assigned']}")
                    st.write(f"**Time Entries:** {user['time_entries']}")
                
                with col3:
                    # Edit user button
                    if st.button(f"Edit User", key=f"edit_user_{user['id']}"):
                        st.session_state.edit_user_id = user['id']
                        st.rerun()
                    
                    # Delete user button (with confirmation)
                    if st.button(f"Delete User", key=f"delete_user_{user['id']}"):
                        st.session_state.delete_user_id = user['id']
                        st.rerun()
    else:
        st.info("No users found")
    
    # Handle user editing
    if 'edit_user_id' in st.session_state:
        st.markdown("---")
        st.subheader("Edit User")
        
        user_to_edit = users[users['id'] == st.session_state.edit_user_id].iloc[0]
        
        with st.form("edit_user_form"):
            edit_username = st.text_input("Username", value=user_to_edit['username'])
            edit_email = st.text_input("Email", value=user_to_edit['email'])
            edit_full_name = st.text_input("Full Name", value=user_to_edit['full_name'])
            edit_role = st.selectbox("Role", ["user", "it_staff", "admin"], 
                                   index=["user", "it_staff", "admin"].index(user_to_edit['role']))
            edit_department = st.text_input("Department", value=user_to_edit['department'] or "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update User"):
                    try:
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE users SET username = ?, email = ?, full_name = ?, role = ?, department = ?
                            WHERE id = ?
                        ''', (edit_username, edit_email, edit_full_name, edit_role, edit_department, st.session_state.edit_user_id))
                        
                        conn.commit()
                        st.success("User updated successfully!")
                        del st.session_state.edit_user_id
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Username or email already exists")
            
            with col2:
                if st.form_submit_button("Cancel"):
                    del st.session_state.edit_user_id
                    st.rerun()
    
    # Handle user deletion
    if 'delete_user_id' in st.session_state:
        st.markdown("---")
        st.subheader("Delete User")
        
        user_to_delete = users[users['id'] == st.session_state.delete_user_id].iloc[0]
        st.warning(f"Are you sure you want to delete user: {user_to_delete['full_name']} ({user_to_delete['username']})?")
        st.write("**This action cannot be undone!**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Delete User", type="primary"):
                try:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM users WHERE id = ?', (st.session_state.delete_user_id,))
                    conn.commit()
                    st.success("User deleted successfully!")
                    del st.session_state.delete_user_id
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Cannot delete user - they have associated tickets or time entries")
        
        with col2:
            if st.button("Cancel"):
                del st.session_state.delete_user_id
                st.rerun()
    
    # Add new user form
    st.markdown("---")
    st.subheader("Add New User")
    
    with st.form("add_user_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "it_staff", "admin"])
        department = st.text_input("Department")
        
        if st.form_submit_button("Add User"):
            if username and email and full_name and password:
                cursor = conn.cursor()
                
                try:
                    cursor.execute('''
                        INSERT INTO users (username, password_hash, email, full_name, role, department)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (username, hash_password(password), email, full_name, role, department))
                    
                    conn.commit()
                    st.success("User added successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Username or email already exists")
            else:
                st.error("Please fill in all required fields")
    
    conn.close()

def show_reports():
    """Show reports and analytics"""
    st.subheader("Reports & Analytics")
    
    conn = get_db_connection()
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Key metrics
    st.subheader("Key Metrics")
    
    # Total tickets in date range
    total_tickets = pd.read_sql_query('''
        SELECT COUNT(*) as count FROM tickets 
        WHERE DATE(created_at) BETWEEN ? AND ?
    ''', conn, params=(start_date, end_date)).iloc[0]['count']
    
    # Resolved tickets
    resolved_tickets = pd.read_sql_query('''
        SELECT COUNT(*) as count FROM tickets 
        WHERE DATE(created_at) BETWEEN ? AND ? AND status_id IN (
            SELECT id FROM statuses WHERE name IN ('Resolved', 'Closed')
        )
    ''', conn, params=(start_date, end_date)).iloc[0]['count']
    
    # Average resolution time
    avg_resolution = pd.read_sql_query('''
        SELECT AVG(julianday(resolved_at) - julianday(created_at)) as avg_days
        FROM tickets 
        WHERE DATE(created_at) BETWEEN ? AND ? AND resolved_at IS NOT NULL
    ''', conn, params=(start_date, end_date)).iloc[0]['avg_days']
    
    # SLA compliance
    sla_compliant = pd.read_sql_query('''
        SELECT COUNT(*) as count FROM tickets 
        WHERE DATE(created_at) BETWEEN ? AND ? 
        AND (first_response_at IS NULL OR first_response_at <= sla_response_due)
        AND (resolved_at IS NULL OR resolved_at <= sla_resolution_due)
    ''', conn, params=(start_date, end_date)).iloc[0]['count']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", total_tickets)
    with col2:
        st.metric("Resolved Tickets", resolved_tickets)
    with col3:
        st.metric("Avg Resolution Time", f"{avg_resolution:.1f} days" if avg_resolution else "N/A")
    with col4:
        sla_percentage = (sla_compliant / total_tickets * 100) if total_tickets > 0 else 0
        st.metric("SLA Compliance", f"{sla_percentage:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets by Status")
        status_data = pd.read_sql_query('''
            SELECT s.name, COUNT(t.id) as count
            FROM statuses s
            LEFT JOIN tickets t ON s.id = t.status_id AND DATE(t.created_at) BETWEEN ? AND ?
            GROUP BY s.id, s.name
            ORDER BY s.id
        ''', conn, params=(start_date, end_date))
        
        if len(status_data) > 0:
            fig = px.pie(status_data, values='count', names='name')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Tickets by Priority")
        priority_data = pd.read_sql_query('''
            SELECT p.name, COUNT(t.id) as count
            FROM priorities p
            LEFT JOIN tickets t ON p.id = t.priority_id AND DATE(t.created_at) BETWEEN ? AND ?
            GROUP BY p.id, p.name
            ORDER BY p.level
        ''', conn, params=(start_date, end_date))
        
        if len(priority_data) > 0:
            fig = px.bar(priority_data, x='name', y='count')
            st.plotly_chart(fig, use_container_width=True)
    
    # Time tracking summary
    st.subheader("Time Tracking Summary")
    time_summary = pd.read_sql_query('''
        SELECT u.full_name as user, SUM(te.time_spent_minutes) as total_minutes,
               COUNT(DISTINCT te.ticket_id) as tickets_worked
        FROM time_entries te
        JOIN users u ON te.user_id = u.id
        WHERE DATE(te.created_at) BETWEEN ? AND ?
        GROUP BY u.id, u.full_name
        ORDER BY total_minutes DESC
    ''', conn, params=(start_date, end_date))
    
    if len(time_summary) > 0:
        time_summary['total_hours'] = time_summary['total_minutes'] / 60
        st.dataframe(time_summary[['user', 'total_hours', 'tickets_worked']], use_container_width=True)
    else:
        st.info("No time tracking data found")
    
    # Recent tickets table
    st.subheader("Recent Tickets")
    recent_tickets = pd.read_sql_query('''
        SELECT t.ticket_number, t.title, s.name as status, p.name as priority,
               c.name as category, u.full_name as requester, t.created_at
        FROM tickets t
        JOIN statuses s ON t.status_id = s.id
        JOIN priorities p ON t.priority_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN users u ON t.requester_id = u.id
        WHERE DATE(t.created_at) BETWEEN ? AND ?
        ORDER BY t.created_at DESC
        LIMIT 20
    ''', conn, params=(start_date, end_date))
    
    conn.close()
    
    if len(recent_tickets) > 0:
        st.dataframe(recent_tickets, use_container_width=True)
    else:
        st.info("No tickets found")

def show_profile():
    """Show user profile page"""
    user = st.session_state.user
    
    st.subheader("Profile")
    
    # Display current profile
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Full Name:** {user['full_name']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Department:** {user['department'] or 'Not specified'}")
    
    with col2:
        # Get user statistics
        conn = get_db_connection()
        
        # Count tickets created by user
        tickets_created = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM tickets WHERE requester_id = ?", 
            conn, params=(user['id'],)
        ).iloc[0]['count']
        
        # Count tickets assigned to user (if IT staff/admin)
        tickets_assigned = 0
        if user['role'] in ['admin', 'it_staff']:
            tickets_assigned = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM tickets WHERE assignee_id = ?", 
                conn, params=(user['id'],)
            ).iloc[0]['count']
        
        # Count time entries
        time_entries = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM time_entries WHERE user_id = ?", 
            conn, params=(user['id'],)
        ).iloc[0]['count']
        
        conn.close()
        
        st.metric("Tickets Created", tickets_created)
        if user['role'] in ['admin', 'it_staff']:
            st.metric("Tickets Assigned", tickets_assigned)
        st.metric("Time Entries", time_entries)
    
    # Profile editing section
    st.markdown("---")
    st.subheader("Edit Profile")
    
    with st.form("edit_profile_form"):
        new_email = st.text_input("Email", value=user['email'])
        new_full_name = st.text_input("Full Name", value=user['full_name'])
        new_department = st.text_input("Department", value=user['department'] or "")
        
        # Password change section
        st.write("**Change Password (leave blank to keep current)**")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Update Profile"):
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validate current password if changing password
            password_valid = True
            if new_password:
                if not current_password:
                    st.error("Please enter your current password to change it")
                    password_valid = False
                else:
                    # Verify current password
                    cursor.execute('''
                        SELECT password_hash FROM users WHERE id = ?
                    ''', (user['id'],))
                    stored_hash = cursor.fetchone()[0]
                    if not verify_password(current_password, stored_hash):
                        st.error("Current password is incorrect")
                        password_valid = False
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                        password_valid = False
            
            if password_valid:
                try:
                    # Update profile
                    if new_password:
                        # Update with new password
                        cursor.execute('''
                            UPDATE users SET email = ?, full_name = ?, department = ?, password_hash = ?
                            WHERE id = ?
                        ''', (new_email, new_full_name, new_department, hash_password(new_password), user['id']))
                    else:
                        # Update without password change
                        cursor.execute('''
                            UPDATE users SET email = ?, full_name = ?, department = ?
                            WHERE id = ?
                        ''', (new_email, new_full_name, new_department, user['id']))
                    
                    conn.commit()
                    
                    # Update session state
                    st.session_state.user['email'] = new_email
                    st.session_state.user['full_name'] = new_full_name
                    st.session_state.user['department'] = new_department
                    
                    st.success("Profile updated successfully!")
                    st.rerun()
                    
                except sqlite3.IntegrityError:
                    st.error("Email already exists. Please choose a different email.")
                finally:
                    conn.close()

# Main app logic
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
