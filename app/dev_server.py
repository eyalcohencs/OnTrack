import app

if __name__ == '__main__':
    server = app.create_app()
    server.run(port=8001)
