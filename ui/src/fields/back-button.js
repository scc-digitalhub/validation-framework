import * as React from 'react';

import { useRedirect, Button } from 'react-admin';

import ArrowBack from '@material-ui/icons/ArrowBack';

import { GetCurrentRun } from '../utils/common-functions';

import { AppContext } from '../contexts/app-context';

const defaultIcon = <ArrowBack />;

export const BackButton = ({
    label = "Back",
    icon = defaultIcon,
    resource,
    clear=false,
    ...rest
}) => {
    const currentRun = GetCurrentRun();
    
    const setProject = React.useContext(AppContext).setProject;
    const setExperiment = React.useContext(AppContext).setExperiment;
    
    const redirect = useRedirect();
    
    const handleClick = () => {
        switch(resource) {
            case 'project':
                setProject(null);
                setExperiment(null);
                redirect('/project');
                break;
            case 'experiment':
                if (clear) {
                    setExperiment(null);
                    redirect('/experiment');
                } else {
                    redirect('/project/overview');
                }
                break;
            case 'run':
                if (clear) {
                    redirect('/run');
                } else {
                    redirect('/experiment/overview');
                }
                break;
            default:
                redirect('/run/' + currentRun + '/overview');
        }
    };
    
    return (
        <Button
            onClick={handleClick}
            label={label}
            {...rest}
        >
            {icon}
        </Button>
    );
    
};