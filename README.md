# Support Ticket Dashboard

A full-stack support ticket management system that allows customers to submit support requests and provides an admin dashboard for monitoring, searching, filtering, and managing tickets.

The system automatically classifies each ticket based on its subject and description and assigns a category and priority before storing the ticket in a MySQL database.

---

## Features

- Customer support ticket submission
- Automatic ticket category classification
- Automatic priority classification
- Input validation
- Admin dashboard for ticket management
- View submitted tickets
- Search tickets
- Filter tickets by category
- Filter tickets by priority
- Filter tickets by status
- View complete ticket details
- Update ticket status
- Ticket statistics dashboard
- REST API backend
- MySQL database integration
- Cloud database using Aiven
- Frontend and backend deployment using Render
- Environment variable based database configuration
- CORS-enabled frontend and backend communication

---

## Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

### Backend

- Python
- Flask
- Flask-CORS
- REST API

### Database

- MySQL
- Aiven

### Deployment

- GitHub
- Render

---

## Project Architecture

```text
Customer
   |
   v
Frontend
HTML / CSS / JavaScript
   |
   | REST API
   v
Flask Backend
   |
   +----------------------+
   |                      |
   v                      v
Ticket Classifier      MySQL Database
Category/Priority         Aiven
   |
   v
Admin Dashboard
Search / Filter / Status Management                  

Project Structure                                 

support-ticket-dashboard/
│
├── backend/
│   ├── app.py
│   ├── classifier.py
│   ├── db.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   ├── dashboard.html
│   └── dashboard.js
│
├── README.md
└── .gitignore


Live Demo
Customer Ticket Form

https://support-ticket-dashboard-frontend.onrender.com

Admin Dashboard

https://support-ticket-dashboard-frontend.onrender.com/dashboard.html

Backend API

https://support-ticket-dashboard-1.onrender.com

How It Works
1.Customer enters their name, email, subject, and description.
2.The frontend sends the ticket information to the Flask REST API.
3.The backend validates the submitted data.
4.The subject and description are passed to the ticket classification module.
5.The system automatically determines the ticket category and priority.
6.The ticket information is stored in the MySQL database.
7.The admin dashboard retrieves and displays the submitted tickets.
8.Admin can search and filter tickets.
9.Admin can view complete ticket details.
10.Admin can update the status of tickets.
11.Dashboard statistics are updated based on the stored ticket data.

Ticket Categories

The system supports the following ticket categories:

Technical
Billing
Shipping

Ticket Priorities

The system supports the following priority levels:

High
Medium
Low

Ticket Status

Each ticket can have one of the following statuses:

Open
In Progress
Resolved

Dashboard

The admin dashboard provides:

Total ticket count
Open ticket count
In Progress ticket count
Resolved ticket count
Category statistics
Priority statistics
Ticket search
Category filtering
Priority filtering
Status filtering
Ticket details modal
Ticket status management
Automatic statistics refresh after status updates
Automatic Ticket Classification

When a customer submits a ticket, the backend processes the subject and description through the ticket classification module.

The system automatically assigns:

Category
Priority

For example:
Customer Issue
      |
      v
Subject + Description
      |
      v
Ticket Classifier
      |
      +----------------+
      |                |
      v                v
   Category         Priority
      |                |
      v                v
Technical          Medium
his reduces the need for manual classification of every incoming support request.

API Endpoints
Method	Endpoint	Purpose
GET	/	Check API status
GET	/health	Check API and database connectivity
POST	/tickets	Create a new support ticket
GET	/tickets	Retrieve and filter tickets
GET	/tickets/stats	Retrieve ticket statistics
PATCH	/tickets/<id>	Update ticket status
Create Ticket API
Endpoint
POST /tickets
Request Body
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Unable to access my account",
  "description": "I am unable to log in to my account."
}
Example Response
{
  "id": 15,
  "category": "Technical",
  "priority": "Medium",
  "status": "Open"
}
Get Tickets API
Endpoint
GET /tickets

The endpoint retrieves submitted tickets from the database.

It supports filtering using:

Category
Priority
Status
Search
Example
GET /tickets?category=Technical
Multiple Filters
GET /tickets?category=Technical&priority=High&status=Open
Search

The search functionality can search ticket information such as:

Customer name
Email
Subject
Description
Category
Ticket Statistics API
Endpoint
GET /tickets/stats

The endpoint provides statistics for:

Total tickets
Ticket categories
Ticket priorities
Ticket statuses

Example response structure:

{
  "category": {
    "Billing": 5,
    "Shipping": 3,
    "Technical": 7
  },
  "priority": {
    "High": 4,
    "Medium": 6,
    "Low": 5
  },
  "status": {
    "Open": 8,
    "In Progress": 4,
    "Resolved": 3
  },
  "total": 15
}
Update Ticket Status
Endpoint
PATCH /tickets/<id>
Request Body
{
  "status": "Resolved"
}

Supported statuses:

Open
In Progress
Resolved

After the update, the dashboard refreshes the ticket list and statistics.

Database

The application uses MySQL for persistent ticket storage.

The MySQL database is hosted using Aiven.

The backend connects to the database using environment variables.

The required environment variables are:

DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME

Database credentials are not stored directly in the source code.

Database Design

The main ticket information stored by the application includes:

Ticket ID
Customer name
Customer email
Subject
Description
Category
Priority
Status
Created date

The database provides persistent storage so that submitted tickets remain available when the application is accessed again.

Security

The project includes basic application security practices:

Database credentials are stored using environment variables.
.env files are excluded from Git.
User input is validated before database operations.
Input length limits are applied to submitted fields.
SQL queries use parameterized values.
HTML content displayed in the dashboard is escaped where appropriate.
CORS is configured for frontend and backend communication.
Deployment

The project is deployed using separate frontend and backend services.

Frontend Deployment

The frontend is deployed using Render.

The frontend contains:

Customer ticket submission form
Admin dashboard
Search functionality
Filtering functionality
Ticket details interface
JavaScript API integration
Backend Deployment

The Flask REST API is deployed using Render.

The backend handles:

API requests
Input validation
Ticket classification
Database operations
Ticket retrieval
Ticket filtering
Ticket statistics
Ticket status updates
Database Deployment

The MySQL database is hosted using Aiven.

The backend connects to the Aiven MySQL database using environment variables.

Local Setup
1. Clone the Repository
git clone https://github.com/Jayalakshmi7/support-ticket-dashboard.git
2. Navigate to the Project
cd support-ticket-dashboard
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

For Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r backend/requirements.txt
6. Configure Environment Variables

Create a .env file inside the backend directory.

Example:

DB_HOST=your_database_host
DB_PORT=your_database_port
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name

Do not commit the .env file to GitHub.

7. Start the Backend

From the project root:

python backend/app.py

The backend will run locally at:

http://127.0.0.1:5000
8. Open the Customer Interface

Open:

frontend/index.html

This provides the customer ticket submission form.

9. Open the Admin Dashboard

Open:

frontend/dashboard.html

This provides the admin ticket management dashboard.

Testing

The application was tested for the following workflows:

Customer ticket submission
Required field validation
Input length validation
Automatic ticket classification
Category assignment
Priority assignment
Ticket database storage
Ticket retrieval
Ticket search
Category filtering
Priority filtering
Status filtering
Ticket details viewing
Ticket status updates
Dashboard statistics
Frontend and backend communication
Cloud database connectivity
Render deployment
Aiven MySQL connectivity
Example Workflow
1. Customer opens the ticket form
              |
              v
2. Customer enters support issue
              |
              v
3. Frontend sends POST /tickets
              |
              v
4. Flask validates the request
              |
              v
5. Ticket classifier determines
   category and priority
              |
              v
6. Ticket is stored in MySQL
              |
              v
7. Customer receives ticket ID
              |
              v
8. Admin opens dashboard
              |
              v
9. Admin searches or filters tickets
              |
              v
10. Admin updates ticket status
              |
              v
11. Dashboard statistics refresh
Future Improvements

The following features can be added in future versions:

User authentication
Admin login
Role-based access control
Ticket assignment to support agents
Pagination for large ticket datasets
Email notifications
Ticket attachments
Advanced analytics
Improved machine-learning based classification
Audit logs
Password-protected admin dashboard
Ticket history tracking
Limitations

The current version focuses on the core support ticket workflow.

Authentication and role-based access control are not included in the current version.

The project is intended as a full-stack portfolio project demonstrating:

Frontend development
Backend API development
Database integration
REST API communication
Basic classification
Cloud deployment
Technologies Used
Python
Flask
Flask-CORS
MySQL
HTML
CSS
JavaScript
REST API
Git
GitHub
Render
Aiven
Repository

GitHub Repository:

https://github.com/Jayalakshmi7/support-ticket-dashboard

Live Application

Customer Ticket Form:

https://support-ticket-dashboard-frontend.onrender.com

Admin Dashboard:

https://support-ticket-dashboard-frontend.onrender.com/dashboard.html

Backend API:

https://support-ticket-dashboard-1.onrender.com