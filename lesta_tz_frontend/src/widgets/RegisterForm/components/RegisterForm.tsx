import { useState} from "react";
import {createTrigger } from "trigger-man";
import { useRouter } from 'next/router'
import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { AuthFooter } from "@/features";

import { TRIGGER } from "@/shared/const";

import { Props } from "../lib/props";
import styles from '../styles/RegisterForm.module.css';
import { postRegister} from "../api/services";

export const RegisterForm = (props: Props) => {
    const router = useRouter()
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<boolean>(false);
    const [name, setName] = useState<string>();
    const [email, setEmail] = useState<string>();
    const [password, setPassword] = useState<string>();
    const [password2, setPassword2] = useState<string>();

    const request = () => {

         if (email !== undefined && 
            name !== undefined &&
            password !== undefined &&
            password == password2
        ) {
            setLoading(true)
            setError(false)

            postRegister({
                email,
                name,
                password
            }).then(r => {
                if (r.status === 200) {
                    console.log(r.data)
                    createTrigger(TRIGGER.ALERT, {message: 'You have successfully registered', type: 'success'})
                    router.push('/login').then(() => {})
                }
            }).catch(e => {
                console.log(e)
                setError(true)
                createTrigger(TRIGGER.ALERT, {message: `${e.response.data.detail}`})
            }).finally(() => {
                setLoading(false)
            })
        }
        else {
            setError(true)
        }
    }
  
    return (
        <>
        <div  className={styles.FormTitle}>Create an Account</div>
        <form className={`${error && styles.error} ${styles.Card}`} onSubmit={(e) => {
            e.preventDefault();
            request()
        }}>
            <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Email</div>
                <input
                    type="email"
                    name={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className={styles.FormInputBody}
                    required
                />
            </div>

              <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Name</div>
                <input
                    type="name"
                    name={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your name"
                    className={styles.FormInputBody}
                    required
                />
            </div>

            <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Password</div>
                <input
                    type="password"
                    name={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className={styles.FormInputBody}
                    required
                />
            </div>

               <div className={styles.FormInput}>
                <div className={styles.FormInputTitle}>Repeat password</div>
                <input
                    type="password"
                    name={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    placeholder="Enter your password"
                    className={styles.FormInputBody}
                    required
                />
            </div>

            <button type="submit" disabled={loading} className={styles.FormButton}>
                {loading ? 
                   <Spin indicator={<LoadingOutlined spin />} />
                :
                <div>
                    Sign up
                </div>
                }
         
                
                </button>
            </form>
            <div className={styles.Card}>
               <div className={styles.flex}>
                <div>
                Already have an account? 
               </div>
                
                <div className={styles.link}  onClick={() => router.push('/login')}>
                    Login  now
                </div>
               </div>
            </div>
            <AuthFooter/>
        </>
    );
};