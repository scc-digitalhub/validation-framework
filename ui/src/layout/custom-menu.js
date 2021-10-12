import * as React from 'react';

import { DashboardMenuItem, MenuItemLink } from 'react-admin';

import { useLocation } from "react-router-dom";

import { GetCurrentRun } from '../utils/common-functions';

import WorkIcon from '@material-ui/icons/Work';
import WorkOutline from '@material-ui/icons/WorkOutline';
import GroupWorkIcon from '@material-ui/icons/GroupWork';
import GroupWorkOutlinedIcon from '@material-ui/icons/GroupWorkOutlined';
import AccountTreeIcon from '@material-ui/icons/AccountTree';
import AccountTreeOutlinedIcon from '@material-ui/icons/AccountTreeOutlined';
import ListIcon from '@material-ui/icons/List';
import ShortTextIcon from '@material-ui/icons/ShortText';
import Divider from '@material-ui/core/Divider';
import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

import { AppContext } from '../contexts/app-context';

const LEFT_PADDING = '18px';

const CustomMenu = () => {
    const currentProject = React.useContext(AppContext).getProject();
    const currentExperiment = React.useContext(AppContext).getExperiment();
    const currentRun = GetCurrentRun();
    
    const setProject = React.useContext(AppContext).setProject;
    const setExperiment = React.useContext(AppContext).setExperiment;
    
    const clearProject = () => {
        setProject(null);
    }
    
    const clearExperiment = () => {
        setExperiment(null);
    }
    
    return (generateMainMenu(currentProject, currentExperiment, currentRun, clearProject, clearExperiment));
}

const generateMainMenu = (currentProject, currentExperiment, currentRun, clearProject, clearExperiment) => {
    let menuContent = [];
    
    menuContent.push(<DashboardMenuItem onClick={clearProject} key='dashboard' />)
    menuContent.push(<Divider key='project-list-divider' />);
    
    menuContent.push(makeMenuItem('projects', '/project', 'Projects', <WorkOutline />, clearProject));
    
    if (currentProject) {
        menuContent.push(generateProjectSubMenu(currentProject, currentExperiment, currentRun, clearExperiment));
    }
    
    return (
        <React.Fragment>
            { menuContent }
        </React.Fragment>
    );
}

const generateProjectSubMenu = (currentProject, currentExperiment, currentRun, clearExperiment) => {
    let projectSubMenuContents = [];
    
    projectSubMenuContents.push(makeMenuItem('project-overview', '/project/overview', currentProject, <WorkIcon />, clearExperiment));
    projectSubMenuContents.push(makeMenuItem('experiments', '/experiment', 'Experiments', <GroupWorkOutlinedIcon />, clearExperiment));
    
    if (currentExperiment) {
        projectSubMenuContents.push(generateExperimentSubMenu(currentExperiment, currentRun));
    }
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='project-sub-menu' >
            { projectSubMenuContents }
        </div>
    );
}

const generateExperimentSubMenu = (currentExperiment, currentRun) => {
    let experimentSubMenuContents = [];
    
    experimentSubMenuContents.push(makeMenuItem('experiment-overview', '/experiment/overview', currentExperiment, <GroupWorkIcon />));
    experimentSubMenuContents.push(makeMenuItem('runs', '/run', 'Runs', <AccountTreeOutlinedIcon />));
    
    if (currentRun) {
        experimentSubMenuContents.push(generateRunSubMenu(currentRun));
    } else if (InRunComparison()) {
        experimentSubMenuContents.push(<Divider key='run-comparison-divider' />);
        experimentSubMenuContents.push(makeMenuItem('run-comparison', '', 'Run comparison', <CompareArrowsIcon />, null, true));
    }
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='experiment-sub-menu' >
            { experimentSubMenuContents }
        </div>
    );
}

const generateRunSubMenu = (currentRun) => {
    let runSubMenuContents = [];
    
    runSubMenuContents.push(makeMenuItem('run-overview', '/run/' + currentRun + '/overview', currentRun, <AccountTreeIcon />));
    runSubMenuContents.push(makeMenuItem('artifact-metadata', '/run/' + currentRun + '/artifact-metadata', 'Artifact metadata', <ListIcon />));
    runSubMenuContents.push(makeMenuItem('data-profile', '/run/' + currentRun + '/data-profile', 'Data profile', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItem('data-resource', '/run/' + currentRun + '/data-resource', 'Data resource', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItem('run-environment', '/run/' + currentRun + '/run-environment', 'Run environment', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItem('run-metadata', '/run/' + currentRun + '/run-metadata', 'Run metadata', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItem('short-report', '/run/' + currentRun + '/short-report', 'Short report', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItem('short-schema', '/run/' + currentRun + '/short-schema', 'Short schema', <ShortTextIcon />));
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='run-sub-menu' >
            { runSubMenuContents }
        </div>
    );
}

const makeMenuItem = (
        key,
        to = '',
        primaryText = '',
        leftIcon = null,
        onClick = null,
        disabled = false
    ) => {
    return (<MenuItemLink
            key={key}
            to={to}
            primaryText={primaryText}
            leftIcon={leftIcon}
            onClick={onClick}
            disabled={disabled}
        />);
}

const InRunComparison = () => {
    return useLocation().pathname.indexOf("run-comparison") > -1;
}

export default CustomMenu;