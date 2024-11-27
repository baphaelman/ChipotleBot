import './App.css'
import { useState, useEffect } from 'react'
import ChessBoard from './components/ChessBoard'

function App() {
  const [inputValue, setInputValue] = useState('');
  const [gameStarted, setGameStarted] = useState(false);

  useEffect(() => {
    if (gameStarted) {
      startGame();
    }
  }, [gameStarted])

  const startGame = () => {
    console.log('game started lol');
  }

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
      <button className="start-game" onClick={() => setGameStarted(true)}>
        Start Game
      </button>
      {gameStarted ? <div className="board"> <ChessBoard /> </div>
      : null}
      <input
        value={inputValue}
        onChange={handleInputChange}
        onKeyUp={handleKeyPress}
      />
    </div>
  )
}

export default App
