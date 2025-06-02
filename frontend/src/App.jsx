import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Books from "./pages/Books"
import MyReservations from "./pages/MyReservations";
import MyLateBooks from "./pages/MyLateBooks";
import MyNotifications from "./pages/MyNotifications";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/books" element={<Books />} />
        <Route path="/reservations" element={<MyReservations />} />
        <Route path="/late" element={<MyLateBooks />} />
        <Route path="/notifications" element={<MyNotifications />} />



      </Routes>
    </BrowserRouter>
  )
}

export default App
