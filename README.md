# Analizador de Representación de Datos - Django

Proyecto desarrollado para la asignatura de Arquitectura y Organización de Computadoras (UTH). La aplicación permite realizar conversiones numéricas entre distintas bases y analizar la codificación de texto en formato UTF-8.

## Integrante
* Dilber Alexander Betanco Ordoñez

---

## Instrucciones de Ejecución con Docker

1. **Construir e iniciar el contenedor:**
```bash
docker compose up --build
```

2. **Acceder a la aplicación desde el navegador:**

   ```URL: http://localhost:8000/```

3. **Verificar el límite de recursos (256 MB de RAM y 1 CPU):**

```bash
docker stats analizador_datos_app
```


## Explicación Técnica y Arquitectura
### Uso de Recursos de la Arquitectura de Von Neumann
La aplicación web interactúa con los componentes del modelo de Von Neumann de la siguiente manera:

I. Memoria Principal (RAM): Almacena el código ejecutable de Python/Django, las estructuras de datos temporales (como los textos y números ingresados) y guarda en sesión los resultados procesados antes de enviarlos a la vista HTML.

II. CPU (Unidad Central de Procesamiento): La ALU realiza las operaciones aritméticas de conversión entre bases (divisiones sucesivas, desplazamientos), mientras que la Unidad de Control gestiona el flujo del ciclo de instrucción (Fetch-Decode-Execute) al interpretar nuestro código en Python.

III. Entrada / Salida (E/S): Las peticiones HTTP ingresadas en los formularios web actúan como los datos de entrada, y las respuestas renderizadas en pantalla con las tablas numéricas son las salidas.

## ¿Por qué el contenedor de Docker comparte el kernel del Host?

A diferencia de una máquina virtual pesada que requiere instalar un sistema operativo invitado completo, los contenedores utilizan la tecnología de aislamiento de procesos de Linux (Namespaces para aislar la red y los procesos, y Cgroups para limitar los recursos como los 256MB de RAM). Esto permite que el contenedor ejecute sus procesos directamente sobre el kernel del sistema host, compartiendo sus llamadas al sistema (syscalls). Esto hace que la aplicación sea extremadamente ligera, rápida y consuma los recursos mínimos necesarios.
