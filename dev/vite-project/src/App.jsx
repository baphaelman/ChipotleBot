import './App.css'
import { useState, useEffect, useRef } from 'react'
import ChessBoard from './components/ChessBoard'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5001/'; // Set Flask backend URL

function App() {
  const [inputValue, setInputValue] = useState('');
  const [gameStarted, setGameStarted] = useState(false);
  const [board, setBoard] = useState('8/8/8/8/8/8/8/8');
  const [numberList, setNumberList] =  useState([]);
  const [myMoves, setMyMoves] = useState([]);
  const [botMoves, setBotMoves] = useState([]);
  const [moveNumber, setMoveNumber] = useState(1);

  // for dragging and dropping
  const [startingSquare, setStartingSquare] = useState('');
  const [endingSquare, setEndingSquare] = useState('');

  const movesEndRef = useRef(null);

  // start game
  useEffect(() => {
    if (gameStarted) {
        startGame();
    }
}, [gameStarted]);

  // scroll new moves into frame
  useEffect(() => {
    scrollToBottom();
  }, [myMoves, botMoves]);

  useEffect(() => {
    if (startingSquare) {
      console.log('starting: ', startingSquare);
      console.log('ending: ', endingSquare);
      submitDraggingMove();
    }
  }, [endingSquare])

  {/*
  const makeDragMove = (e) => {
    if (startingSquare) {
    console.log(startingSquare);
      console.log(e.tile);
        setEndingSquare(e.tile);
        submitDraggingMove();
    }
  }
    */}

  const startGame = async () => {
    try {
      const response = await axios.post('/start_game');
      setBoard(response.data.board);
      console.log(board);
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

  const submitDraggingMove = async () => {
    // player move
    try {
      const response_player = await axios.post('/make_player_move_dragging', { move: `${startingSquare}${endingSquare}` });
      setBoard(response_player.data.board);
      setMyMoves((prevMoves) => [...prevMoves, response_player.data.move]);
      setNumberList((prevNums) => [...prevNums, moveNumber.toString() + '.']);
      setMoveNumber(moveNumber + 1);
      setStartingSquare('');
      setEndingSquare('');

      // computer move
      try {
        const response_bot = await axios.post('/make_computer_move');
        setBoard(response_bot.data.board);
        setBotMoves((prevMoves) => [...prevMoves, response_bot.data.move_san]);
        setInputValue('');
      } catch (error) {
        console.error('Error making move:', error);
      }

    } catch (error) {
      console.error('Error making move:', error);
      toast.error('Invalid move');
    }
  }

  const handleSubmit = async () => {
    // player move
    try {
      const response_player = await axios.post('/make_player_move', { move: inputValue });
      setBoard(response_player.data.board);
      setMyMoves((prevMoves) => [...prevMoves, response_player.data.move]);
      setNumberList((prevNums) => [...prevNums, moveNumber.toString() + '.']);
      setMoveNumber(moveNumber + 1);
      setInputValue('');

      // computer move
      try {
        const response_bot = await axios.post('/make_computer_move');
        setBoard(response_bot.data.board);
        setBotMoves((prevMoves) => [...prevMoves, response_bot.data.move_san]);
        setInputValue('');
      } catch (error) {
        console.error('Error making move:', error);
      }

    } catch (error) {
      console.error('Error making move:', error);
      toast.error('Invalid move');
    }
  }

  const scrollToBottom = () => {
    movesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="app">
      <div className="text">
        <h1>ChipotleBot</h1>
        <h3>pay up,, sucker</h3>
      </div>
      <ToastContainer autoClose={1000} hideProgressBar={true} />
      {gameStarted ?
        <div className="game">
          <div className="board">
            <ChessBoard
              fen={board}
              setStartingSquare={setStartingSquare}
              endingSquare={endingSquare}
              setEndingSquare={setEndingSquare}
              submitDraggingMove={submitDraggingMove}
            />
            {/* move input would go here */}
          </div>
          <div className="moves-stats">
            <div className="moves-headers">
              <p className="header" style={{paddingLeft: '40px'}}>#</p>
              <p className="header">My Moves</p>
              <p className="header">ChipotleBot's Moves</p>
            </div>
            <div className="moves-grid">
              <div className="numbers column">
                {numberList.map((item, index) => (
                <p key={index} className={index % 2 === 0 ? 'even' : 'odd'}>
                  {item}
                </p>
              ))}
              </div>
              <div className="column">
                {myMoves.map((item, index) => (
                  <p key={index} className={index % 2 === 0 ? 'even' : 'odd'}>
                    {item}
                  </p>
                ))}
                <div ref={movesEndRef} />
              </div>
              <div className="column">
                {botMoves.map((item, index) => (
                  <p key={index} className={index % 2 === 0 ? 'even' : 'odd'}>
                    {item}
                  </p>
                ))}
              </div>
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

{/* move input:
<input
  value={inputValue}
  onChange={handleInputChange}
  onKeyUp={handleKeyPress}
  placeholder="Type your move and press Enter"
/>
*/}