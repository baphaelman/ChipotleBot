import './Square.css'

const Square = ({ tile, color, piece, pieceColor, setStartingSquare, setEndingSquare, isDragging, setIsDragging, isHighlighted, selected, setSelected }) => {
    let sprite = null;
    if (piece != null && pieceColor != null) {
        sprite = pieceColor === 'white' ? piece.white_sprite : piece.black_sprite;
    }

    const handleSelection = () => {
        if (selected.includes(tile)) {
            setSelected(selected.filter((selectedTile) => selectedTile !== tile));
        } else {
            setSelected([...selected, tile]);
            console.log(selected);
        }
    }

    return (
        <div
            className={`square
                ${color}
                ${piece ? 'pieceful' : ''}
                ${isDragging ? 'dragging' : ''}
                ${isHighlighted ? 'highlighted' : ''}
                ${selected.includes(tile) ? 'selected' : ''}`
            }
            onMouseDown={() => {setStartingSquare(tile);
                if (piece) {
                    setIsDragging(true);
                    }
            }}
            onMouseUp={() => {
                setEndingSquare(tile);
                setIsDragging(false);
            }}
            onContextMenu={(e) => {
                e.preventDefault(); // Prevent the default context menu from appearing
                handleSelection(); // Call the selection handler
            }}
        >
            {piece != null ? <img src={sprite} alt="chess piece" /> : null}
        </div>
    )
}

export default Square