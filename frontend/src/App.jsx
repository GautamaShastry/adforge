import Dashboard from "./pages/Dashboard"
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-logo">✨ AdForge AI</h1>
        <p className="app-tagline">Transform your product images into stunning video ads</p>
      </header>
      <Dashboard />
    </div>
  )
}

export default App
