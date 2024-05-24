import logo from './logo.svg';
import Login from './components/Login/Login';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
            <Routes>
                <Route path="/login" element={<Login/>} />
                <Route path="/" exact element={<Login/>} />
            </Routes>
        </Router>
  );
}

export default App;
