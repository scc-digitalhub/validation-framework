import * as React from 'react';

import { matchPath } from "react-router";
import { useLocation } from "react-router-dom";

import { useRedirect } from 'react-admin';

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
    if (bytes < 0)
        return 'Error';
    
    if (bytes === 0)
        return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export const formatDuration = (duration, msDecimals = 3) => {
    const dm = msDecimals < 0 ? 0 : msDecimals;
    
    if (duration < 1000)
        return duration.toFixed(dm) + ' ms';
        
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
    let dm = decimals < 0 ? 0 : decimals;
    if (value === 1 || value === 0)
        dm = 0;
    
    return (value * 100).toFixed(dm) + '%';
}