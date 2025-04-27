import React from "react";

import {DocsList, TableTF} from '@/widgets'

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
                    <div style={{
                        width: "80%",
                        backgroundColor: 'white',
                        borderRight: '2px solid #f4f4f4',
                        padding: '30px 24px'
                    }}>
                       <div style={{textAlign: 'center', marginBottom: '60px', fontWeight: 'bold'}}>Название файла</div>
                       <div >
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads
                        Lmsdfmkladmfkla dksamfkladmfkl;as f asklnaf;klan fal nfads

                       </div>
                    </div>
                    <TableTF/>
                </div>
            </main>
        </>
    )
};

export default Home;