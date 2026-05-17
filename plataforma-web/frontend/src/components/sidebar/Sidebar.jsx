import "./Sidebar.css"
import { NavLink } from "react-router-dom"
import routes from "../../constants/routes"

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1>AulaSmart</h1>
      </div>

      <nav className="sidebar-nav">
        {routes.map((route) => (
          <NavLink
            key={route.path}
            to={route.path}
            className={({ isActive }) =>
              isActive ? "sidebar-link active-link" : "sidebar-link"
            }
          >
            {route.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar