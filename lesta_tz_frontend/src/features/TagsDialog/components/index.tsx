import { Props } from '../lib/props';
import { useTagsDialog } from '../lib/useTagsDialog';

import { DialogButton, Button } from '@/shared/ui';

export const TagsDialog = (props: Props) => {

    const { tags, handleClick } = useTagsDialog();

    return <>
        <DialogButton title={'Tags'}>
            {tags.map((tag, i) =>
                <Button onClick={() => handleClick(tag.name)} selected={!tag.isSelected} key={i}>
                    {tag.name}
                </Button>
            )}
            
        </DialogButton>
    </>
}