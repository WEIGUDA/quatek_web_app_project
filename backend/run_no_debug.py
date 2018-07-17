from app import create_app, socketio
app = create_app({'DEBUG': False, 'ENV': 'production'})

if __name__ == "__main__":
    socketio.run(app)
