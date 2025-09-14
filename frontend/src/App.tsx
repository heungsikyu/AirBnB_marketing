import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Layout from './components/Layout.tsx'
import Dashboard from './pages/Dashboard.tsx'
import Properties from './pages/Properties.tsx'
import Analytics from './pages/Analytics.tsx'
import Settings from './pages/Settings.tsx'
import Notifications from './pages/Notifications.tsx'

function App() {
  return (
    <ThemeProvider>
      <Router
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true
        }}
      >
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/properties" element={<Properties />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/notifications" element={<Notifications />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  )
}

export default App
