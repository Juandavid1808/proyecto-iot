import "./AlertCard.css";

const AlertCard = ({ alerta }) => {

  const alertClass =
    alerta.nivel === "critica"
      ? "danger"
      : alerta.nivel === "media"
      ? "warning"
      : "normal";

  return (
    <div
      className={`alert-card ${alertClass}`}
    >

      <div className="alert-header">

        <h3>
          {alerta.tipo}
        </h3>

        <span className="alert-level">
          {alerta.nivel}
        </span>

      </div>

      <p className="alert-message">
        {alerta.mensaje}
      </p>

      <div className="alert-footer">

        <span>
          Sensor:
          {" "}
          {alerta.sensor}
        </span>

        <span>
          {alerta.fecha}
        </span>

      </div>

    </div>
  );
};

export default AlertCard;