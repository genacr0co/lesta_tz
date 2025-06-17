import {Props} from "../lib/props";
import {useEffect, useRef} from "react";

export const InfiniteScroll = (props: Props) => {
 const _lastElement = useRef<HTMLDivElement>(null);
    const observer = useRef<IntersectionObserver | null>(null);

    useEffect(() => {
        if (props.loading) return;

        if (observer.current) {
            observer.current.disconnect();
        }

        const options: IntersectionObserverInit | undefined = props.root
            ? { root: document.querySelector(props.root) }
            : undefined;

        observer.current = new IntersectionObserver((entries) => {
            const [entry] = entries;
            if (
                entry.isIntersecting &&
                !props.loading &&
                props.listLength < props.count // более точная проверка
            ) {
            props.setPage(props.page + 1);
            }
        }, options);

        const target = props.lastElementCurrent ?? _lastElement.current;
        if (target) {
            observer.current.observe(target);
        }

        return () => {
            observer.current?.disconnect();
        };
    }, [props.loading, props.lastElementCurrent, props.page, props.pageSize, props.count, props.root, props.setPage]);

    return (
        <>
            {props.children}
            {props.lastElementCurrent === undefined && (
                <div
                    ref={_lastElement}
                    style={props.debug ? { backgroundColor: 'red', height: 20, width: '100%' } : {}}
                />
            )}
        </>
    );
};