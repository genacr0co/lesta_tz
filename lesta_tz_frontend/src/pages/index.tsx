import React from "react";

import {DocsList, TableTF} from '@/widgets'

const Home = () => {
    return (
        <>
            <main>
                <div style={{margin: '0 auto', width: '100%', padding: '0 10px'}}>
                    {/* <DocsList/> */}
                    <TableTF/>
                </div>
            </main>
        </>
    )
};

export default Home;