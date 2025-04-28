import {Props} from "../lib/props";
import styles from '../styles/docButton.module.css';
import Image from 'next/image'
import docs_icon from '../assets/docs.png'
import eye_icon from '../assets/eye.svg'

import { IoMdOpen } from "react-icons/io";
import { MdDelete } from "react-icons/md";

export const DocButton = (props: Props) => {
    return <div 
                className={`${styles.root} ${props.selected && styles.selected} ${props.fixed && styles.fixed} ${props.disabled && styles.disabled}`}
              
    >
      <div className={styles.icon}>
      <Image
          src={docs_icon}
          width={32}
          height={32}
          draggable={"false"}
          alt="doc_icon"
        />
      </div>
 

        <div className={styles.title}  onClick={props.onClickTitle}>
          {props.title}
        </div>

        <MdDelete size={32} className={styles.delete} onClick={props.onDeleteClick}/>

        <IoMdOpen size={32} className={styles.view} />

    </div>
}