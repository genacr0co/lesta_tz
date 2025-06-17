import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import {InfiniteScroll} from "@/shared/ui";

import {DocButton} from '@/shared/ui'
import { TRIGGER } from "@/shared/const";
import { Skeleton} from 'antd';



import { Props } from "../lib/props";
import styles from '../styles/ColList.module.css';
import { getColList} from "../api/services";
import { ICol } from "../api/types";
import { FcOpenedFolder } from "react-icons/fc";
import { MdOutlineAddCircle } from "react-icons/md";

export const ColList = (props: Props) => {

    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<ICol[]>([]);

    const [page, setPage] = useState<number>(1);
    const [page_size, setPageSize] = useState<number>(10);
    const [count, setCount] = useState<number>(0);

    const { refetch } = useQuery('getDocsList', () => {
        request();
    });

    const request = () => {
        setLoading(true)

        getColList({page, page_size}).then(r => {
            if (r.status === 200) {
                console.log(r.data)
                setCount(r.data.total);
                setList([...list, ...r.data.results]);
            }
        }).catch(e => {
            console.log(e)

        }).finally(() => {
            setLoading(false)
        })
    }

    useEffect(() => {
        refetch()
    }, [page])

 
    const onSelect = (collection_id: number, collection_name: string) => {
        createTrigger(TRIGGER.SELECT_COLLECTION, { collection_id: collection_id,  collection_name: collection_name});
    }
       

    // useTrigger(TRIGGER.DELETE_DOCUMENT, (event) => {
    //     refetch()
    // });

    // useTrigger(TRIGGER.FILE_UPLOADED, (event) => {
    //     refetch();
    // });

      const loaders = () => <>
        <div className={styles.skeletonList}>
            <Skeleton.Node active={true} className={styles.skeleton} />
            <Skeleton.Node active={true} className={styles.skeleton} />
            <Skeleton.Node active={true} className={styles.skeleton} />
            <Skeleton.Node active={true} className={styles.skeleton} />
        </div>
    </>


    return (
        <>
            <div className={styles.Root}>
                <div className={styles.title}>
                 
                  <div>Список коллекций</div>
                    {/* {   
                     // @ts-ignore
                     <MdOutlineAddCircle size={32} />
                    } */}
                </div>
                <div className={styles.line}/>

                 <div className={styles.ListRow}>
                        <InfiniteScroll listLength={list.length} page={page} setPage={setPage} loading={loading} count={count} pageSize={page_size} debug={false}>
                            <div className={styles.items}>
                                {
                                    list.map((item) => <div 
                                    
                                    onClick={() => onSelect(item.id, item.name)}
                                    key={item.id} className={styles.flex}>
                                        {   
                                        // @ts-ignore
                                        <FcOpenedFolder size={32} />
                                        }
                                        <span>{item.name}</span>
                                    </div>)
                                }
                                {loading && loaders()} 
                            </div>
                        </InfiniteScroll>
                </div> 

                
            </div>
        </>
    );
};