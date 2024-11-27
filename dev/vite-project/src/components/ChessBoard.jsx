import './ChessBoard.css'
import Square from './Square'
import pieces from '../pieces.js'

function ChessBoard() {
    const renderSquares = () => {
        const squares = [];
        for (let row = 7; row >= 0; row--) {
            for (let col = 7; col >= 0; col--) {
                const color = (row + col) % 2 === 0 ? 'white' : 'black';
                let piece = null;
                let pieceColor = null;
                if (row == 1 || row == 6) {
                    piece = pieces[0]; // pawn
                } else if (row == 0 || row == 7) {
                    if (col == 0 || col == 7) {
                        piece = pieces[3]; // rook
                    } else if (col == 1 || col == 6) {
                        piece = pieces[1]; // knight
                    } else if (col == 2 || col == 5) {
                        piece = pieces[2]; // bishop
                    }
                }

                if (row < 2) { // white pieces
                    pieceColor = 'white';
                    if (row == 0) {
                        if (col == 3) {
                            piece = pieces[5]; // king
                        } else if (col == 4) {
                            piece = pieces[4]; // queen
                        }
                    }
                    
                } else if (row > 5) { // black pieces
                    pieceColor = 'black';
                    if (row == 7) {
                        if (col == 3) {
                            piece = pieces[5]; // king
                        } else if (col == 4) {
                            piece = pieces[4]; // queen
                        }
                    }
                }

                squares.push(<Square key={`${row}-${col}`} color={color} piece={piece} pieceColor = {pieceColor}/>);
            }
        }
        return squares;
    };

    return (
        <div className="square-grid">
            {renderSquares()}
        </div>
    )
}

export default ChessBoard