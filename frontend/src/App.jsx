import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Books from "./pages/Books"
import MyReservations from "./pages/MyReservations";
import MyLateBooks from "./pages/MyLateBooks";
import MyNotifications from "./pages/MyNotifications";
import LoginPage from './pages/LoginPage';
import BooksPage from './pages/BooksPage';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import ProtectedRoute from './components/ProtectedRoute';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<Home />} />
        <Route path="/books" element={<ProtectedRoute><BooksPage /></ProtectedRoute>} />
        <Route path="/reservations" element={<ProtectedRoute><MyReservations /></ProtectedRoute>} />
        <Route path="/late" element={<ProtectedRoute><MyLateBooks /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><MyNotifications /></ProtectedRoute>} />
      </Routes>
    </Router>
  )
}

export default App
