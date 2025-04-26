import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";
import { useRouter } from 'next/router';

import { BookCard, TagsDialog } from "@/features";
import { TRIGGER } from "@/shared/const";


import { Props } from "../lib/props";
import styles from '../styles/BookList.module.css';
import { getBookList } from "../api/services";
import { IBookItem, IFilterBy } from "../api/types";


export const BookList = (props: Props) => {
    const router = useRouter();

    const [loading, setLoading] = useState<boolean>(true);
    const [list, setList] = useState<IBookItem[]>([]);

    const [totalPrice, setTotalPrice] = useState<number>(0);

    const [tags, setTags] = useState<string[]>([]);

    const [filterBy, setFilterBy] = useState<IFilterBy | undefined>();

    const [priceOrder, setPriceOrder] = useState<boolean>(true);
    const [authorOrder, setAuthorOrder] = useState<boolean>(true);
    const [dateOrder, setDateOrder] = useState<boolean>(true);


    const { refetch } = useQuery('getFirstPageList', () => {
        request();
    });

    const request = () => {
        setLoading(true)

        getBookList({ tags, filterBy }).then(r => {
            if (r.status === 200) {
                console.log(r.data)
                setList(r.data);
                setTotalPrice(r.data.reduce((accumulator, item) => accumulator + item.price, 0))
            }
        }).catch(e => {
            console.log(e)

        }).finally(() => {
            setLoading(false)
        })
    }

    useEffect(() => {
        refetch()
    }, [tags, filterBy])

    useTrigger(TRIGGER.CHANGE_TAG, (event) => {
        setTags(event.detail.tags)
    });

    const handleResetRules = () => {
        localStorage.removeItem('tags');
        router.reload();
        // router.push('/')
    }
    

    const loaders = () => <>
        Loading...
    </>

    return (
        <>
            <div className={styles.Root}>
                <h1 className={styles.logo}>Book Store</h1>
            </div>

            <div className={styles.Root}>
                <div className={styles.spaceBetween}>

                    <div className={styles.row} style={{ gap: 18 }}>
                        <div className={styles.filterButton} onClick={
                            () => {
                                setFilterBy({
                                    name: 'price',
                                    order: priceOrder
                                })
                                setPriceOrder(!priceOrder)

                                setAuthorOrder(true)
                                setDateOrder(true)
                            }
                        }>
                            price {priceOrder ? '↓' : '↑'}
                        </div>


                        <div className={styles.filterButton} onClick={
                            () => {
                                setFilterBy({
                                    name: 'author',
                                    order: authorOrder
                                })
                                setAuthorOrder(!authorOrder)

                                setPriceOrder(true)
                                setDateOrder(true)

                            }
                        }>
                            author {authorOrder ? '↓' : '↑'}
                        </div>

                        <div className={styles.filterButton} onClick={
                            () => {
                                setFilterBy({
                                    name: 'date',
                                    order: dateOrder
                                })
                                setDateOrder(!dateOrder)

                                setPriceOrder(true)
                                setAuthorOrder(true)
                            }
                        }>
                            date {dateOrder ? '↓' : '↑'}
                        </div>

                    </div>

                    <div className={styles.row} style={{ gap: 18 }}>
                        <TagsDialog />

                        <div className={`${styles.underline} ${styles.filterButton}`} onClick={handleResetRules}>reset rules</div>
                    </div>
                </div>

            </div>

            <div className={styles.Root}>
                {
                    // loading ? loaders() :
                    list.map((item, i) => {
                        if (
                            !item.id ||
                            !item.author ||
                            !item.date ||
                            !item.price ||
                            !item.title ||
                            !item.tags
                        ) {
                            return null;
                        }

                        return <BookCard
                            key={item.id}
                            {...item}
                            title={`${i + 1} ${item.title}`}
                        />;
                    })}

                <div className={styles.totalPrice}>
                    <span>TOTAL:</span> {totalPrice}$
                </div>
            </div>
        </>

    );
};