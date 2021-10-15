import * as React from 'react';

import { List, Datagrid, TextField, DateField, FunctionField } from 'react-admin';
import { useQuery, Loading, BulkDeleteButton } from 'react-admin';
import { Title, Toolbar, TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import ShortTextIcon from '@material-ui/icons/ShortText';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';
import { CompareRecentButton } from '../fields/compare-recent-button';
import { CompareButton } from '../fields/compare-button';

import { PATH_RUN, PATH_ARTIFACT_METADATA, PATH_DATA_PROFILE, PATH_DATA_RESOURCE, PATH_RUN_ENVIRONMENT,
 PATH_RUN_METADATA, PATH_SHORT_REPORT, PATH_SHORT_SCHEMA, RESOURCE_RUN} from '../utils/common-constants';
import { CheckProjectAndExperiment, calculateDuration, missingDocumentError, makeMenuItemLink } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <CompareRecentButton key='compare-recent-button' />
            <BackButton key='back-button' resource={RESOURCE_RUN} />
        </TopToolbar>
    );
}

const ListBulkActionButtons = props => (
    <React.Fragment>
        <CompareButton {...props} />
        <BulkDeleteButton {...props} />
    </React.Fragment>
);

const getStatus = (data) => {
    if (data.runMetadata.contents.endStatus)
        return data.runMetadata.contents.endStatus;
    return data.runMetadata.contents.beginStatus;
}

const getDuration = (data) => {
    return calculateDuration(data.runMetadata.contents.created, data.runMetadata.contents.finished);
}

export const RunSummaryList = (props) => {
    if (!CheckProjectAndExperiment())
        return null;
    
    return (
        <List {...props}
                perPage={50}
                pagination={false}
                sort={{ field: 'created', order: 'DESC' }}
                actions={<ListActions />}
                bulkActionButtons={<ListBulkActionButtons />}>
            <Datagrid rowClick="">
                <DateField source="created" label="Created" showTime={true} />
                <TextField source="shortReport.contents.valid" label="Valid" />
                <TextField source="runMetadata.contents.endStatus" label="End status" />
                <TextField source="runId" label="Run ID"/>
                <TextField source="runMetadata.contents.validationLibraryName" label="Validation library" />
                <SelectButton />
            </Datagrid>
        </List>
    );
}

export const RunSummaryOverview = props => {
    CheckProjectAndExperiment();
    
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: RESOURCE_RUN,
        payload: {
            id: props.match.params.runId
        }
    });

    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(RESOURCE_RUN);
    
    if (!data.shortReport) {
        data.shortReport = {};
        data.shortReport.contents = {};
        data.shortReport.contents.errors = {};
    }
    
    return (
        <React.Fragment>
            <Title title={data.runId} />
            <TopToolbar>
                <BackButton resource={RESOURCE_RUN} clear={true} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={RESOURCE_RUN}>
                            <FunctionField label="Status" render={getStatus} />
                            <TextField source="shortReport.contents.valid" label="Valid" />
                            <FunctionField label="Number of errors" render={data => data.shortReport.contents.errors.length} />
                            <TextField source="created" label="created" />
                            <FunctionField label="Duration" render={getDuration} />
                            <TextField source="runId" label="Run ID" />
                            <TextField source="runMetadata.contents.validationLibraryName" label="Validation library" />
                            <TextField source="runMetadata.contents.validationLibraryVersion" label="Validation library version" />
                            <TextField source="runMetadata.contents.profilingLibraryName" label="Profiling library version" />
                            <TextField source="runMetadata.contents.profilingLibraryVersion" label="Profiling library version" />
                            <TextField source="runMetadata.contents.started" label="started" />
                            <TextField source="runMetadata.contents.finished" label="finished" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    {makeMenuItemLink('artifact-metadata', PATH_RUN + `/${data.runId}` + PATH_ARTIFACT_METADATA, 'ArtifactMetadata', <ListIcon />)}
                    {makeMenuItemLink('data-profile', PATH_RUN + `/${data.runId}` + PATH_DATA_PROFILE, 'Data profile', <ShortTextIcon />)}
                    {makeMenuItemLink('data-resource', PATH_RUN + `/${data.runId}` + PATH_DATA_RESOURCE, 'Data resource', <ShortTextIcon />)}
                    {makeMenuItemLink('run-environment', PATH_RUN + `/${data.runId}` + PATH_RUN_ENVIRONMENT, 'Run environment', <ShortTextIcon />)}
                    {makeMenuItemLink('run-metadata', PATH_RUN + `/${data.runId}` + PATH_RUN_METADATA, 'Run metadata', <ShortTextIcon />)}
                    {makeMenuItemLink('short-report', PATH_RUN + `/${data.runId}` + PATH_SHORT_REPORT, 'Short report', <ShortTextIcon />)}
                    {makeMenuItemLink('short-schema', PATH_RUN + `/${data.runId}` + PATH_SHORT_SCHEMA, 'Short schema', <ShortTextIcon />)}
                </Toolbar>
            </Card>
        </React.Fragment>
    );
}