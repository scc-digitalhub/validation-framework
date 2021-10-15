import * as React from 'react';
import { Route } from 'react-router-dom';

import { Admin, Resource } from 'react-admin';

import Work from '@material-ui/icons/Work';

import { PATH_PROJECT, PATH_EXPERIMENT, PATH_RUN, PATH_RUN_COMPARISON, PATH_RUN_COMPARISON_RECENT,
 PATH_OVERVIEW, PATH_ARTIFACT_METADATA, PATH_DATA_PROFILE, PATH_DATA_RESOURCE, PATH_RUN_ENVIRONMENT,
 PATH_RUN_METADATA, PATH_SHORT_REPORT, PATH_SHORT_SCHEMA} from './utils/common-constants';
import customLayout from './layout/custom-layout';
import { AuthProvider } from './auth/auth-provider';
import { DataProvider } from './data-provider';
import dashboard from './dashboard';
import { ProjectList, ProjectCreate, ProjectEdit, ProjectOverview } from './resources/project';
import { ExperimentList, ExperimentOverview } from './resources/experiment';
import { RunSummaryList, RunSummaryOverview } from './resources/run-summary';
import { ArtifactMetadataList } from './resources/artifact-metadata';
import { DataProfileDetail } from './resources/data-profile';
import { DataResourceDetail } from './resources/data-resource';
import { RunEnvironmentDetail } from './resources/run-environment';
import { RunMetadataDetail } from './resources/run-metadata';
import { ShortReportDetail } from './resources/short-report';
import { ShortSchemaDetail } from './resources/short-schema';
import { RunComparisonDetail, RunComparisonRecentDetail } from './resources/run-comparison/comparison';
import { AppContext } from './contexts/app-context';

const customRoutes = [
    <Route exact path={PATH_PROJECT+PATH_OVERVIEW} component={ProjectOverview} />,
    <Route exact path={PATH_EXPERIMENT+PATH_OVERVIEW} component={ExperimentOverview} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_OVERVIEW} component={RunSummaryOverview} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_ARTIFACT_METADATA} component={ArtifactMetadataList} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_DATA_PROFILE} component={DataProfileDetail} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_DATA_RESOURCE} component={DataResourceDetail} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_RUN_ENVIRONMENT} component={RunEnvironmentDetail} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_RUN_METADATA} component={RunMetadataDetail} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_SHORT_REPORT} component={ShortReportDetail} />,
    <Route exact path={PATH_RUN+"/:runId"+PATH_SHORT_SCHEMA} component={ShortSchemaDetail} />,
    <Route exact path={PATH_RUN_COMPARISON+"/:requested"} component={RunComparisonDetail} />,
    <Route exact path={PATH_RUN_COMPARISON_RECENT} component={RunComparisonRecentDetail} />
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
                    layout = {customLayout}
                    dashboard = {dashboard}
                    customRoutes = {customRoutes}
                    authProvider = {AuthProvider}
                >
                    <Resource key='project' name='project' options={{ label: 'Projects' }} icon={Work} list={ProjectList} create={ProjectCreate} edit={ProjectEdit} />
                    <Resource key='experiment' name='experiment' options={{ label: 'Experiments' }} list={ExperimentList} />
                    <Resource key='run' name='run' options={{ label: 'Runs' }} list={RunSummaryList} />
                </Admin>
            </AppContext.Provider>
        );
    }
}