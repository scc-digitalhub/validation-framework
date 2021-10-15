import * as React from 'react';

import { useRedirect } from 'react-admin';

import { Button, Loading } from 'react-admin';
import ArrowForward from '@material-ui/icons/ArrowForward';

import { AppContext } from '../contexts/app-context';

import { PATH_PROJECT, PATH_EXPERIMENT, PATH_RUN, PATH_OVERVIEW, RESOURCE_PROJECT,
 RESOURCE_EXPERIMENT, RESOURCE_RUN} from '../utils/common-constants';

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
            case RESOURCE_PROJECT:
                setProject(record.id);
                setExperiment(null);
                redirect(PATH_PROJECT + PATH_OVERVIEW);
                break;
            case RESOURCE_EXPERIMENT:
                setExperiment(record.experimentId);
                redirect(PATH_EXPERIMENT + PATH_OVERVIEW);
                break;
            case RESOURCE_RUN:
                redirect(PATH_RUN + '/' + record.runId + PATH_OVERVIEW);
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