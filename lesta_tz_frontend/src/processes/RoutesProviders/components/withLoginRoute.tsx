import {useRouter} from 'next/router';
import {useCookies} from "react-cookie";
import {isTokenExpired} from "@/shared/lib/helpers";
import { useEffect, useState } from "react";

// eslint-disable-next-line react/display-name
export const withLoginRoute = <P extends object>(
    Component: React.ComponentType<P>,
    href?: string
): React.FC<P> => {
    return (props) => {
        const router = useRouter();
        const [cookies] = useCookies();
        const [loading, setLoading] = useState(true);

        useEffect(() => {
            const checkAuth = () => {
                const access = cookies.access;
                const refresh = cookies.refresh;

                if (access !== undefined && !isTokenExpired(refresh)) {
                    router.replace(href || '/'); // faster redirect, no history entry
                } else {
                    setLoading(false); // разрешаем рендер компонента
                }
            };

            checkAuth();
        }, [cookies, router]);

        if (loading) {
            return null; // или можно вернуть спиннер
        }

        return <Component {...props} />;
    };
};
