
import xmlrpclib

from user import user_blueprint
from config import app,HOST
from operations import operations_blueprint



try:
    if __name__ == '__main__':
        app.register_blueprint(user_blueprint)
        app.register_blueprint(operations_blueprint)
        app.run(debug=True, use_reloader=True, host=HOST)
except xmlrpclib.Fault as err:
    print "A fault occurred"
    print "Fault code: %d" % err.faultCode
    print "Fault string: %s" % err.faultString
