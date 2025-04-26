import React from "react";
import type {AppProps} from 'next/app';
import {QueryClient, QueryClientProvider} from "react-query";

import '@/shared/styles/globals.css';
import '@/shared/assets/fonts/inter/stylesheet.css';

import Head from "next/head";

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            refetchOnReconnect: false,
            refetchOnMount: false,
            retry: false,
            staleTime: Infinity,
            cacheTime: Infinity,
        },
    },
});


export default function App({Component, pageProps}: AppProps) {

    return <div>
        <Head>
            <title>Book Store</title>
            <meta name="description" content="Welcome to Book Store."/>
            <meta name="keywords" content="Book Store, store, book"/>

            <meta name="viewport" content="width=device-width, initial-scale=1"/>
        </Head>
        <QueryClientProvider client={queryClient}>
            <Component {...pageProps} />
        </QueryClientProvider>
    </div>
}