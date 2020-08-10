DEBUG=True
SECRET_KEY='THISISSECRETKEY'
SQLALCHEMY_DATABASE_URI='postgresql://postgres:postre123@localhost/catelog_db'
#                            ⬆             ⬆         ⬆        ⬆          ⬆
#                        <database>://<userid>:<password>@<server>/<database_name>
SQLALCHEMY_TRACK_MODIFICATIONS=False

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
