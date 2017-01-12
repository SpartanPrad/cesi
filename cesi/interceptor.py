import sqlite3
import time
from cesi import Config,CONFIG_FILE


class Interceptor(object):
    def __init__(self, app):
        self.app = app
        self.expiry_limit = 600.0

    def get_db(self):
        DATABASE = Config(CONFIG_FILE).getDatabase()
        conn = sqlite3.connect(DATABASE)
        return conn

    def auth_list_operation(self, mobile_number, operation='select'):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            if operation.lower() == 'delete':
                cur.execute("delete from otp where MOBILE=?", (int(mobile_number),))
                conn.commit()
            else:
                cur.execute("select * from otp where MOBILE=?", (int(mobile_number),))
            return cur.fetchall()
        except Exception as ex:
            print ex
        finally:
            conn.close()

    def __call__(self, environ, start_response):
        if not (str(environ.get('PATH_INFO')).startswith("/mobile") or str(environ.get('PATH_INFO')).startswith("/login")):
           if environ.get('HTTP_AUTHORIZATION') is not None:
                enc_auth_string = environ.get('HTTP_AUTHORIZATION')
                plain_auth_token = enc_auth_string.decode("base64")
                result_list = self.auth_list_operation(plain_auth_token.split(':')[0], operation='select')
                try:
                    if len(result_list) == 0:
                        raise Exception("No entries in otp table")
                    else:
                        if plain_auth_token.split(':')[1] != str(result_list[0][1]).decode('base64').split(':')[1]:
                            environ['PATH_INFO'] = '/denial'
                        else:
                            if time.time() - (result_list[0][2]/1000) > self.expiry_limit:
                                self.auth_list_operation(plain_auth_token.split(':')[0], operation='delete')
                                environ['PATH_INFO'] = '/token_expire'

                except Exception as ex:
                    print ex
                    environ['PATH_INFO'] = '/denial'

            #TODO for browser level filtering
            # else:
            #     print "Authorization needed for this operation"
            #     start_response('403 Permission Denied', [('Content-Type', 'application/json')])
            #     return ["Wrong OTP"]
        return self.app(environ, start_response)


