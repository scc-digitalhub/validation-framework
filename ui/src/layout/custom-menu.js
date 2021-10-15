import * as React from 'react';

import { DashboardMenuItem } from 'react-admin';

import { useLocation } from "react-router-dom";
import { PATH_PROJECT, PATH_EXPERIMENT, PATH_RUN, PATH_RUN_COMPARISON, PATH_OVERVIEW,
 PATH_ARTIFACT_METADATA, PATH_DATA_PROFILE, PATH_DATA_RESOURCE, PATH_RUN_ENVIRONMENT,
 PATH_RUN_METADATA, PATH_SHORT_REPORT, PATH_SHORT_SCHEMA} from '../utils/common-constants';
import { GetCurrentRun, makeMenuItemLink } from '../utils/common-functions';

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
    
    menuContent.push(makeMenuItemLink('projects', PATH_PROJECT, 'Projects', <WorkOutline />, clearProject));
    
    const inRunComparison = InRunComparison();
    
    if (currentProject) {
        menuContent.push(generateProjectSubMenu(currentProject, currentExperiment, inRunComparison, currentRun, clearExperiment));
    }
    
    return (
        <React.Fragment>
            { menuContent }
        </React.Fragment>
    );
}

const generateProjectSubMenu = (currentProject, currentExperiment, inRunComparison, currentRun, clearExperiment) => {
    let projectSubMenuContents = [];
    
    projectSubMenuContents.push(makeMenuItemLink('project-overview', PATH_PROJECT + PATH_OVERVIEW, currentProject, <WorkIcon />, clearExperiment));
    projectSubMenuContents.push(makeMenuItemLink('experiments', PATH_EXPERIMENT, 'Experiments', <GroupWorkOutlinedIcon />, clearExperiment));
    
    if (currentExperiment) {
        projectSubMenuContents.push(generateExperimentSubMenu(currentExperiment, inRunComparison, currentRun));
    }
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='project-sub-menu' >
            { projectSubMenuContents }
        </div>
    );
}

const generateExperimentSubMenu = (currentExperiment, inRunComparison, currentRun) => {
    let experimentSubMenuContents = [];
    
    experimentSubMenuContents.push(makeMenuItemLink('experiment-overview', PATH_EXPERIMENT + PATH_OVERVIEW, currentExperiment, <GroupWorkIcon />));
    experimentSubMenuContents.push(makeMenuItemLink('runs', PATH_RUN, 'Runs', <AccountTreeOutlinedIcon />));
    
    if (currentRun) {
        experimentSubMenuContents.push(generateRunSubMenu(currentRun));
    } else if (inRunComparison) {
        experimentSubMenuContents.push(<Divider key='run-comparison-divider' />);
        experimentSubMenuContents.push(makeMenuItemLink('run-comparison', '', 'Run comparison', <CompareArrowsIcon />, null, true));
    }
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='experiment-sub-menu' >
            { experimentSubMenuContents }
        </div>
    );
}

const generateRunSubMenu = (currentRun) => {
    let runSubMenuContents = [];
    
    runSubMenuContents.push(makeMenuItemLink('run-overview', PATH_RUN + '/' + currentRun + PATH_OVERVIEW, currentRun, <AccountTreeIcon />));
    runSubMenuContents.push(makeMenuItemLink('artifact-metadata', PATH_RUN + '/' + currentRun + PATH_ARTIFACT_METADATA, 'Artifact metadata', <ListIcon />));
    runSubMenuContents.push(makeMenuItemLink('data-profile', PATH_RUN + '/' + currentRun + PATH_DATA_PROFILE, 'Data profile', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItemLink('data-resource', PATH_RUN + '/' + currentRun + PATH_DATA_RESOURCE, 'Data resource', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItemLink('run-environment', PATH_RUN + '/' + currentRun + PATH_RUN_ENVIRONMENT, 'Run environment', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItemLink('run-metadata', PATH_RUN + '/' + currentRun + PATH_RUN_METADATA, 'Run metadata', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItemLink('short-report', PATH_RUN + '/' + currentRun + PATH_SHORT_REPORT, 'Short report', <ShortTextIcon />));
    runSubMenuContents.push(makeMenuItemLink('short-schema', PATH_RUN + '/' + currentRun + PATH_SHORT_SCHEMA, 'Short schema', <ShortTextIcon />));
    
    return (
        <div style={{ "paddingLeft": LEFT_PADDING }} key='run-sub-menu' >
            { runSubMenuContents }
        </div>
    );
}

const InRunComparison = () => {
    return useLocation().pathname.indexOf(PATH_RUN_COMPARISON) > -1;
}

export default CustomMenu;