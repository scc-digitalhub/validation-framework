import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import ArrowBack from '@material-ui/icons/ArrowBack';

import { PATH_PROJECT, PATH_EXPERIMENT, PATH_RUN, PATH_OVERVIEW, RESOURCE_PROJECT, RESOURCE_EXPERIMENT,
 RESOURCE_RUN, RESOURCE_RUN_COMPARISON, RESOURCE_RUN_COMPARISON_RECENT }  from '../utils/common-constants'; 
import { GetCurrentRun } from '../utils/common-functions';

import { AppContext } from '../contexts/app-context';

const defaultIcon = <ArrowBack />;

export const BackButton = ({
    label = "Back",
    icon = defaultIcon,
    resource,
    clear=false
}) => {
    const currentRun = GetCurrentRun();
    
    const setProject = React.useContext(AppContext).setProject;
    const setExperiment = React.useContext(AppContext).setExperiment;
    
    const redirect = useRedirect();
    
    const handleClick = () => {
        switch(resource) {
            case RESOURCE_PROJECT:
                setProject(null);
                setExperiment(null);
                redirect(PATH_PROJECT);
                break;
            case RESOURCE_EXPERIMENT:
                if (clear) {
                    setExperiment(null);
                    redirect(PATH_EXPERIMENT);
                } else {
                    redirect(PATH_PROJECT + PATH_OVERVIEW);
                }
                break;
            case RESOURCE_RUN:
                if (clear) {
                    redirect(PATH_RUN);
                } else {
                    redirect(PATH_EXPERIMENT + PATH_OVERVIEW);
                }
                break;
            case RESOURCE_RUN_COMPARISON: case RESOURCE_RUN_COMPARISON_RECENT:
                redirect(PATH_RUN);
                break;
            default:
                redirect(PATH_RUN + '/' + currentRun + PATH_OVERVIEW);
        }
    };
    
    return (
        <Button
            onClick={handleClick}
            label={label}
        >
            {icon}
        </Button>
    );
    
};