# 1. Encuentra y resuelve el error

Al ejecutar los tests con el siguiente comando

> make test/all

Puede observarse que falla un test. Ecuentra y resuelve el error.

# 2. Añadimos autenticación y autorización.

Casos de uso:
  - Como usuario quiero crear un documento:
    - Escenario: Alta de un documento
      - Dado un usuario válido
      - Cuando inserto un documento
      - Entonces se crea correctamente
      - Y yo puedo consultarlo
      - Y otros usuario no puede consultarlo
  - Como usuario quiero consultar todos mis documentos
    - Escenario: Como usuario quiero consultar todos mis documentos
      - Dado un usuario válido
      - Y existen documentos de diferentes usuarios
      - Cuando consulto todos los documentos
      - Enconces recupero una lista de documento
      - Y la lista sólo contiene mis documentos
    - Escenario: Como usuario quiero consultar un documento ajeno
      - Dado un usuario válido
      - Y existe al menos un documento ajeno
      - Cuando consulto el documento
      - Entonces la respuesta es 403
  - Como usuario quiero borrar un documento
    - Escenario: Como usuario quiero borrar mi documento
      - Dado un usuario valido
      - Y un documento existente
      - Cuando borro el documento
      - Este es borrado
      - Y no existe en el bucket
    - Escenario: Como usuario quiero borrar un documento ajeno
      - Dado un usuario valido
      - Y un documento existente de otro usuario
      - Cuando borro el documento
      - Recibo un 403
      - Y este no ha sido borrado de la base de datos