=========
chibi_api
=========


.. image:: https://img.shields.io/pypi/v/chibi_api.svg
        :target: https://pypi.python.org/pypi/chibi_api

.. image:: https://readthedocs.org/projects/chibi-api/badge/?version=latest
        :target: https://chibi-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




libreria para hacer clientes de apis rest

Ejemplos
--------

.. code-block:: python

	from chibi_requests import Response
	from chibi_api.chibi_api import Chibi_inner_api


	class Response_200( Response ):
		serializer = Catalog_serializer


	class Response_post( Response_200 ):
		pass


	class Response_put( Response_200 ):
		pass


	class Response_delete( Response_200 ):
		pass


	class Api_inner( Chibi_inner_api ):
		response = {
			'get': Response_200,
			'post': Response_post,
			'delete': Response_delete,
			'put': Response_put,
		}


* Free software: WTFPL
* Documentation: https://chibi-api.readthedocs.io.


Features
--------

* TODO
