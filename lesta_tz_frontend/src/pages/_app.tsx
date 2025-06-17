import React from "react";
import type {AppProps} from 'next/app';
import {QueryClient, QueryClientProvider} from "react-query";

import '@/shared/styles/globals.css';
import '@/shared/assets/fonts/inter/stylesheet.css';

import Head from "next/head";
import {AppProvider} from "@/processes";

export default function App({Component, pageProps}: AppProps) {

    return <div>
        <Head>
            <title>TF IDF</title>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
        </Head>
        <AppProvider>
            <Component {...pageProps} />
        </AppProvider>
    </div>
}