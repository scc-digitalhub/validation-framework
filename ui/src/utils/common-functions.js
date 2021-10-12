import * as React from 'react';

import { matchPath } from "react-router";
import { useLocation } from "react-router-dom";

import { TopToolbar } from 'react-admin';
import { useRedirect } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { BackButton } from '../fields/back-button';
import { AppContext } from '../contexts/app-context';

export const CheckProjectAndExperiment = () => {
    const redirect = useRedirect();
    const currentProject = React.useContext(AppContext).getProject();
    const currentExperiment = React.useContext(AppContext).getExperiment();
    
    let valid = true;
    
    if (!currentProject) {
        valid = false;
        redirect('/project');
    } else if (!currentExperiment) {
        valid = false;
        redirect('/experiment');
    }
    
    return valid;
}

export const GetCurrentRun = () => {
    let run = null;
    
    const runMatch = (matchPath(useLocation().pathname, {
        path: ['/run/:run', '/run/:run/:other'],
        exact: true,
        strict: false
    }));
    
    if (runMatch && runMatch.params && runMatch.params.run)
        run = runMatch.params.run;
    
    return run;
}

export const formatBytes = (bytes, decimals = 2) => {
    if (typeof(bytes) == 'string')
        return bytes;
    
    if (bytes == null || bytes < 0)
        return null;

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export const calculateDuration = (start, finish) => {
    if (!start)
        return null;
    
    const startDate = new Date(start);
    
    let finishDate = finish ? new Date(finish) : Date.now();
    
    return formatDuration(finishDate - startDate);
}

export const formatDuration = (duration, msDecimals = 2) => {
    if (!duration || duration < 0)
        return null;
    
    const dm = msDecimals < 0 ? 2 : msDecimals;
    
    if (duration < 10)
        return duration.toFixed(dm) + ' ms';
    
    if (duration < 1000)
        return parseInt(duration) + ' ms';
        
    const ms = parseInt((duration % 1000) / 100);
    let s = Math.floor((duration / 1000) % 60);
    let m = Math.floor((duration / (1000 * 60)) % 60);
    let h = Math.floor((duration / (1000 * 60 * 60)) % 24);
    
    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;
    
    return h + ':' + m + ':' + s + '.' + ms;
}

export const displayAsPercentage = (value, decimals = 2) => {
    if (value == null)
        return null;
    
    let dm = decimals < 0 ? 0 : decimals;
    if (value === 1 || value === 0)
        dm = 0;
    
    return (value * 100).toFixed(dm) + '%';
}

export const makeFieldObject = (index, label, value) => {
    return {
        'index': index,
        'label': label,
        'value': value
    }
}

export const normalizeSeverity = (severity) => {
    if (isNaN(severity))
        return 5;
    else if (severity < 1)
        return 1;
    else if (severity > 5)
        return 5;
    
    return severity;
}

export const missingDocumentError = (resource) => {
    return genericError(resource, 'No ' + resource + ' document found.');
}

export const genericError = (resource, errorMessage) => {
    return (
        <React.Fragment>
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <Typography class='MuiFormLabel-root' >
                        {errorMessage}
                    </Typography>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}