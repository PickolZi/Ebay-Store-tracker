
import "./card.styles.css"

const Card = ({title, content}) => {

    return (
        <div className="card">
            <h4 className="card__title">{title}</h4>
            <h1 className="card__content">{content}</h1>
        </div>
    )
}

export default Card;