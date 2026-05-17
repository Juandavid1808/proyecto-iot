const DeviceCard = ({
  nombre,
  activo,
  sensores,
}) => {
  return (
    <div className="device-card">
      <h3>{nombre}</h3>

      <p>
        Estado:
        <span
          className={
            activo
              ? "status active"
              : "status inactive"
          }
        >
          {activo ? " Activo" : " Inactivo"}
        </span>
      </p>

      <p>
        Sensores activos: {sensores}
      </p>
    </div>
  );
};

export default DeviceCard;