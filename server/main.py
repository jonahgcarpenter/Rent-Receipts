# server/
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

# TODO:

# 1. Add User Authentication
# 2. Link Users to Households
