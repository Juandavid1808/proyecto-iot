import "./AlertTable.css"

function AlertTable({ alertas }) {

  return (

    <div className="table-container">

      <table className="alert-table">

        <thead>

          <tr>
            <th>Sensor</th>
            <th>Mensaje</th>
            <th>Nivel</th>
            <th>Fecha</th>
          </tr>

        </thead>

        <tbody>

          {alertas.map((alerta) => (

            <tr key={alerta.id}>

              <td>
                {alerta.tipo_sensor}
              </td>

              <td>
                {alerta.mensaje}
              </td>

              <td>
                {alerta.nivel}
              </td>

              <td>
                {new Date(
                  alerta.timestamp
                ).toLocaleString()}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  )
}

export default AlertTable