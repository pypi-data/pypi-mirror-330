from database import User, get_db_connection
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/users", methods=["GET"])
def get_users():
    """Get all users or filter by query parameters."""
    try:
        # Get query parameters
        active_only = request.args.get("active", "").lower() == "true"
        limit = request.args.get("limit", 100, type=int)

        # Get database connection
        db = get_db_connection()

        # Build query
        query = db.query(User)
        if active_only:
            query = query.filter(User.is_active is True)

        # Execute query with limit
        users = query.limit(limit).all()

        # Format response
        result = []
        for user in users:
            result.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "post_count": len(user.posts),
                }
            )

        return jsonify({"users": result})

    except Exception as e:
        app.logger.exception(f"Error fetching users: {e!s}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID."""
    try:
        db = get_db_connection()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get user's posts
        posts = []
        for post in user.posts:
            posts.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "created_at": post.created_at.isoformat(),
                }
            )

        # Format response
        result = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "posts": posts,
        }

        return jsonify(result)

    except Exception as e:
        app.logger.exception(f"Error fetching user {user_id}: {e!s}")
        return jsonify({"error": "Internal server error"}), 500
