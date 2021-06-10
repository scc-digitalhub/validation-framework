import * as React from 'react';
import { Route } from 'react-router-dom';

import { Admin, Resource } from 'react-admin';

import Work from '@material-ui/icons/Work';

import customLayout from './layout/custom-layout';
import { DataProvider } from './data-provider';
import dashboard from './dashboard';
import { ProjectList, ProjectCreate, ProjectEdit, ProjectOverview } from './resources/project';
import { ExperimentList, ExperimentOverview } from './resources/experiment';
import { RunMetadataList, RunMetadataOverview } from './resources/run-metadata';
import { ArtifactMetadataList } from './resources/artifact-metadata';
import { DataProfileDetail } from './resources/data-profile';
import { DataResourceDetail } from './resources/data-resource';
import { RunEnvironmentDetail } from './resources/run-environment';
import { ShortReportDetail } from './resources/short-report';
import { ShortSchemaDetail } from './resources/short-schema';

import { AppContext } from './contexts/app-context';

import { authProvider } from './auth/auth-provider';
import { LoginPage } from './auth/login-page';

const customRoutes = [
    <Route exact path="/project/overview" component={ProjectOverview} />,
    <Route exact path="/experiment/overview" component={ExperimentOverview} />,
    <Route exact path="/run/:run_id/overview" component={RunMetadataOverview} />,
    <Route exact path="/run/:run_id/artifact-metadata" component={ArtifactMetadataList} />,
    <Route exact path="/run/:run_id/data-profile" component={DataProfileDetail} />,
    <Route exact path="/run/:run_id/data-resource" component={DataResourceDetail} />,
    <Route exact path="/run/:run_id/run-environment" component={RunEnvironmentDetail} />,
    <Route exact path="/run/:run_id/short-report" component={ShortReportDetail} />,
    <Route exact path="/run/:run_id/short-schema" component={ShortSchemaDetail} />
]

let currentProject = null;
let currentExperiment = null;

let getProject = () => {
    return currentProject;
};

let getExperiment = () => {
    return currentExperiment;
};

let setProject = (val) => {
    currentProject = val;
};

let setExperiment = (val) => {
    currentExperiment = val;
};

const context = {
    getProject: getProject,
    getExperiment: getExperiment,
    setProject: setProject,
    setExperiment: setExperiment
};

const getters = {
    getProject: getProject,
    getExperiment: getExperiment
};

const dp = new DataProvider(getters);
export default class App extends React.Component {
    render() {
        return (
            <AppContext.Provider value={context}>
                <Admin
                    dataProvider = {dp}
                    // authProvider = { authProvider }
                    // loginPage={ LoginPage }
                    layout = {customLayout}
                    dashboard = {dashboard}
                    customRoutes = {customRoutes}
                >
                    <Resource key="project" name="project" options={{ label: 'Projects' }} icon={Work} list={ProjectList} create={ProjectCreate} edit={ProjectEdit} />
                    <Resource key="experiment" name="experiment" options={{ label: 'Experiments' }} list={ExperimentList} />
                    <Resource key="run" name="run" options={{ label: 'Runs' }} list={RunMetadataList} />
                </Admin>
            </AppContext.Provider>
        );
    }
}