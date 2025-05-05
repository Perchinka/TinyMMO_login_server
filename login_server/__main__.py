if __name__ == "__main__":
    import uvicorn
    from login_server.app import create_app

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
