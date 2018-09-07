from app import app_factory

if __name__ == '__main__':
    app_factory().run(host='localhost', port=5000, debug=True)