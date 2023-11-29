
import "./spreadsheet.styles.css";

const Spreadsheet = () => {
    return (
        <div className="spreadsheet">
            <div className="spreadsheet__titles">
                <h4>Picture</h4>
                <h4>Title</h4>
                <h4>Make</h4>
                <h4>Model</h4>
                <h4>Price</h4>
                <h4>Listed date</h4>
                <h4>Date sold</h4>
                <h4>Days till sold</h4>
            </div>
            <div className="spreadsheet__rows">
                row!
            </div>
        </div>
    )
}

export default Spreadsheet;