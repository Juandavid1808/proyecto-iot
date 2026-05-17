import "./SensorCard.css";

const SensorCard = ({
  title,
  value,
  unit,
  type,
}) => {

  return (
    <div className={`sensor-card ${type}`}>

      <div className="sensor-card-header">

        <h3>
          {title}
        </h3>

      </div>

      <div className="sensor-card-body">

        <h1>
          {value}
        </h1>

        <span>
          {unit}
        </span>

      </div>

    </div>
  );
};

export default SensorCard;