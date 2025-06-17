import React from "react";

import {ColDocList, TableTF, FileText, ColList} from '@/widgets'
import {withPrivateRoute} from "@/processes";

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
                        <ColList/>
                        <ColDocList/>
                         <FileText/>
                        <TableTF/>
                </div>
            </main>
        </>
    )
};


export default withPrivateRoute(Home, '/login')


