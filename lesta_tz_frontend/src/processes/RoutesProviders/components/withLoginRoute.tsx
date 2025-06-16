import {useRouter} from 'next/router';
import React, {useEffect} from 'react';
import {useCookies} from "react-cookie";
import {isTokenExpired} from "@/shared/lib/helpers";

export const withLoginRoute = <P extends object>(Component: React.ComponentType<P>, href?: string): React.FC<P> => {
    return (props) => {
        const router = useRouter();
        const [cookies] = useCookies();

        useEffect(() => {
            if (cookies.access !== undefined) {
                console.log(cookies.refresh)
                if (!isTokenExpired(cookies.refresh)) {
                    router.push(href || '/')
                }
            }
        }, []);

        return <Component {...props} />;
    };
};
