import { BrowserRouter , Route, Routes } from "react-router-dom";
import Dashboard from "./pages/results.jsx";

function App() {

  return (
    <BrowserRouter>
    <Routes>
      {/* <Route path="/" element={<Home />} /> */}
      {/* <Route path="/about" element={<About />} /> */}
      <Route path="/" element={<Dashboard />} />
      
    </Routes>
    </BrowserRouter>
  )
}

export default App
