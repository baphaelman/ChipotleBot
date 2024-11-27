import './Square.css'

const Square = ({ color, piece, pieceColor }) => {
    let sprite = null;
    if (piece != null && pieceColor != null) {
        sprite = pieceColor === 'white' ? piece.white_sprite : piece.black_sprite;
    }
    
    return (
        <div className={`square ${color}`}>
            {piece != null ? <img src={sprite} alt="chess piece" /> : null}
        </div>
    )
}

export default Square