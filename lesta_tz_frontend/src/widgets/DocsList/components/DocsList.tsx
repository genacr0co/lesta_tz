import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import {DocButton} from '@/shared/ui'
import { TRIGGER } from "@/shared/const";


import { Props } from "../lib/props";
import styles from '../styles/DocsList.module.css';
import { getDocsList } from "../api/services";
import { IDocItem } from "../api/types";
import { FcOpenedFolder } from "react-icons/fc";

export const DocsList = (props: Props) => {

    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<IDocItem[]>([]);

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

    useEffect(()=>{
        request();
    }, [])

    const onSelect = (document_id: number) => {
        createTrigger(TRIGGER.SELECT_DOCUMENT, { document_id: document_id });
    }

    return (
        <>
            <div className={styles.Root}>
                <div className={styles.title}><FcOpenedFolder size={32} /> <div>Список документов</div></div>
                <div className={styles.line}/>

                 <div className={styles.ListRow}>
                    {loading ? <div>Loading</div> : <>
                    
                    {
                        list.map((item) => <DocButton onClickTitle={() => onSelect(item.id)} key={item.id} title={item.filename}/>)
                    }
                    
                    </>}
                </div> 
                
            </div>
        </>
    );
};