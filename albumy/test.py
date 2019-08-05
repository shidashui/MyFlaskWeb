from albumy import create_app, whooshee

if __name__=='__main__':
    app = create_app()
    # print(app.config)
    app.run()