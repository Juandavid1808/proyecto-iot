-- Monitoreo IoT
-- Líder de Infraestructura: Karen
-- Descripción: Estructura de la tabla para recibir datos de sensores

CREATE TABLE monitoreo_maqueta (
  -- Llave primaria automática para orden de registros
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  
  -- Datos de sensores (Santiago)
  temperatura FLOAT,       -- Del sensor DHT22
  humedad FLOAT,           -- Del sensor DHT22
  nivel_luz INTEGER,       -- Del sensor LDR (vía multiplexor)
  nivel_sonido INTEGER,    -- Del sensor KY-038 (vía multiplexor)
  movimiento BOOLEAN,      -- Del sensor PIR HC-SR501
  
  -- Registro de tiempo
  fecha_registro TIMESTAMPTZ DEFAULT NOW()
);
