from gate import create_app

import config

app = create_app('config')

if __name__ == "__main__":
    dic = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    app.run(**dic)