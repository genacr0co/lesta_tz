import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";


import {DocButton} from '@/shared/ui'
import { TRIGGER } from "@/shared/const";



import { Props } from "../lib/props";
import styles from '../styles/DocsList.module.css';
import { getDocsList, deleteDocument} from "../api/services";
import { IDocItem } from "../api/types";
import { FcOpenedFolder } from "react-icons/fc";

export const DocsList = (props: Props) => {

    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<IDocItem[]>([]);

    const { refetch } = useQuery('getDocsList', () => {
        request();
    });

    const request = () => {
        setLoading(true)

        getDocsList().then(r => {
            if (r.status === 200) {
                console.log(r.data)
                setList(r.data.results);
            }
        }).catch(e => {
            console.log(e)

        }).finally(() => {
            setLoading(false)
        })
    }

    useEffect(() => {
        refetch()
    }, [])

 
    const onSelect = (document_id: number) => {
        createTrigger(TRIGGER.SELECT_DOCUMENT, { document_id: document_id });
    }
       
    const delete_request = (document_id: number) => {

        deleteDocument({document_id}).then(r => {
            if (r.status === 200) {
                console.log(r.data)
                createTrigger(TRIGGER.DELETE_DOCUMENT);
            }
        }).catch(e => {
            console.log(e)

        }).finally(() => {

        })
    }

    useTrigger(TRIGGER.DELETE_DOCUMENT, (event) => {
        refetch()
    });

    useTrigger(TRIGGER.FILE_UPLOADED, (event) => {
        refetch();
    });


    return (
        <>
            <div className={styles.Root}>
                <div className={styles.title}><FcOpenedFolder size={32} /> <div>Список документов</div></div>
                <div className={styles.line}/>

                 <div className={styles.ListRow}>
                    {loading ? <div>Loading</div> : <>
                    
                    {
                        list.map((item) => <DocButton
                        onDeleteClick={() => delete_request(item.id) }
                        onClickTitle={() => onSelect(item.id)} key={item.id} title={item.filename}/>)
                    }
                    
                    </>}
                </div> 

                
            </div>
        </>
    );
};