import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n==========================================")
    print(f"🎬 CineFlow Cinema Production Management")
    print(f"   Server running at http://127.0.0.1:{port}")
    print(f"==========================================\n")
    app.run(host='127.0.0.1', port=port, debug=True)
