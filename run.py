from app import app
from app import views

if __name__ == '__main__':
    port = 8000
    app.run(host='0.0.0.0', port=port,debug=True)
