import React from "react";

import {DocsList, TableTF, FileText} from '@/widgets'

const Home = () => {
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