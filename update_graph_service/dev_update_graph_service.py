import update_graph_service

if __name__ == '__main__':
    service = update_graph_service.create_app()
    service.run(port=8002)
