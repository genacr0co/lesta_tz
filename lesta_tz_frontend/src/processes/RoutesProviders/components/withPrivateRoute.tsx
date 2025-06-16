import {useRouter} from 'next/router';
import React, {useEffect} from 'react';
import {Cookies as ReactCookies, useCookies} from "react-cookie";
import {createTrigger} from "trigger-man";
import {isTokenExpired} from "@/shared/lib/helpers";
import {postRefreshTokens} from "@/shared/api/services";

// eslint-disable-next-line react/display-name
export const withPrivateRoute = <P extends object>(Component: React.ComponentType<P>, href?: string): React.FC<P> => {
    return (props) => {
        const router = useRouter();
        const [cookies, setCookie] = useCookies();
        useEffect(() => {
            if(cookies.refresh === undefined || isTokenExpired(cookies.refresh)) {
                router.push(href || '/')
            }else {
                if (cookies.access === undefined || isTokenExpired(cookies.access)) {
                    postRefreshTokens().then((r) => {
                        if (r.status === 200) {
                            setCookie('access', r.data.access_token)
                            setCookie('refresh', r.data.refresh_token)
                        }
                    }).catch(e => {
                        createTrigger('alert', {message: 'Refresh Token Expired', type: 'error'})

                        const react_cookies = new ReactCookies();
                        react_cookies.remove('access')
                        react_cookies.remove('refresh')
                        router.push(href || '/').then(() => {
                        })
                    })
                }
            }
        }, []);

        return <Component {...props} />;
    };
};
