Proyecto de Monitoreo Ambiental - IoT

Este repositorio centraliza el desarrollo del sistema de monitoreo ambiental. Aquí se integra el hardware (IoT), la base de datos (Nube) y la interfaz de usuario (Plataforma Web).

## Equipo de Nube y Roles

*   **Juan David (Líder de Proyecto):** Gestión de este repositorio, integración de servicios y comunicación entre líderes de área (Santiago y Rafael).
*   **Luis:** Administrador Cloud. Responsable de la creación del proyecto en Supabase e invitación de miembros.
*   **Karen:** Diseñadora de Datos. Encargada de estructurar las tablas según los requerimientos técnicos.
*   **Juan José:** Tester (QA). Encargado de validar la llegada de datos a la nube mediante Postman.
*   **Andrey:** Arquitecto Visual. Responsable del diagrama de arquitectura.

## Estructura del Repositorio
Para mantener el orden entre los líderes de área, cada uno debe usar su carpeta:

*   `📁 /iot-sensor`: Código del ESP32 y sensores (Líder: Santiago).
*   `📁 /plataforma-web`: Código del Dashboard/Frontend (Líder: Rafael).
*   `📁 /nube-infra`: 
    *   `/database`: Esquemas de tablas de Karen.
    *   `/pruebas`: Evidencias de éxito de Juan José.
    *   `/arquitectura`: Diagramas de Andrey.

## 🛠️ Especificaciones Técnicas
*   **Base de Datos:** Supabase (PostgreSQL).
*   **Seguridad:** Uso obligatorio de RLS y protección de API Keys.
