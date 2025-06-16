import { useEffect, useState, } from "react";
import Link from "next/link";
import getConfig from "next/config";

import { Props } from "../lib/props";
import styles from '../styles/AuthFooter.module.css';

const {publicRuntimeConfig} = getConfig();

export const AuthFooter = (props: Props) => {

    return (
        <>
         <div className={styles.footer}>
                <Link className={styles.footer_link} href={'/terms'} target="_blank">Terms</Link>
                <Link className={styles.footer_link} href={'/Privacy'} target="_blank">Privacy</Link>
                <Link className={styles.footer_link} href={`${publicRuntimeConfig.NEXT_PUBLIC_DOMAIN}/docs`} target="_blank">Docs</Link>
                <Link className={styles.footer_link} href={'https://t.me/genacr0co'} target="_blank">Contact</Link>
                <Link className={styles.footer_link} href={'https://github.com/genacr0co/lesta_tz'} target="_blank">GitHub Repository</Link>
            </div>
        </>
    );
  
};