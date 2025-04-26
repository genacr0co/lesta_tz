import {Card} from '@/entities';
import {Button} from '@/shared/ui';

import {Props} from "../lib/props";
import styles from '../styles/BookCard.module.css';

export const BookCard = (props:Props) => {

    const date = new Date(props.date);

    const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'long'
    };
    
    const formattedDate = date.toLocaleDateString('en-US', options);

    return <Card onClick={props.onClick}>
            <div className={styles.root}>
                <h1 className={styles.title}>
                    {props.title}
                </h1>

                <h2 className={styles.author}>
                by {props.author}
                </h2>

                <h3 className={styles.date}>
                    {formattedDate}
                </h3>

                <h3 className={styles.price}>
                    {props.price}$
                </h3>
            </div>
            
            <div className={styles.line}/>

            <div className={styles.tags}>
                {props.tags !== undefined && props.tags.map((e, i) => <Button disabled key={i}>{e}</Button>)}
            </div>
        </Card>
}

