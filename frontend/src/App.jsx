
import Login from './pages/Login'
import Home from './pages/Home'
import Perfil from './pages/Perfil'
import './App.css'

function App() {
  const token = localStorage.getItem('token')

  const caminho = window.location.pathname

  if (!token) {
    return <Login />
  }

  if (caminho === '/perfil') {
    return <Perfil />
  }

  return <Home />
}

export default App

