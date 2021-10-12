import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

export const CompareButton = ({
    selectedIds
}) => {
    let disabled = true;
    if (selectedIds.length >= 2)
        disabled = false;
    
    const redirect = useRedirect();
    
    const handleClick = () => {
        redirect('/run-comparison/' + selectedIds);
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