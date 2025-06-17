import { useState} from "react";
import {createTrigger } from "trigger-man";
import { useRouter } from 'next/router'
import { Spin, Checkbox, Modal  } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { AuthFooter } from "@/features";
import { TRIGGER } from "@/shared/const";

import { Props } from "../lib/props";
import styles from '../styles/RegisterForm.module.css';
import { postRegister} from "../api/services";

export const RegisterForm = (props: Props) => {
    const router = useRouter()
    const [loading, setLoading] = useState<boolean>(false);
    const [isChecked, setIsChecked] = useState<boolean>(false);
    const [error, setError] = useState<boolean>(false);
    const [name, setName] = useState<string>();
    const [email, setEmail] = useState<string>();
    const [password, setPassword] = useState<string>();
    const [password2, setPassword2] = useState<string>();

      const [isModalOpen, setIsModalOpen] = useState(false);

        const showModal = () => {
            setIsModalOpen(true);
        };

        const handleCancel = () => {
            setIsModalOpen(false);
        };

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

            <div  className={styles.FormCheckbox}>
                <Checkbox 
                onChange={() => {
                    setIsChecked(!isChecked)
                }}
                >
                   I agree to the <span className={styles.link} onClick={showModal}>Terms</span> and <span className={styles.link} onClick={showModal}>Privacy Policy</span>
                </Checkbox>
              
            </div>

            <button type="submit" disabled={loading || !isChecked} className={`${!isChecked && styles.disableButton} ${styles.FormButton}`}>
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

            <Modal
            title="Terms and Privacy Policy"
            closable={{ 'aria-label': 'Custom Close Button' }}
            open={isModalOpen}
            onCancel={handleCancel}
            footer={null}
            >
                <p>Создавая аккаунт, вы соглашаетесь с тем, что:</p>
                <br/>
                <p>
                    <ul>
                    <li>Ваша душа теперь принадлежит нам (обратно не возвращается).</li>
                    <li>Мы имеем право присылать вам мемы в 3 часа ночи.</li>
                    <li>Вы обязуетесь участвовать в танцевальных баттлах по первому зову.</li>
                    <li>Ваш первенец будет назван в честь нашего сервиса.</li>
                    <li>Печеньки (cookies) — не съедобные. Смиритесь.</li>
                    <li>Ну и, в целом, вы становитесь нашим верным подданным навеки вечные.</li>
                    </ul>
                </p>
                   <br/>
                <p><em>*Это не является юридическим документом. Всё выше сказанное — лишь шутка 😄*</em></p>
            </Modal>
        </>
    );
};