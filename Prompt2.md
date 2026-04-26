<CRITICAL_REQUIREMENT>
You are an expert Python developer.

Implement backend code where:
ADMIN manages users, trainers, and system access.

The system MUST:
- Allow admin login
- View all users and trainers
- Create, update, delete accounts
- Enable/disable access
</CRITICAL_REQUIREMENT>

<CONTEXT>
Use Case (from SRS):
- Admin logs in
- Views list of users/trainers
- Adds, updates, removes accounts
- System saves and confirms success

Errors:
- Invalid login → deny access
- DB failure → show error
</CONTEXT>

<REITERATION>
REMEMBER:
The code MUST include:
- CRUD operations for users and trainers
- Access control (enabled/disabled accounts)
- Proper exception handling
</REITERATION>