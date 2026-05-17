import "./MainLayout.css"

import { Outlet } from "react-router-dom"

import Sidebar from "../components/sidebar/Sidebar"
import Navbar from "../components/navbar/Navbar"

function MainLayout() {
  return (
    <div className="layout">
      <Sidebar />

      <div className="main-section">
        <Navbar />

        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout