import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";
import { useRouter } from 'next/router';

import { BookCard, TagsDialog } from "@/features";
import { TRIGGER } from "@/shared/const";
import {DocButton} from '@/shared/ui'


import { Props } from "../lib/props";
import styles from '../styles/DocsList.module.css';
import { getBookList } from "../api/services";
import { IBookItem, IFilterBy } from "../api/types";


export const DocsList = (props: Props) => {
    // const router = useRouter();

    // const [loading, setLoading] = useState<boolean>(true);
    // const [list, setList] = useState<IBookItem[]>([]);

    // const [totalPrice, setTotalPrice] = useState<number>(0);

    // const [tags, setTags] = useState<string[]>([]);

    // const [filterBy, setFilterBy] = useState<IFilterBy | undefined>();

    // const [priceOrder, setPriceOrder] = useState<boolean>(true);
    // const [authorOrder, setAuthorOrder] = useState<boolean>(true);
    // const [dateOrder, setDateOrder] = useState<boolean>(true);


    // const { refetch } = useQuery('getFirstPageList', () => {
    //     request();
    // });

    // const request = () => {
    //     setLoading(true)

    //     getBookList({ tags, filterBy }).then(r => {
    //         if (r.status === 200) {
    //             console.log(r.data)
    //             setList(r.data);
    //             setTotalPrice(r.data.reduce((accumulator, item) => accumulator + item.price, 0))
    //         }
    //     }).catch(e => {
    //         console.log(e)

    //     }).finally(() => {
    //         setLoading(false)
    //     })
    // }

    // useEffect(() => {
    //     refetch()
    // }, [tags, filterBy])

    // useTrigger(TRIGGER.CHANGE_TAG, (event) => {
    //     setTags(event.detail.tags)
    // });

    // const handleResetRules = () => {
    //     localStorage.removeItem('tags');
    //     router.reload();
    //     // router.push('/')
    // }
    

    // const loaders = () => <>
    //     Loading...
    // </>

    return (
        <>
            <div className={styles.Root}>
                <div>
                    S
                </div>
                <div className={styles.Container}>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>
                    <DocButton/>

                </div>
                <div>
                    D
                </div>
            </div>
        </>
    );
};