import * as React from 'react';

import { useRedirect } from 'react-admin';

import { Button, Loading } from 'react-admin';
import ArrowForward from '@material-ui/icons/ArrowForward';

import { AppContext } from '../contexts/app-context';

const defaultIcon = <ArrowForward />;

export const SelectButton = ({
    label = "View",
    record,
    icon = defaultIcon,
    resource,
    ...rest
}) => {
    const setProject = React.useContext(AppContext).setProject;
    const setExperiment = React.useContext(AppContext).setExperiment;
    
    const redirect = useRedirect();
    
    const handleClick = () => {
        switch(resource) {
            case 'project':
                setProject(record.id);
                setExperiment(null);
                redirect('/project/overview');
                break;
            case 'experiment':
                setExperiment(record.experimentId);
                redirect('/experiment/overview');
                break;
            case 'run':
                redirect('/run/' + record.runId + '/overview');
                break;
            default:
        }
    };
    
    if (!record)
        return <Loading />;
    
    return (
        <Button
            onClick={handleClick}
            label={label}
            alignIcon='right'
            {...rest}
        >
            {icon}
        </Button>
    );
    
};