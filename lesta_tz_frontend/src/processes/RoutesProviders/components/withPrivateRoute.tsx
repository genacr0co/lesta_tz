import {useRouter} from 'next/router';
import {Cookies as ReactCookies, useCookies} from "react-cookie";
import {createTrigger} from "trigger-man";
import {isTokenExpired} from "@/shared/lib/helpers";
import {postRefreshTokens} from "@/shared/api/services";
import { useEffect, useState } from "react";

// eslint-disable-next-line react/display-name
export const withPrivateRoute = <P extends object>(
    Component: React.ComponentType<P>,
    href?: string
): React.FC<P> => {
    return (props) => {
        const router = useRouter();
        const [cookies, setCookie] = useCookies();
        const [authorized, setAuthorized] = useState(false);
        const [checking, setChecking] = useState(true); // состояние загрузки

        useEffect(() => {
            const checkTokens = async () => {
                const refresh = cookies.refresh;
                const access = cookies.access;

                if (!refresh || isTokenExpired(refresh)) {
                    router.replace(href || '/');
                    return;
                }

                if (!access || isTokenExpired(access)) {
                    try {
                        const r = await postRefreshTokens();
                        if (r.status === 200) {
                            setCookie('access', r.data.access_token);
                            setCookie('refresh', r.data.refresh_token);
                            setAuthorized(true);
                        }
                    } catch (e) {
                        createTrigger('alert', { message: 'Refresh Token Expired', type: 'error' });
                        const reactCookies = new ReactCookies();
                        reactCookies.remove('access');
                        reactCookies.remove('refresh');
                        router.replace(href || '/');
                        return;
                    }
                } else {
                    setAuthorized(true);
                }

                setChecking(false);
            };

            checkTokens();
        }, [cookies, router, setCookie]);

        // пока проверяется — ничего не рендерим
        if (checking) return null;

        // если проверено и авторизован — отрисовываем компонент
        return authorized ? <Component {...props} /> : null;
    };
};