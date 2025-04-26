import React, { useState } from 'react';
import { Props } from "../lib/props";
import IconPolygon from './icon_polygon';
import styles from '../styles/DialogButton.module.css';

export const DialogButton = (props: Props) => {

  const [isClicked, setIsClicked] = useState<Boolean>(false);

  const onClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (props.onClick) {
      props.onClick(event);
    }

    setIsClicked(!isClicked)

  }

  return <div className={`${styles.root}`}>

    <div className={`${styles.container}`} onClick={onClick}>
      {props.title}

      <span className={`${styles.icon} ${isClicked ? styles.iconUp : styles.iconDown}`}>
        <IconPolygon />
      </span>

    </div>


    {
      isClicked ? <>

        <div className={`${styles.dialog}`}>
          {props.children}
        </div>

        <div className={`${styles.bgDialog}`} onClick={() => { setIsClicked(false) }} />

      </> : <></>
    }

  </div>
}