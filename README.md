# Documentación del Proyecto: Migración de API en Memoria a Base de Datos con FastAPI y SQLModel

Este documento registra la evolución, arquitectura y el proceso de desarrollo de nuestra API de gestión de clientes, facturas y transacciones utilizando **FastAPI**. El proyecto comenzó utilizando estructuras de datos volátiles (listas en memoria) y evolucionó hacia una solución robusta y persistente utilizando el ORM **SQLModel** (basado en SQLAlchemy y Pydantic).

---

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Fase 1: Arquitectura Inicial en Memoria](#fase-1-arquitectura-inicial-en-memoria)
3. [Fase 2: Transición a Base de Datos con SQLModel](#fase-2-transición-a-base-de-datos-con-sqlmodel)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Modelos de Datos (SQLModel)](#modelos-de-datos-sqlmodel)
6. [Enrutadores (Endpoints de la API)](#enrutadores-endpoints-de-la-api)
7. [Errores Comunes y Soluciones (Lecciones Aprendidas)](#errores-comunes-y-soluciones-lecciones-aprendidas)

---

## 1. Descripción General
El sistema es una API REST diseñada para la administración de un flujo de facturación estándar. Permite realizar operaciones CRUD completas sobre tres entidades principales estrechamente relacionadas:
* **Clientes:** Entidades individuales que reciben facturas.
* **Facturas:** Comprobantes emitidos a un cliente específico.
* **Transacciones:** Ítems individuales o movimientos asociados a una factura (relación uno a muchos).

---

## 2. Fase 1: Arquitectura Inicial en Memoria
En la primera etapa del desarrollo, con el fin de prototipar rápidamente las rutas y la lógica de negocio, se utilizaron listas nativas de Python (`list`) almacenadas en un archivo centralizado (`listas.py`).

### Características de la Fase 1:
* **Almacenamiento Volátil:** Datos como `lista_clientes`, `lista_facturas` y `lista_transacciones` residían en la memoria RAM del servidor. Al reiniciar Uvicorn, toda la información se borraba.
* **Lógica Manual:** Para operaciones de búsqueda (`GET` por ID), edición (`PATCH`) o eliminación (`DELETE`), se requería el uso de bucles explícitos `for` combinados con `enumerate()` para alterar los índices de las listas.
* **Desventajas:** Cero persistencia, vulnerabilidad a condiciones de carrera (race conditions) y falta de integridad referencial automática entre llaves foráneas.

---

## 3. Fue 2: Transición a Base de Datos con SQLModel
Para solventar las limitaciones de la fase en memoria, el proyecto migró hacia **SQLModel**, una librería diseñada por el creador de FastAPI que unifica el modelado de datos de **Pydantic** (validación de esquemas) con las capacidades relacionales de **SQLAlchemy** (ORM).

### Beneficios Clave:
* **Persistencia Real:** Los datos se escriben y leen desde un motor de base de datos relacional de manera transparente.
* **Inyección de Dependencias:** Implementación de `sesion_dependencia` para abrir y cerrar conexiones de manera segura por cada ciclo de solicitud/respuesta HTTP (`Session`).
* **Relaciones Complejas:** Automatización de llaves foráneas (`ForeignKey`) y propiedades de navegación relacional (`Relationship`) con carga perezosa (lazy loading).

---

## 4. Estructura del Proyecto
El código se encuentra modularizado separando los esquemas/tablas de la lógica de los controladores o rutas HTTP:

```text
app/
├── conexion_bd.py       # Configuración del motor y la sesión (sesion_dependencia)
├── listas.py            # Listas antiguas de memoria (en proceso de depreciación)
├── modelos/             # Modelos de definición de Tablas y Esquemas
│   ├── clientes.py
│   ├── facturas.py
│   └── transacciones.py
└── enrutadores/         # Definición de las rutas HTTP (APIRouter)
    ├── clientes.py
    ├── facturas.py
    └── transacciones.py
```

---

## 5. Modelos de Datos (SQLModel)
A continuación, se detalla la configuración correcta de los modelos ORM para garantizar la integridad referencial y evitar conflictos de inicialización.

### Clientes (`app/modelos/clientes.py`)
Representa la entidad independiente. Un cliente puede tener múltiples facturas.
```python
class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str

    # Relación inversa: Un cliente tiene muchas facturas
    facturas: list["Factura"] = Relationship(back_populates="cliente")
```

### Facturas (`app/modelos/facturas.py`)
Entidad intermedia. Pertenece a un cliente y agrupa múltiples transacciones.
```python
class Factura(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int | None = Field(default=None, foreign_key="cliente.id")
    vr_total: float = Field(default=0.0)

    # Relaciones
    cliente: "Cliente" = Relationship(back_populates="facturas")
    transacciones: list["Transaccion"] = Relationship(back_populates="factura")
```

### Transacciones (`app/modelos/transacciones.py`)
Entidad dependiente. Cada transacción se vincula a una única factura.
```python
class Transaccion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    descripcion: str = Field(default=None)

    factura_id: int | None = Field(default=None, foreign_key="factura.id")

    # Relación: Una transacción pertenece a UNA sola Factura
    factura: "Factura" = Relationship(back_populates="transacciones")
```

---

## 6. Enrutadores (Endpoints de la API)
Los enrutadores exponen las operaciones CRUD utilizando las sesiones inyectadas de la base de datos en lugar de la memoria global.

### Ejemplo de Enrutador de Clientes (`rutas_clientes`)
Migrado al 100% al uso de la base de datos transaccional:
* `GET /clientes`: Obtiene la lista completa mediante `sesion.exec(select(Cliente)).all()`.
* `POST /clientes`: Valida el payload de entrada con `model_validate`, añade el registro a la sesión mediante `.add()` y confirma con `.commit()`.
* `PATCH /clientes/{id}`: Utiliza `.sqlmodel_update()` para actualizar parcialmente campos mutados.
* `DELETE /clientes/{id}`: Busca la entidad con `.get()` y la remueve usando `.delete()`.

### Ejemplo de Enrutador de Facturas (`rutas_facturas`)
Maneja esquemas compuestos (`FacturaLeerCompuesta`) para anidar información relacional en las respuestas JSON y realiza validaciones lógicas antes de insertar datos, verificando previamente si el `cliente_id` existe en el sistema.

---

## 7. Errores Comunes y Soluciones (Lecciones Aprendidas)

### ❌ El Error: `sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize...`
* **Causa:** Este error crítico ocurría porque en el modelo ORM de `Transaccion`, la propiedad relacional `factura` estaba definida erróneamente bajo el tipo de dato `list["factura"]` o apuntaba a nombres en minúsculas inapropiados. Al usar `list[...]`, el ORM intentaba mapear una relación de múltiples elementos en vez de un mapeo directo de clase uno a uno, confundiéndose con objetos `Table` puros.
* **Solución:** Se corrigió la anotación del tipo de dato en el modelo relacional a `"Factura"` como un literal de texto plano (String) en singular, lo que le permite a SQLModel resolver la clase ORM de manera tardía sin generar errores de mappers ni problemas de importaciones circulares en Python.

### ❌ Uso Mixto de Memoria y Sesiones de Base de Datos
* **Síntoma:** Rutas como `CrearTransaccion` guardaban datos correctamente en la BD física a través de `sesion.add()`, pero rutas vecinas como `EditarTransaccion` o `EliminarTransaccion` seguían iterando sobre arreglos locales mediante bucles `for transaccion in lista_transacciones:`. Esto causaba una desincronización crítica.
* **Solución:** Homogeneizar todos los endpoints de los archivos de rutas para que acepten el parámetro `sesion: sesion_dependencia` y realicen las consultas SQL de manera homogénea.
