import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import { PATH_RUN_COMPARISON_RECENT } from '../utils/common-constants';

import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

export const CompareRecentButton = () => {
    const redirect = useRedirect();
    
    const handleClick = () => {
        redirect(PATH_RUN_COMPARISON_RECENT);
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