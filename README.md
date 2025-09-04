# IT Ticketing System

A comprehensive IT support ticketing system built with Python and Streamlit, featuring user authentication, role-based access control, ticket management, SLA tracking, and real-time analytics.

## 🚀 Features

### User Management
- **Multi-role authentication** (Admin, IT Staff, User)
- **Secure login system** with password hashing
- **Role-based access control** with different permissions

### Ticket Management
- **Create, view, edit, and delete tickets**
- **Color-coded status badges** (Open, In Progress, Resolved, etc.)
- **Priority levels** (Low, Medium, High, Critical)
- **Category organization** (Hardware, Software, Network, etc.)
- **Bulk operations** for IT staff and admins

### Advanced Features
- **SLA tracking** with response and resolution time monitoring
- **Time tracking** for work hours and productivity
- **Comments system** with internal/external visibility
- **Knowledge base** for common solutions
- **Analytics and reporting** with interactive charts
- **User management** (admin only)

## 🛠️ Technologies

- **Python** - Core development language
- **Streamlit** - Web framework and UI
- **SQLite** - Database management
- **HTML/CSS** - Custom styling and components
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive charts and visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/it-ticketing-system.git
   cd it-ticketing-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 👥 Demo Accounts

The system comes with pre-configured demo accounts:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | `admin` | `admin123` | Full system control, user management, all tickets |
| **IT Staff** | `itstaff` | `itstaff123` | All tickets, time tracking, reports (no user management) |
| **User** | `user` | `user123` | Create tickets, view own tickets, knowledge base |

## 📊 System Overview

### Dashboard
- **Real-time statistics** and ticket counts
- **SLA alerts** for overdue tickets
- **Interactive charts** showing ticket distribution
- **Recent activity** feed

### Ticket Workflow
1. **Create** - Users submit tickets with priority and category
2. **Assign** - IT staff assign tickets to team members
3. **Track** - Monitor progress with status updates and time tracking
4. **Resolve** - Close tickets with resolution details
5. **Report** - Generate analytics and performance reports

### Role Permissions

#### Admin
- Full system access
- User management (create, edit, delete users)
- All ticket operations
- System configuration
- Advanced reporting

#### IT Staff
- All ticket management
- Time tracking
- Bulk operations
- Reports and analytics
- Knowledge base management

#### User
- Create and view own tickets
- Access knowledge base
- Update profile information

## 🎨 UI/UX Features

- **Modern, responsive design** with clean interface
- **Color-coded status badges** for quick visual identification
- **Interactive charts** and data visualizations
- **Mobile-friendly** layout
- **Professional styling** with custom CSS

## 📈 Analytics & Reporting

- **Ticket volume** by status, priority, and category
- **SLA compliance** tracking
- **Time tracking** summaries
- **User productivity** metrics
- **Interactive dashboards** with Plotly charts

## 🔧 Configuration

The system automatically initializes with:
- Default user accounts
- Standard ticket categories
- Priority levels
- Status definitions
- Sample knowledge base articles

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Deploy with one click

### Local Production
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support or questions, please open an issue in the GitHub repository.

---

**Built with ❤️ using Python and Streamlit**
