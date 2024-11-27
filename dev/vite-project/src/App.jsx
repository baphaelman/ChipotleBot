import './App.css'
import { useState } from 'react'
import ChessBoard from './components/ChessBoard'

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }

  // this is where my code should interact with the backend in the chipotlebot code
  const handleSubmit = () => {
    console.log('Input value: ', inputValue);
    setInputValue('');
  }

  return (
    <div className="app">
      <div className="text">
        <h1>ChipotleBot</h1>
        <h3>pay up,, sucker</h3>
      </div>
      <div className="board">
        <ChessBoard />
      </div>
      <input
        value={inputValue}
        onChange={handleInputChange}
        onKeyUp={handleKeyPress}
      />
    </div>
  )
}

export default App
