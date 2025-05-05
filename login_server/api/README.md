HTTP interface layer.  
Translates external requests into service calls and handles error mapping.

**Key elements:**
- `controllers.py`: Request handlers that call into `UserService`.
- `routes.py`: Maps URLs to controller functions.
