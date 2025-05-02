import React from "react";

import {DocsList, TableTF, FileText} from '@/widgets'

const Home = () => {
    console.log('process.env.NEXT_PUBLIC_DOMAIN: ', process.env.NEXT_PUBLIC_DOMAIN)
    
    return (
        <>
            <main>
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    margin: '0 auto', width: '100%'
                    }}>
                    <DocsList/>
                    <FileText/>
                    <TableTF/>
                </div>
            </main>
        </>
    )
};

export default Home;