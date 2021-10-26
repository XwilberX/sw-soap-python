# Application is the glue between one or more service definitions, interface and protocol choices.

from spyne import Application

# @rpc decorator exposes methods as remote procedure calls

# and declares the data types it accepts and returns

from spyne import rpc

# spyne.service.ServiceBase is the base class for all service definitions.

from spyne import ServiceBase

# The names of the needed types for implementing this service should be self-explanatory.

from spyne import Iterable, Integer, Unicode, Li   


from spyne.protocol.soap import Soap11

# Our server is going to use HTTP as transport, It’s going to wrap the Application instance.

from spyne.server.wsgi import WsgiApplication


# step1: Defining a Spyne Service

class HelloWorldService(ServiceBase):

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):

        for i in range(times):

            yield u'Hello, %s' % name

    @rpc(Integer(nillable=False), Integer(nillable=False), _returns=Integer)
    def sum(ctx, a, b):
        return int(a + b)


# step2: Glue the service definition, input and output protocols
soap_app = Application([HelloWorldService], 'spyne.examples.hello.soap',

                       in_protocol=Soap11(validator='lxml'),

                       out_protocol=Soap11())


# step3: Wrap the Spyne application with its wsgi wrapper

wsgi_app = WsgiApplication(soap_app)


if __name__ == '__main__':

    import logging

    from wsgiref.simple_server import make_server

    # configure the python logger to show debugging output

    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")

    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    # step4:Deploying the service using Soap via Wsgi

    # register the WSGI application as the handler to the wsgi server, and run the http server

    server = make_server('127.0.0.1', 8000, wsgi_app)

    server.serve_forever()
