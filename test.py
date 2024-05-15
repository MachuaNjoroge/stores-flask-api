import functools

user = {"username": "jose", "level": "admin"}


def make_secure(level):
  def decorator(func):
      @functools.wraps(func)
      def secure_function(*args, **kwargs):
          if user["level"] == level:
              return func(*args, **kwargs)
          else:
              return f"No admin permissions for {user["username"]}"
      return secure_function
  return decorator
  

@make_secure("admin")
def get_admin_password():
    return "admin: 1234"

@make_secure("user")
def get_dashboard_password():
    return "user: user_password"

print(get_admin_password())

