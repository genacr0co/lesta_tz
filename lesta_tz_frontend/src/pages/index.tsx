import React from "react";

import {BookList} from '@/widgets'

const Home = () => {
    return (
        <>
            <main>
                <div style={{margin: '0 auto', width: '100%', padding: '0 10px'}}>
                    <BookList/>
                </div>
            </main>
        </>
    )
};

export default Home;