import {Props} from "../lib/props";
import styles from '../styles/docButton.module.css';
import Image from 'next/image'
import docs_icon from '../assets/docs.png'

export const DocButton = (props: Props) => {
    return <div 
                className={`${styles.root} ${props.selected && styles.selected} ${props.fixed && styles.fixed} ${props.disabled && styles.disabled}`}
                onClick={props.onClick}
    >
        <Image
          src={docs_icon}
          width={64}
          height={64}
          draggable={"false"}
          alt="doc_icon"
        />
    </div>
}