import { useEffect, useState, } from "react";
import { useTrigger, createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import { Props } from "../lib/props";
import styles from '../styles/FileText.module.css';
import { getDocumentContent } from "../api/services";
import { IGetDocumentContentParams } from "../api/types";
import { TRIGGER } from "@/shared/const";
import { UploadButton } from "@/features";
import Image from 'next/image'
import image_no_data from '../assets/image.svg'

export const FileText = (props: Props) => {


    const [loading, setLoading] = useState<boolean>(true);

    const [filename, setFileName] = useState<string>();
    const [content, setContent] = useState<string>();

    const [document_id, setDocumentId] = useState<number>();


     const { refetch } = useQuery('getDocumentContent', () => {
           request();
    });
   

    const request = () => {
        setLoading(true)

        if(document_id) {
            getDocumentContent({
                document_id, 
            }).then(r => {
                if (r.status === 200) {
                    console.log(r.data)
                    setFileName(r.data.filename);
                    setContent(r.data.content);
                }
            }).catch(e => {
                console.log(e)

                setFileName('');
                setContent('');

            }).finally(() => {
                setLoading(false)
            })
        }
        
    }

    useEffect(() => {
        refetch()
    }, [document_id])

    useTrigger(TRIGGER.SELECT_DOCUMENT, (event) => {
        setDocumentId(event.detail.document_id)
    });

    useTrigger(TRIGGER.DELETE_DOCUMENT, (event) => {
        refetch()
    });

    useTrigger(TRIGGER.FILE_UPLOADED, (event) => {
        setDocumentId(event.detail.document_id)
    });

    return (
        <>

            <div style={{
                position: "relative", 
                width: "50%",
                backgroundColor: 'white',
                borderRight: '2px solid #f4f4f4',
            }}>
                <UploadButton/>
                

            
                
                <div className={styles.content}>
                <div style={{textAlign: 'center', margin: '20px', fontWeight: 'bold'}}>{filename}</div>
                {!content ?
                        <Image
                        src={image_no_data}
                        width={400}
                        height={400}
                        draggable={"false"}
                        alt="image_no_data"
                        style={{position: 'absolute', left: '50%',  top: '50%', transform: 'translate(-50%, -50%)'}}
                    /> : content}
                    
                    </div>
            </div>
        </>
    );
};