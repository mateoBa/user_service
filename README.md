# User API

Servicio para el tratamiento de usuarios con ventas asociadas. 

La idea es correr este servicio con un container de Docker. Por el momento, la conexión con mongodb no esta funcionando correctamente. Es mi primer paso con Docker, si tienen algun consejo o advertencia se lo voy a agradecer.


### Instalación como en la vieja escuela
Se deberá instalar mongodb y tenerlo levantado al momento del uso del servicio (service mongod start)

```sh
$ cd user_service
$ pip install -r requirements.txt
$ python ./service.py
```

### Requests al servicio con libreria de python requests
1. Crear usuario:
```sh
$ data = {'email': 'mateobasaldua@gmail.com', 'name': 'Mathew', 'last_name': 'Basaldua', 'address': 'Zabala'}
$ requests.post('http://127.0.0.1:5000/api/users', json=data)
```

2. Por defecto el usuario se crea desaprobado, para aprobarlo:
```sh
$ requests.get('http://127.0.0.1:5000/api/approve_user/mateobasaldua@gmail.com')
``` 

3. Modificar un usuario, indicando email:
```sh
$ data = {'email': 'mateobasaldua@gmail.com', 'name': 'Mateo', 'last_name': 'Basa', 'address': 'Zabala 2472'}
$ requests.put('http://127.0.0.1:5000/api/users', json=data)
```

4. Deshabilitar un usuario indicando email:
```sh
$ requests.get('http://127.0.0.1:5000/api/deactivate_user/mateobasaldua@gmail.com')
``` 

5. Crear una venta asociada a un usuario:
```sh
$ data = {'uuid': '889e068d-b098-4da2-82dd-4c712a0446b6', 'user_email': 'mateobasaldua@gmail.com', 'amount': 123.45, 'date': '2017-10-15 11:35'}
$ requests.post('http://127.0.0.1:5000/api/users/save_sale', json=data)
```
Nos tira error porque para crear una venta el usuario tiene que estar aprobado. Por lo ejecutamos el paso 2 y despues volvemos a ejecutar este paso.
La venta se crea por defecto en estado aprobado. La suma de todas las ventas aprobadas se muestra en la descripción del usuario.

6. Anular una venta indicando su identificador único:
```sh
$ requests.get('http://127.0.0.1:5000/api/deactivate_sale/889e068d-b098-4da2-82dd-4c712a0446b6')
``` 

7. Listar todos los usuarios:
Mi preferido es ingresar en el navegador a http://127.0.0.1:5000/api/users
Por consola:
```sh
$ response = requests.get('http://127.0.0.1:5000/api/users')
$ print(response.content)
``` 

8. Mostrar descripción de un usuario: http://127.0.0.1:5000/api/users/mateobasaldua@gmail.com

9. Consultar la lista de ventas de un usuario: http://127.0.0.1:5000/api/sales/mateobasaldua@gmail.com
```sh
$ response = requests.get('http://127.0.0.1:5000/api/sales/mateobasaldua@gmail.com')
$ print(response.content)
``` 
