import { Props } from "../lib/props";
import styles from '../styles/TableTF.module.css';


export const TableTF = (props: Props) => {

    const list = ['Привет', 'Пока', 'Пока', 'Пока', 'Пока', 'Пока',
        'Привет', 'Пока', 'Пока', 'Пока'
    ]

    return (
        <>
            <div className={styles.TableHead}>
                <div className={styles.BoderRight} style={{width: "60%"}}>Слово</div>
                <div className={styles.BoderRight} style={{width: "20%", textAlign: "center"}}>TF</div>
                <div style={{width: "20%", textAlign: "center"}}>IDF</div>
            </div>

            {
                list.map((item, index) => 
                    <div key = {index} className={styles.TableRow}>
                        <div className={styles.BoderRight} style={{width: "60%"}}>{item}</div>
                        <div className={styles.BoderRight} style={{width: "20%", textAlign: "center"}}>0.5</div>
                        <div style={{width: "20%", textAlign: "center"}}>1</div>
                    </div>
                )
            }
           
            <div className={styles.TableBottom}>
              <div>Rows per page: 5 </div> 
              <div>
                <div> 1–5 of 9</div>
              </div>
            </div>
        </>
    );
};