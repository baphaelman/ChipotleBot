import { useState } from 'react'
import './ChessBoard.css'
import Square from './Square'
import pieces from '../pieces.js'

function ChessBoard({ fen, setStartingSquare, setEndingSquare, highlighted, halfMoveNumber }) {
    const [isDragging, setIsDragging] = useState(false);
    const alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

    const renderBoardFromFen = (fen) => {
        const squares = [];
        const rows = fen.split(' ')[0].split('/');
        for (let row = 0; row < 8; row++) {
            let col = 0;
            for (let char of rows[row]) {
                if (isNaN(char)) {
                    const color = (row + col) % 2 === 0 ? 'white' : 'black';
                    const tile = `${alphabet[col]}${8 - row}`;
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
                    squares.push(
                        <Square
                            key={tile}
                            tile={tile}
                            color={color}
                            piece={piece}
                            pieceColor={pieceColor}
                            setStartingSquare={setStartingSquare}
                            setEndingSquare={setEndingSquare}
                            isDragging={isDragging}
                            setIsDragging={setIsDragging}
                            isHighlighted={highlighted[halfMoveNumber].includes(tile)}
                        />
                    );
                    col++;
                } else {
                    const emptySquares = parseInt(char, 10);
                    for (let i = 0; i < emptySquares; i++) {
                        const color = (row + col) % 2 === 0 ? 'white' : 'black';
                        const tile = `${alphabet[col]}${8 - row}`
                        squares.push(<Square
                            key={tile}
                            tile={tile}
                            color={color}
                            setStartingSquare={setStartingSquare}
                            setEndingSquare={setEndingSquare}
                            isDragging={isDragging}
                            setIsDragging={setIsDragging}
                            isHighlighted={highlighted[halfMoveNumber].includes(tile)}
                            />);
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