from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    # Tambahkan host="0.0.0.0" agar server Nginx kampus bisa mengaksesnya
    # Ubah debug=False untuk keamanan server (Production mode)
    app.run(host="0.0.0.0", port=int(Config.APP_PORT), debug=False)