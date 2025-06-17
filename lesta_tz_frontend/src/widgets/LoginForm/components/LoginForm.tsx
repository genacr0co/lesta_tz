import { useState} from "react";
import {createTrigger } from "trigger-man";
import { useRouter } from 'next/router'
import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { AuthFooter } from "@/features";
import {useCookies} from "react-cookie";

import { TRIGGER } from "@/shared/const";

import { Props } from "../lib/props";
import styles from '../styles/LoginForm.module.css';
import { postlogin} from "../api/services";


export const LoginForm = (props: Props) => {
  const router = useRouter()
      const [loading, setLoading] = useState<boolean>(false);
      const [error, setError] = useState<boolean>(false);
      const [email, setEmail] = useState<string>();
      const [password, setPassword] = useState<string>();
      const [cookies, setCookie] = useCookies();

      const request = () => {
  
           if (email !== undefined && 
              password !== undefined 
            ) {
              setLoading(true)
              setError(false)
  
              postlogin({
                  email,
                  password,
              }).then(r => {
                  if (r.status === 200) {
                      console.log(r.data)
                        setCookie('access', r.data.access_token)
                        setCookie('refresh', r.data.refresh_token)
                      createTrigger(TRIGGER.ALERT, {message: 'You have successfully logged', type: 'success'})
                      router.push('/').then(() => {})
                  }
              }).catch(e => {
                  console.log(e)
                  setError(true)

                 if (Array.isArray(e.response.data.detail)) {
                    for (let i = 0; i <e.response.data.detail.length; i++) {
                        createTrigger(TRIGGER.ALERT, {message: `${e.response.data.detail[i].msg}`})
                    }
                 }else {
                  createTrigger(TRIGGER.ALERT, {message: `${e.response.data.detail}`})
                 }
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
        <div  className={styles.FormTitle}>Login to Account</div>
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

            <button type="submit" className={styles.FormButton}>
               {loading ? 
                   <Spin indicator={<LoadingOutlined spin />} />
                :
                <div>
                    Sign in
                </div>
                }
            </button>
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