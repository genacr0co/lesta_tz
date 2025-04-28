import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import { Props } from "../lib/props";
import styles from '../styles/UploadButton.module.css';
import { postUploadFile } from "../api/services";
import { TRIGGER } from "@/shared/const";

import { useRef } from 'react';
import { FaGithub } from "react-icons/fa";

export const UploadButton = (props: Props) => {
    const inputRef = useRef<HTMLInputElement>(null);

    const [loading, setLoading] = useState<boolean>(true);

    const [file, setFile] = useState<File | null>(null);
   

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {

      const selectedFile = e.target.files?.[0];

      if (selectedFile) {
            setFile(selectedFile);
            setLoading(true)

            await postUploadFile({ file: selectedFile }).then(r => {
                if (r.status === 200) {
                    console.log(r.data)
                    createTrigger(TRIGGER.FILE_UPLOADED, { document_id: r.data.document_id });
                }
            }).catch(e => {
                console.log(e)

            }).finally(() => {
                setLoading(false)
            })
        }
    }

    const handleClick = () => {
        inputRef.current?.click(); // Программно нажимаем на input
      };
        

    return (
        <>
        <div className={styles.root}>
            <input
                type="file"
                accept=".txt"
                ref={inputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

            <div
                onClick={handleClick}
                className={styles.button}
            >
                Загрузить .txt файл
            </div>

            <a href="https://github.com/genacr0co/lesta_tz/tree/main" target="_blank">
                 <FaGithub style={{cursor: 'pointer'}} size={32} />
            </a>
        </div>
        </>
    );
  
};