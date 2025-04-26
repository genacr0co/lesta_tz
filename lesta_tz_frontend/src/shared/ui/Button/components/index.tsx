import {Props} from "../lib/props";
import styles from '../styles/button.module.css';

export const Button = (props: Props) => {
    return <div 
                className={`${styles.root} ${props.selected && styles.selected} ${props.fixed && styles.fixed} ${props.disabled && styles.disabled}`}
                onClick={props.onClick}
    >
      {props.children}
    </div>
}