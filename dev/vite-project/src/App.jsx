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

  // for table rows
  const [numberList, setNumberList] =  useState([]);
  const [myMoves, setMyMoves] = useState([]);
  const [botMoves, setBotMoves] = useState([]);

  const [moveNumber, setMoveNumber] = useState(1); // for going backwards/forwards

  // for highlighting squares
  const [highlighted, setHighlighted] = useState([[]]);
  const [halfMoveNumber, setHalfMoveNumber] = useState(0);

  // list of currently selected squares (right clicking)
  const [selected, setSelected] = useState([]);

  // for dragging and dropping
  const [startingSquare, setStartingSquare] = useState('');
  const [endingSquare, setEndingSquare] = useState('');

  const movesEndRef = useRef(null);

  useEffect(() => {
    console.log('half-move number:', halfMoveNumber);
  }, [halfMoveNumber]);

  useEffect(() => {
    console.log('half-move number:', highlighted);
  }, [highlighted]);

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
    if (startingSquare && (startingSquare != endingSquare)) {
      submitDraggingMove();
    }
  }, [endingSquare])

  const startGame = async () => {
    try {
      const response = await axios.post('/start_game');
      setBoard(response.data.board);
      setNumberList([]);
      setMyMoves([]);
      setBotMoves([]);
      setMoveNumber(1);
      setHighlighted([[]]);
      setHalfMoveNumber(0);
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

  const handleBackButton = async () => {
    try {
      const response = await axios.post('/prev_board');
      setBoard(response.data.board);
      setHalfMoveNumber(halfMoveNumber - 1);
    } catch (error) {
      console.error('Error visualizing previous board:', error);
    }
  }

  const handleForwardButton = async () => {
    try {
      const response = await axios.post('/next_board');
      setBoard(response.data.board);
      setHalfMoveNumber(halfMoveNumber + 1);
    } catch (error) {
      console.error('Error visualizing next board:', error);
    }
  }

  const handleUndo = async () => {
    try {
      const response = await axios.post('/undo');
      setBoard(response.data.board);
      setMyMoves((prevMoves) => prevMoves.slice(0, -1)); // remove last player moves
      setBotMoves((prevMoves) => prevMoves.slice(0, -1)); // remove last bot moves
      setNumberList((prevNums) => prevNums.slice(0, -1)); // remove last numbers
      setHalfMoveNumber(halfMoveNumber - 2);
      setHighlighted((prevHighlighted) => prevHighlighted.slice(0, -2)); // remove last highlighted squares
      setMoveNumber(moveNumber - 1);
    } catch (error) {
      console.error('Error undoing move:', error);
    }
  }

  const submitDraggingMove = async () => {
    // player move
    try {
      const response_player = await axios.post('/make_player_move_dragging', { move: `${startingSquare}${endingSquare}` });
      setBoard(response_player.data.board);
      setMyMoves((prevMoves) => [...prevMoves, response_player.data.move]);
      setNumberList((prevNums) => [...prevNums, moveNumber.toString() + '.']);
      setMoveNumber(moveNumber + 1); // ok because only called once in this function
      setHalfMoveNumber((prevHalfMoveNumber) => prevHalfMoveNumber + 1);
      setHighlighted((prevHighlighted) => [...prevHighlighted, response_player.data.highlighted]);
      setStartingSquare('');
      setEndingSquare('');
      setSelected([]);

      // computer move
      try {
        const response_bot = await axios.post('/make_computer_move');
        setBoard(response_bot.data.board);
        setBotMoves((prevMoves) => [...prevMoves, response_bot.data.move_san]);
        setHighlighted((prevHighlighted) => [...prevHighlighted, response_bot.data.highlighted]);
        setHalfMoveNumber((prevHalfMoveNumber) => prevHalfMoveNumber + 1);
        setInputValue('');
      } catch (error) {
        console.error('Error making move:', error);
      }

    } catch (error) {
      console.error('Error making move:', error);
      setStartingSquare('');
      setEndingSquare('');
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
    <div className="app" onClick={() => setSelected([])}>
      <div className="top">
        <img src="chipotlebot_logo.png" />
        <div className="text">
          <h1>ChipotleBot</h1>
          <h3>pay up,, sucker</h3>
        </div>
      </div>
      <ToastContainer autoClose={1000} hideProgressBar={true} />
      {gameStarted ?
        <div className="game">
          <div className="board">
            <div className="board-buttons">
              <button className="undo" onClick={handleUndo} title="undo"/>
              <div className="boardstate-buttons">
                <button className="back button" onClick={handleBackButton} title="back"/>
                <button className="forward button" onClick={handleForwardButton} title="forward"/>
              </div>
            </div>
            <ChessBoard
              fen={board}
              startingSquare={startingSquare}
              setStartingSquare={setStartingSquare}
              setEndingSquare={setEndingSquare}
              highlighted={highlighted}
              halfMoveNumber={halfMoveNumber}
              selected={selected}
              setSelected={setSelected}
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