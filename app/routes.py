def register_routes(app, root="api"):
    from app.bot import register_routes as attach_bot

    # Add routes
    attach_bot(app=app, root=root)
