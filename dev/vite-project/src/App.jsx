import './App.css'
import { useState, useEffect } from 'react'
import ChessBoard from './components/ChessBoard'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5001/'; // Set Flask backend URL

function App() {
  const [inputValue, setInputValue] = useState('');
  const [gameStarted, setGameStarted] = useState(false);
  const [board, setBoard] = useState('8/8/8/8/8/8/8/8');
  const [computerMove, setComputerMove] = useState('');

  useEffect(() => {
    if (gameStarted) {
        startGame();
    }
}, [gameStarted]);

  const startGame = async () => {
    try {
      const response = await axios.post('/start_game');
      setBoard(response.data.board);
    } catch (error) {
      console.error('Error starting game:', error);
      alert('error starting game');
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyPress = async (e) => {
    if (e.key === 'Enter') {
      await handleSubmit();
    }
  };

  const handleSubmit = async () => {
    // player move
    try {
      const response = await axios.post('/make_player_move', { move: inputValue });
      setBoard(response.data.board);
      setInputValue('');

      // computer move
    try {
      const response = await axios.post('/make_computer_move');
      setBoard(response.data.board);
      setComputerMove(response.data.move);
      setInputValue('');
    } catch (error) {
      console.error('Error making move:', error);
    }

    } catch (error) {
      console.error('Error making move:', error);
      alert('Invalid move');
    }
  }

  return (
    <div className="app">
      <div className="text">
        <h1>ChipotleBot</h1>
        <h3>pay up,, sucker</h3>
      </div>
      {gameStarted ?
        <div className="game">
          <div className="board">
            <ChessBoard fen={board} />
            <input
              value={inputValue}
              onChange={handleInputChange}
              onKeyUp={handleKeyPress}
              placeholder="Type your move and press Enter"
            />
          </div>
          <div className="moves-grid">
            <div className="numbers column">
              <p>.</p>
              <p className="odd">1.</p>
              <p>2.</p>
              <p className="odd">3.</p>
            </div>
            <div className="my-moves column">
              <p>My Move</p>
              <p className="odd">e4</p>
              <p>Qxg7</p>
              <p className="odd">Rhe3</p>
            </div>
            <div className="chipotle-moves column">
              <p>ChipotleBot's Move</p>
              <p className="odd">.{computerMove}</p>
              <p>e5</p>
              <p className="odd">gxe7</p>
            </div>
          </div>
          
        </div>
      : <button className="start-game" onClick={() => setGameStarted(true)}>
          Start Game
        </button>}
    </div>
  );
}

export default App;

{/* 
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
*/}