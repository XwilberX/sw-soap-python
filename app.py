# Application is the glue between one or more service definitions, interface and protocol choices.

from spyne import Application

# @rpc decorator exposes methods as remote procedure calls

# and declares the data types it accepts and returns

from spyne import rpc

# spyne.service.ServiceBase is the base class for all service definitions.

from spyne import ServiceBase

# The names of the needed types for implementing this service should be self-explanatory.

from spyne import Iterable, Integer, Unicode, Integer32, TTableModel, UnsignedInteger32, Mandatory
from spyne.error import ResourceNotFoundError
from spyne.protocol.soap import Soap11

# Our server is going to use HTTP as transport, It’s going to wrap the Application instance.

from spyne.server.wsgi import WsgiApplication

# database sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

# Initialize SQLAlchemy Environment
db = create_engine('sqlite:///moviles.db')
Session = sessionmaker(bind=db)
session = Session()

TableModel = TTableModel()
TableModel.Attributes.sqla_metadata.bind = db

class Moviles(TableModel):
    __tablename__ = 'moviles'

    id = Integer32(primary_key=True, nullable=False)
    marca = Unicode(50)
    linea = Unicode(50)
    modelo = Unicode(50)
    color = Unicode(70)
    ram = Integer32()

TableModel.Attributes.sqla_metadata.create_all(checkfirst=True)


# step1: Defining a Spyne Service

class MovilesServiceCRUD(ServiceBase):

    @rpc(Moviles, _returns=UnsignedInteger32)
    def create(ctx, movile):
        print(movile)
        new_movile = Moviles(marca = movile.marca, linea = movile.linea, modelo = movile.modelo, color = movile.color, ram = movile.ram)
        session.add(new_movile)
        session.commit()

        return 1

    @rpc(Mandatory(UnsignedInteger32))
    def delete(ctx, movil_id):
        count = session.query(Moviles).filter_by(id=movil_id).count()
        if count == 0:
            raise ResourceNotFoundError(movil_id)

        session.query(Moviles).filter_by(id=movil_id).delete()
        session.commit()

    @rpc(_returns=Iterable(Moviles))
    def get_all(ctx):
        return session.query(Moviles)


# step2: Glue the service definition, input and output protocols
soap_app = Application([MovilesServiceCRUD], 'spyne.examples.sql_crud',

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
    logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")

    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    # step4:Deploying the service using Soap via Wsgi

    # register the WSGI application as the handler to the wsgi server, and run the http server

    server = make_server('127.0.0.1', 8000, wsgi_app)

    server.serve_forever()