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
          1. *Sí*: Elimina la inscripción
          2. *No*: Cancela la acción
  2. Si oprime *Eliminar inscripción* le debe aparecer una ventana emergente que le pregunté sí desea confirmar la acción: 1) *Sí* o 2) *No*
    1. *Sí*: Elimina la inscripción
    2. *No*: Cancela la acción

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
