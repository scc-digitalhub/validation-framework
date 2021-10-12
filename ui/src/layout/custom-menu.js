import * as React from 'react';

import { DashboardMenuItem, MenuItemLink } from 'react-admin';

import { GetCurrentRun } from '../utils/common-functions';

// import { useMediaQuery } from '@material-ui/core';
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

const LEFT_PADDING = "18px";

const CustomMenu = ({ onMenuClick, logout }) => {
    const currentProject = React.useContext(AppContext).getProject();
    const currentExperiment = React.useContext(AppContext).getExperiment();
    const currentRun = GetCurrentRun();
    
    const setProject = React.useContext(AppContext).setProject;
    const setExperiment = React.useContext(AppContext).setExperiment;
    
    const clearProject = () => {
        setProject(null);
        onMenuClick();
    }
    
    const clearExperiment = () => {
        setExperiment(null);
        onMenuClick();
    }
    
    let menuContent = [];
    
    menuContent.push(<DashboardMenuItem onClick={clearProject} key='dashboard' />)
    menuContent.push(<Divider key='project-list-divider' />);
    
    menuContent.push(<MenuItemLink
            key='projects'
            to={`/project`}
            primaryText='Projects'
            leftIcon={<WorkOutline />}
            onClick={clearProject}
        />
    );
    
    if (currentProject) {
        let projectSubMenuContents = [];
        
        projectSubMenuContents.push(
            <MenuItemLink
                key={'project-overview'}
                to={`/project/overview`}
                primaryText={currentProject}
                leftIcon={<WorkIcon />}
                onClick={clearExperiment}
            />
        );
        
        projectSubMenuContents.push(
            <MenuItemLink
                key={'experiments'}
                to={`/experiment`}
                primaryText='Experiments'
                leftIcon={<GroupWorkOutlinedIcon />}
                onClick={clearExperiment}
            />
        );
        
        if (currentExperiment) {
            let experimentSubMenuContents = [];
            
            experimentSubMenuContents.push(
                <MenuItemLink
                    key={'experiment-overview'}
                    to={`/experiment/overview`}
                    primaryText={currentExperiment}
                    leftIcon={<GroupWorkIcon />}
                    onClick={onMenuClick}
                />
            );
            
            experimentSubMenuContents.push(
                <MenuItemLink
                    key={'runs'}
                    to={`/run`}
                    primaryText='Runs'
                    leftIcon={<AccountTreeOutlinedIcon />}
                    onClick={onMenuClick}
                />
            );
            
            if (currentRun) {
                let runSubMenuContents = [];
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'run-overview'}
                        to={`/run/${currentRun}/overview`}
                        primaryText={currentRun}
                        leftIcon={<AccountTreeIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'artifact-metadata'}
                        to={`/run/${currentRun}/artifact-metadata`}
                        primaryText='Artifact metadata'
                        leftIcon={<ListIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'data-profile'}
                        to={`/run/${currentRun}/data-profile`}
                        primaryText='Data profile'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'data-resource'}
                        to={`/run/${currentRun}/data-resource`}
                        primaryText='Data resource'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'run-environment'}
                        to={`/run/${currentRun}/run-environment`}
                        primaryText='Run environment'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'run-metadata'}
                        to={`/run/${currentRun}/run-metadata`}
                        primaryText='Run metadata'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'short-report'}
                        to={`/run/${currentRun}/short-report`}
                        primaryText='Short report'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                runSubMenuContents.push(
                    <MenuItemLink
                        key={'short-schema'}
                        to={`/run/${currentRun}/short-schema`}
                        primaryText='Short schema'
                        leftIcon={<ShortTextIcon />}
                        onClick={onMenuClick}
                    />
                );
                
                const runSubMenu = (
                    <div style={{ "paddingLeft": LEFT_PADDING }} key='run-sub-menu' >
                        { runSubMenuContents }
                    </div>
                );
                
                experimentSubMenuContents.push(runSubMenu);
            } else if (inRunComparison()) {
                experimentSubMenuContents.push(<Divider key='run-comparison-divider' />);
                experimentSubMenuContents.push(
                    <MenuItemLink
                        key={'run-comparison'}
                        to={``}
                        primaryText='Run comparison'
                        leftIcon={<CompareArrowsIcon />}
                        disabled={true}
                    />
                );
            }
            
            const experimentSubMenu = (
                <div style={{ "paddingLeft": LEFT_PADDING }} key='experiment-sub-menu' >
                    { experimentSubMenuContents }
                </div>
            );
            
            projectSubMenuContents.push(experimentSubMenu);
        }
        
        const projectSubMenu = (
            <div style={{ "paddingLeft": LEFT_PADDING }} key='project-sub-menu' >
                { projectSubMenuContents }
            </div>
        );
        
        menuContent.push(projectSubMenu);
    }
    
    // const isXSmall = useMediaQuery(theme => theme.breakpoints.down('xs'));
    return (
        <React.Fragment>
            { menuContent }
        </React.Fragment>
    );
}

const inRunComparison = () => {
    return (""+window.location).indexOf("run-comparison") > -1;
}

export default CustomMenu;