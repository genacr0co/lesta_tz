import { useEffect, useState,useRef } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";
import { Skeleton} from 'antd';
import { FcOpenedFolder } from "react-icons/fc";
import Image from 'next/image'

import {DocButton, InfiniteScroll} from '@/shared/ui'
import { TRIGGER } from "@/shared/const";

import { Props } from "../lib/props";
import styles from '../styles/ColDocList.module.css';
import { getColDocsList} from "../api/services";
import { IColDoc} from "../api/types";

import img from '../assets/image.png';

export const ColDocList = (props: Props) => {
    const requestIdRef = useRef(0);
    const isResettingRef = useRef(false);

    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<IColDoc[]>([]);

    const [page, setPage] = useState<number>(1);
    const [page_size, setPageSize] = useState<number>(10);
    const [count, setCount] = useState<number>(0);

    const [collection_id, setCollectionId] = useState<number>();
    const [collection_name, setCollectionName] = useState<string>('');

    const { refetch } = useQuery('getDocsList', () => {
        if(collection_id !== undefined) {
            request(page, page_size, collection_id);
        }
    });

    const request = (page: number, page_size: number, collection_id: number) => {
        const currentRequestId = ++requestIdRef.current;

        if(collection_id !== undefined){
            setLoading(true)

            getColDocsList({page, page_size, collection_id}).then(r => {
                if (requestIdRef.current === currentRequestId)  {
                    if (r.status === 200) {
                        setCount(r.data.total);
                        // setList([...list, ...r.data.documents]);
                        setList(prev => {
                        const existingIds = new Set(prev.map(item => item.id));
                        const newItems = r.data.documents.filter(item => !existingIds.has(item.id));
                        return [...prev, ...newItems];
                        });
                    }
                }
             
            }).catch(e => {
                console.log(e)

            }).finally(() => {
              if (requestIdRef.current === currentRequestId) {
                  setLoading(false);
              }
            })
        }
    }

     const reset_request = (collection_id: number, collection_name: string) => {
        if(collection_id !== undefined){

             const currentRequestId = ++requestIdRef.current;
              isResettingRef.current = true; 

            setLoading(true)

            setCollectionId(collection_id)
            setCollectionName(collection_name)
            setList([])
            setPage(1)


            getColDocsList({page: 1, page_size, collection_id}).then(r => {
              if (requestIdRef.current === currentRequestId) {
                if (r.status === 200) {
                    setCount(r.data.total);
                    setList(r.data.documents);
                }
            }
            }).catch(e => {
                console.log(e)

            }).finally(() => {
             if (requestIdRef.current === currentRequestId) {
                  setLoading(false);
                   isResettingRef.current = false;
              }
            })
        }
    }

    useEffect(() => {
        if (!isResettingRef.current) {
            refetch();
        }
    }, [page, collection_id]);

    
    
    useTrigger(TRIGGER.SELECT_COLLECTION, (event) => {
       reset_request(event.detail.collection_id, event.detail.collection_name);
    });

 
    const onSelect = (document_id: number,collection_id: number) => {
        createTrigger(TRIGGER.SELECT_DOCUMENT, { document_id: document_id , collection_id: collection_id});
    }
       
    // const delete_request = (document_id: number) => {

    //     deleteDocument({document_id}).then(r => {
    //         if (r.status === 200) {
    //             console.log(r.data)
    //             createTrigger(TRIGGER.DELETE_DOCUMENT);
    //         }
    //     }).catch(e => {
    //         console.log(e)

    //     }).finally(() => {

    //     })
    // }

    // useTrigger(TRIGGER.DELETE_DOCUMENT, (event) => {
    //     refetch()
    // });



    // useTrigger(TRIGGER.FILE_UPLOADED, (event) => {
    //     refetch();
    // });

    const loaders = () => <>
        <Skeleton.Node active={true} className={styles.skeleton} />
        <Skeleton.Node active={true} className={styles.skeleton} />
        <Skeleton.Node active={true} className={styles.skeleton} />
        <Skeleton.Node active={true} className={styles.skeleton} />
    </>


    return (
        <>
            <div className={styles.Root}>
                {collection_id !== undefined ? 
                    <>

                        <div className={styles.title}>
                            {   
                            // @ts-ignore
                            <FcOpenedFolder size={32} />
                            }
                            <div>{collection_name}</div>
                        </div>
                        
                        <div className={styles.line}/>


                        <div className={styles.ListRow}>
                            <InfiniteScroll listLength={list.length} page={page} setPage={setPage} loading={loading} count={count} pageSize={page_size} debug={false}>
                                <div className={styles.items}>
                                    {
                                    list.map((item) => <DocButton
                                    filename={item.filename}
                                    download_url={`${process.env.NEXT_PUBLIC_DOMAIN}/static/${item.filename}`}
                                    // onDeleteClick={() => delete_request(item.id) }
                                    onClickTitle={() => onSelect(item.id, collection_id)} 
                                    key={item.id} title={item.filename}/>)
                                    }
                                    {loading && loaders()} 
                                </div>
                            </InfiniteScroll>
                        </div> 
                    </>
                
                : <>
                    <div className={styles.empty}>
                                <div>
                                        Выберите коллекцию для просмотра документов
                                </div>
                    </div>
                
                </> }
            </div>
        </>
    );
};