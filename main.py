#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import init_login, app

if __name__ == '__main__':
    init_login()
    app.run(debug=True, port=8080)
