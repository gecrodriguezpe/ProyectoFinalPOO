# Proyecto final POO - G33 

## Integrantes del proyecto 
- Andrew Nicolay Prieto Mendoza: aprietome@unal.edu.co
- Ary Sofia Thyme Santos: athymes@unal.edu.co
- Jesus David Manrique Rios: jemanrique@unal.edu.co
- German Camilo Rodriguez Perilla: gecrodriguezpe@unal.edu.co

## Tareas

### Semana 1: 
- David y Nicolay: Crear la base de datos en SQLite
- Germán y Sofia: Modificar la plantilla del proyecto

### Semana 2: 

#### Botones
- Germán: Realizar la funcionalidad del Botón **Guardar** que incluya lo del autoincremental
- Nicolay: Realizar la funcionalidad del Botón **Editar** que incluya lo del cambio de botón
- David: Realizar la funcionalidad del Botón **Eliminar** que incluya la ventana externa con las dos opciones:
  - Elminar una asignatura específica
  - Elminar toda la inscripción  
- Sofía: Revisar el Notion con toda la documetnación relacionada con POO, tkinter, SQLite y las grabaciones de Fernando sobre el proyecto

##### Botón Eliminar
- Se oprime el botón **Eliminar**. Aparecé un menú con dos opciones: 1) *Eliminar Curso* o 2) *Eliminar inscripción*
  1. Si oprime *Eliminar curso*
    - Sale una ventana emergente que le pide por favor que seleccione el curso que desea eliminar y que vuelva a oprimir el botón eliminar 
    - Luego de seleccionar el curso que desea eliminar vuelve a oprimir el botón eliminar
      - Le aparece una ventana emergente que le pregunté sí desea confirmar la acción: 1) *Sí* o 2) *No*
          - *Sí*: Elimina la inscripción
          - *No*: Cancela la acción
  2. Si oprime *Eliminar inscripción* le debe aparecer una ventana emergente que le pregunté sí desea confirmar la acción: 1) *Sí* o 2) *No*
    - *Sí*: Elimina la inscripción
    - *No*: Cancela la acción
#### Mecanismo validacion de fechas

- validacion_Dias_Mes_Año(self, d, m, a): 

- Esta función valida si una fecha dada (día, mes, año) es válida. Veamos paso a paso cómo funciona:

  - if a <= 1754:: Verifica si el año es menor o igual a 1754. Si es así, muestra un mensaje de error indicando que solo se permiten años superiores a 1754 y devuelve False.
  - if not (1 <= m <= 12):: Verifica si el mes está dentro del rango válido (entre 1 y 12). Si no lo está, muestra un mensaje de error indicando que solo se permiten meses entre 1 y 12 y devuelve False.
  - Si el mes es uno de los meses que tienen 31 días (enero, marzo, mayo, julio, agosto, octubre o diciembre), verifica si el día está dentro del rango válido (entre 1 y 31) para estos meses. - Si no lo está, muestra un mensaje de error específico para el mes correspondiente y devuelve False.
  - Si el mes es febrero, verifica si el año es bisiesto. Si lo es, verifica si el día está dentro del rango válido (entre 1 y 29) para febrero en un año bisiesto. Si no lo es, muestra un mensaje de error específico para febrero en un año bisiesto. Si el año no es bisiesto, verifica si el día está dentro del rango válido (entre 1 y 28) para febrero en un año no bisiesto. Si no lo está, muestra un mensaje de error específico para febrero en un año no bisiesto.
  - Si el mes no es ni uno de los meses con 31 días ni febrero, se asume que es uno de los meses con 30 días. Verifica si el día está dentro del rango válido (entre 1 y 30) para estos meses. - Si no lo está, muestra un mensaje de error específico para el mes correspondiente y devuelve False.
  - Si la fecha pasa todas las validaciones anteriores, devuelve True, indicando que la fecha es válida.

- validar_fecha(self, event=None): 
  - Esta función obtiene la fecha del campo de entrada (self.fecha) y luego divide la fecha en día, mes y año. Luego llama a la función validacion_Dias_Mes_Año() con los componentes de fecha. - Si la función de validación devuelve False, significa que la fecha no es válida y se borra la entrada del campo de fecha. Si la función de validación devuelve True, la fecha es válida y no se hace nada. Esta función puede vincularse a un evento específico, como la pérdida de foco del campo de entrada, para validar automáticamente la fecha cuando el usuario complete la entrada.

#### Mecanismo de deteccion año biciesto

Un año es bisiesto si cumple con las siguientes condiciones:

1. Es divisible por 4.
2. Si es divisible por 100, también debe ser divisible por 400.

Vamos a analizar estas condiciones más detalladamente:

1. **Divisible por 4:** Esto significa que el año tiene un día adicional en febrero. Por ejemplo, el año 2020 es divisible por 4, por lo que es bisiesto, y febrero de ese año tiene 29 días.

2. **Divisible por 100 y 400:** Esta condición es una excepción a la primera. Si un año es divisible por 100 pero no por 400, no es bisiesto. Esto significa que, aunque un año sea divisible por 4, si es divisible por 100 pero no por 400, no es considerado bisiesto. Por ejemplo, el año 1900 fue divisible por 100 pero no por 400, por lo que no fue bisiesto, a pesar de ser divisible por 4.

Por lo tanto, el cálculo de si un año es bisiesto puede hacerse de la siguiente manera:

```python
es_bisiesto = (a % 4 == 0) and (a % 100 != 0 or a % 400 == 0)
```

En esta expresión:

- `(a % 4 == 0)`: Verifica si el año es divisible por 4.
- `(a % 100 != 0 or a % 400 == 0)`: Verifica si el año no es divisible por 100 o si es divisible por 400. Si cumple esta condición, el año es bisiesto.

Esta expresión `es_bisiesto` será `True` si el año cumple ambas condiciones y `False` si no las cumple. Entonces, esta variable se usa para determinar si febrero debe tener 28 o 29 días en el caso de la validación de la fecha.

## Estandarización del código 
- Comentarios:
  - Comentarios simples: Colocarlos #
  - Docstring de funciones: Colocarlos con triple comilla ''' DOCSTRING ''' luego de la firma de la función

## Comentarios acerca del código
### Antacipn .bind

`.bind()` es un método en `Tkinter` que te permite asociar una función o método a un evento específico en un widget. Cuando se produce el evento especificado, la función asociada se ejecuta.

Por ejemplo, puedes usar `.bind()` para ejecutar una función cuando un botón es presionado, cuando se ingresa texto en un Entry, cuando se selecciona un elemento en un Combobox, entre otros eventos.

## Cosas adicionales que se le pueden agregar al proyecto 

1. Documentar de manera correcta las funciones del proyecto (docstring).
  - Que cada función contenga su DOCSTRING describiendo su funcionalidad, los parámetros y lo que retorna.
  - Ejemplo de función con DOCSTRING: 
  ```
  def sumar (num1, num2): 
    '''
    

    Parameters
    ----------
    num1 : TYPE
        DESCRIPTION.
    num2 : TYPE
        DESCRIPTION.

    Returns
    -------
    suma : TYPE
        DESCRIPTION.

    '''
    
    suma = num1 + num2
    
    return suma
  ```
