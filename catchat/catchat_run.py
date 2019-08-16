from catchat import create_app


if __name__=='__main__':
    app = create_app()
    # print(app.config)
    app.run()