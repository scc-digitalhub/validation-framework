import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import { PATH_RUN_COMPARISON } from '../utils/common-constants';

import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

export const CompareButton = ({
    selectedIds
}) => {
    let disabled = true;
    if (selectedIds.length >= 2)
        disabled = false;
    
    const redirect = useRedirect();
    
    const handleClick = () => {
        redirect(PATH_RUN_COMPARISON + '/' + selectedIds);
    };
    
    return (
        <Button
            onClick={handleClick}
            label="Compare"
            disabled={disabled}
        >
            <CompareArrowsIcon />
        </Button>
    );
    
};