import './App.css'

function App() {
  const appVersion = import.meta.env.VITE_APP_VERSION || '0.1.0'
  const appName = import.meta.env.VITE_APP_NAME || 'PhD Progress Tracker'
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

  return (
    <>
      <div className="container">
        <h1>{appName}</h1>
        <p>Welcome to the PhD Progress Tracker application</p>
        <div className="info-box">
          <p>Version: {appVersion}</p>
          <p>API URL: {apiUrl}</p>
          <p>Status: Ready for development</p>
        </div>
      </div>
    </>
  )
}

export default App
