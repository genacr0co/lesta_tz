import {QueryClient, QueryClientProvider} from "react-query";
import {CookiesProvider} from 'react-cookie';

import {Props} from "../lib/props";

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


export const AppProvider = (props: Props) => {
    return (
        <>
                <CookiesProvider>
                    <QueryClientProvider client={queryClient}>
                        {props.children}
                    </QueryClientProvider>
             </CookiesProvider>
        </>
    );
};
