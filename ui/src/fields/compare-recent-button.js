import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

export const CompareRecentButton = () => {
    const redirect = useRedirect();
    
    const handleClick = () => {
        redirect('/run-comparison/recent');
    };
    
    return (
        <Button
            onClick={handleClick}
            label="Compare recent runs"
        >
            <CompareArrowsIcon />
        </Button>
    );
};