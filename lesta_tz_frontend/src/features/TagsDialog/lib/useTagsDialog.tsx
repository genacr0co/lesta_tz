import { useEffect, useState } from 'react';
import { createTrigger } from "trigger-man";
import { useQuery } from "react-query";

import { TRIGGER } from "@/shared/const";

import { getTagList } from "../api/services";

interface ITag {
    name: string;
    isSelected: Boolean;
}

export const useTagsDialog = () => {

    const getTagsFromLocalStorage = (key: string): string[] | undefined => {
        try {
            const jsonArray = localStorage.getItem(key);
            if (jsonArray) {
                return JSON.parse(jsonArray);
            } else {
                return undefined;
            }
        } catch (error) {
            console.error(error);
            return undefined;
        }
    };

    const [loading, setLoading] = useState<boolean>(true);
    const [tags, setTags] = useState<ITag[]>([]);

    const request = () => {
        setLoading(true)

        getTagList().then(r => {
            if (r.status === 200) {
                console.log(r.data)

                const tagsFromLocalStorage = getTagsFromLocalStorage('tags');
                console.log(tagsFromLocalStorage)

                if (tagsFromLocalStorage !== undefined) {
                    const tagsArray: ITag[] = r.data.tags.map(tag => ({
                        name: tag,
                        isSelected: tagsFromLocalStorage.includes(tag)
                    }));
                    createTrigger(TRIGGER.CHANGE_TAG, { tags: tagsFromLocalStorage });
                    setTags(tagsArray);
                } else {
                    const tagsArray: ITag[] = r.data.tags.map(tag => ({
                        name: tag,
                        isSelected: true
                    }));

                    createTrigger(TRIGGER.CHANGE_TAG, { tags: r.data.tags });
                    setTags(tagsArray);
                }
            }

        }).catch(e => {
            console.log(e)

        }).finally(() => {
            setLoading(false)
        })
    }

    useQuery('getTagList', () => {
        request();
    });

    function handleClick(name: string) {
        const newTags = tags.map(tag =>
            tag.name === name
                ? { ...tag, isSelected: !tag.isSelected }
                : tag
        )

        setTags(newTags);

        const selectedTagNames: string[] = newTags.filter(tag => tag.isSelected).map(tag => tag.name);

        createTrigger(TRIGGER.CHANGE_TAG, { tags: selectedTagNames });

        try {
            const jsonArray = JSON.stringify(selectedTagNames);
            localStorage.setItem('tags', jsonArray);
        } catch (error) {
            console.error(error);
        }
    }

    return {
        getTagsFromLocalStorage,
        loading, setLoading,
        tags, setTags,
        request,
        handleClick
    }
}