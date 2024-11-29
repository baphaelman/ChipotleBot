import './Square.css'

const Square = ({ tile, color, piece, pieceColor, setStartingSquare, setEndingSquare, isDragging, setIsDragging }) => {
    let sprite = null;
    if (piece != null && pieceColor != null) {
        sprite = pieceColor === 'white' ? piece.white_sprite : piece.black_sprite;
    }
    
    return (
        <div
            className={`square ${color} ${piece ? 'pieceful' : ''} ${isDragging ? 'dragging' : ''}`}
            onMouseDown={() => {setStartingSquare(tile);
                if (piece) {
                    setIsDragging(true);
                    }
            }}
            onMouseUp={() => {
                setEndingSquare(tile);
                setIsDragging(false);
            }}
        >
            {piece != null ? <img src={sprite} alt="chess piece" /> : null}
        </div>
    )
}

export default Square