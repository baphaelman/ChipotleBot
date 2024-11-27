import './ChessBoard.css'
import Square from './Square'
import pieces from '../pieces.js'

function ChessBoard({ fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' }) {
    const renderNewBoard = () => {
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

    const renderBoardFromFen = (fen) => {
        const squares = [];
        const rows = fen.split(' ')[0].split('/');
        for (let row = 0; row < 8; row++) {
            let col = 0;
            for (let char of rows[row]) {
                if (isNaN(char)) {
                    const color = (row + col) % 2 === 0 ? 'white' : 'black';
                    let piece = null;
                    let pieceColor = null;
                    switch (char) {
                        case 'p':
                            piece = pieces[0];
                            pieceColor = 'black';
                            break;
                        case 'r':
                            piece = pieces[3];
                            pieceColor = 'black';
                            break;
                        case 'n':
                            piece = pieces[1];
                            pieceColor = 'black';
                            break;
                        case 'b':
                            piece = pieces[2];
                            pieceColor = 'black';
                            break;
                        case 'q':
                            piece = pieces[4];
                            pieceColor = 'black';
                            break;
                        case 'k':
                            piece = pieces[5];
                            pieceColor = 'black';
                            break;
                        case 'P':
                            piece = pieces[0];
                            pieceColor = 'white';
                            break;
                        case 'R':
                            piece = pieces[3];
                            pieceColor = 'white';
                            break;
                        case 'N':
                            piece = pieces[1];
                            pieceColor = 'white';
                            break;
                        case 'B':
                            piece = pieces[2];
                            pieceColor = 'white';
                            break;
                        case 'Q':
                            piece = pieces[4];
                            pieceColor = 'white';
                            break;
                        case 'K':
                            piece = pieces[5];
                            pieceColor = 'white';
                            break;
                        default:
                            break;
                    }
                    squares.push(<Square key={`${row}-${col}`} color={color} piece={piece} pieceColor={pieceColor} />);
                    col++;
                } else {
                    const emptySquares = parseInt(char, 10);
                    for (let i = 0; i < emptySquares; i++) {
                        const color = (row + col) % 2 === 0 ? 'white' : 'black';
                        squares.push(<Square key={`${row}-${col}`} color={color} />);
                        col++;
                    }
                }
            }
        }
        return squares;
    }

    return (
        <div className="square-grid">
            {renderBoardFromFen(fen)}
        </div>
    )
}

export default ChessBoard