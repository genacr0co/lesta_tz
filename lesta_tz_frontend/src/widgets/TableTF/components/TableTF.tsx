import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import { Props } from "../lib/props";
import styles from '../styles/TableTF.module.css';
import { getWordList } from "../api/services";
import { IGetWordList, IGetWordListItem, IGetWordListParams } from "../api/types";
import { TRIGGER } from "@/shared/const";
import { MdKeyboardArrowLeft } from "react-icons/md";
import { MdOutlineKeyboardArrowRight } from "react-icons/md";

export const TableTF = (props: Props) => {


    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<IGetWordListItem[]>([]);
    
    const [page, setPage] = useState<number>(1);
    const [page_size, setPageSize] = useState<number>(50);

    const [total, setTotal] = useState<number>();
    const [total_pages, setTotalPages] = useState<number>();

    const [document_id, setDocumentId] = useState<number>();


     const { refetch } = useQuery('getWordList', () => {
           request();
    });
   
     

    const request = () => {
        setLoading(true)

        if(document_id) {
            getWordList({
                document_id, 
                page,
                page_size
            }).then(r => {
                if (r.status === 200) {
                    console.log(r.data)
                    setList(r.data.results);
                    setTotalPages(r.data.total_pages)
                    setTotal(r.data.total)
                }
            }).catch(e => {
                console.log(e)

            }).finally(() => {
                setLoading(false)
            })
        }
        
    }

    useEffect(() => {
        refetch()
    }, [document_id, page_size, page])

    useTrigger(TRIGGER.SELECT_DOCUMENT, (event) => {
        setDocumentId(event.detail.document_id)
        setPage(1)
        setTotalPages(undefined)
    });

    useTrigger(TRIGGER.DELETE_DOCUMENT, (event) => {
        refetch()
        setPage(1)
        setTotalPages(undefined)
    });

    useTrigger(TRIGGER.FILE_UPLOADED, (event) => {
        setDocumentId(event.detail.document_id)
        setPage(1)
        setTotalPages(undefined)
    });


    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newSize = parseInt(event.target.value, 10);
        setPageSize(newSize);
      };

    return (
        <>
        
            <div className={styles.table}>
                <div className={styles.table_body}>
                    <div className={styles.TableHead}>
                        <div className={`${styles.Column} ${styles.BorderRight}`} style={{width: "60%"}}>Слово</div>
                        <div className={`${styles.Column} ${styles.BorderRight}`} style={{width: "20%", textAlign: "center"}}>TF</div>
                        <div className={`${styles.Column}`}  style={{width: "20%", textAlign: "center"}}>IDF</div>
                    </div>
                    <div className={styles.rows}>
                        {
                            list.map((item, i) => 
                                <div key = {item.word}
                                style={{backgroundColor: `${i % 2 === 0 ? "white": "none"}`}}
                                className={styles.TableRow}>
                                    <div  className={`${styles.rowColumn} ${styles.BorderRight}`} style={{width: "60%"}}>{item.word}</div>
                                    <div  className={`${styles.rowColumn} ${styles.BorderRight}`}style={{width: "20%", textAlign: "center"}}>{item.tf}</div>
                                    <div  className={`${styles.rowColumn}`} style={{width: "20%", textAlign: "center"}}>{item.idf}</div>
                                </div>
                            )
                        }
                    </div>
                   
                </div>
                <div className={styles.table_bottom}>
                    <div className={styles.pageSize}>
                        <div>
                            Кол-во строк:
                        </div>

                        <select id="page-size" value={page_size} onChange={handleChange}>
                        <option value="5">5</option>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                        </select>
                    </div>
                    <div className={styles.pageSize}>
                        <div className={styles.arrowBtn} onClick={() => {
                            if(page>1){
                                setPage(page - 1)
                            }else{
                                setPage(1)
                            }
                        }}>{ 
                           // @ts-ignore
                            <MdKeyboardArrowLeft />
                        }</div>
                        <div>{total_pages && page}</div>
                        <div>...</div>
                        <div>{total_pages}</div>
                        <div className={styles.arrowBtn} onClick={() => {
                            if(total_pages) {
                                if(page<total_pages){
                                    setPage(page + 1)
                                }else{
                                    setPage(total_pages)
                                }
                            }
                        }}>{
                           // @ts-ignore
                            <MdOutlineKeyboardArrowRight />
                        }</div>
                    </div>
                </div>
            </div>


            {/*

          
           
            <div className={styles.TableBottom}>
              <div>Rows per page: 5 </div> 
              <div>
                <div> 1–5 of 9</div>
              </div>
            </div> */}
        </>
    );
};