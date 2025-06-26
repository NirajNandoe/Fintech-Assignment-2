# Topic tags: authentication, authorization, user roles

# This function simulates a logged-in user for the MVP demo. This user is assigned a role of "accountant".
# In a real application, you would retrieve the user from a session or token.
def get_current_user():
    return {"id": "demo_user", "role": "accountant"}

# This function includes a simple access control check based on the user's role. 
# The functionn returns true if the user has the required role or is an admin, otherwise it returns false.
# This function allows for the authentication and authorization of users in the application.
def check_access(required_role):
    user = get_current_user()
    if user["role"] != required_role and user["role"] != "admin":
        return False
    return True
