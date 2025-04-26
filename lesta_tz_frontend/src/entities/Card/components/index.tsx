import {Props} from "../lib/props";
import styles from '../styles/card.module.css';

export const Card = (props:Props) => {
    return <div className={`${styles.root}`} onClick={props.onClick}>
            {props.children}
        </div>
}

