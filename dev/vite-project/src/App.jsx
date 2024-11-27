import './App.css'
import ChessBoard from './components/ChessBoard'

function App() {

  return (
    <div className="app">
      <div className="text">
        <h1>ChipotleBot</h1>
        <h2>pay up,, sucker</h2>
      </div>
      <div className="board">
        <ChessBoard />
      </div>
      <input></input>
    </div>
  )
}

export default App
