import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";
import { useRouter } from 'next/router'


import { AuthFooter } from "@/features";

import {DocButton} from '@/shared/ui'
import { TRIGGER } from "@/shared/const";


import { Props } from "../lib/props";
import styles from '../styles/LoginForm.module.css';
import { getDocsList, deleteDocument} from "../api/services";
import { IDocItem } from "../api/types";
import { FcOpenedFolder } from "react-icons/fc";

export const LoginForm = (props: Props) => {
  const router = useRouter()
    // const [loading, setLoading] = useState<boolean>(true);
    // const [list, setList] = useState<IDocItem[]>([]);

    // const { refetch } = useQuery('getDocsList', () => {
    //     request();
    // });

    // const request = () => {
    //     setLoading(true)

    //     getDocsList().then(r => {
    //         if (r.status === 200) {
    //             console.log(r.data)
    //             setList(r.data.results);
    //         }
    //     }).catch(e => {
    //         console.log(e)

    //     }).finally(() => {
    //         setLoading(false)
    //     })
    // }

    // useEffect(() => {
    //     refetch()
    // }, [])

 
    // const onSelect = (document_id: number) => {
    //     createTrigger(TRIGGER.SELECT_DOCUMENT, { document_id: document_id });
    // }
       
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


    return (
        <>
        <div  className={styles.FormTitle}>Login to Account</div>
        <form className={styles.Card} onSubmit={(e) => {
            e.preventDefault();
        }}>
            <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Email</div>
                <input
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    className={styles.FormInputBody}
                    required
                />
            </div>

            <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Password</div>
                <input
                    type="password"
                    name="password"
                    placeholder="Enter your password"
                    className={styles.FormInputBody}
                    required
                />
            </div>

            <button type="submit" className={styles.FormButton}>Sign in</button>
            </form>
            <div className={styles.Card}>
               <div className={styles.flex}>
                <div>
                 Don't have an account? 
               </div>
                
                <div className={styles.link}  onClick={() => router.push('/register')}>
                    Register now
                </div>
               </div>
            </div>
            <AuthFooter/>
        </>
    );
};