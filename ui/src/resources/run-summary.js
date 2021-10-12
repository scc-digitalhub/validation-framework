import * as React from 'react';

import { List, Datagrid, TextField, DateField, FunctionField } from 'react-admin';
import { useQuery, Loading, BulkDeleteButton } from 'react-admin';
import { Title, Toolbar, TopToolbar, MenuItemLink, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import ShortTextIcon from '@material-ui/icons/ShortText';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';
import { CompareRecentButton } from '../fields/compare-recent-button';
import { CompareButton } from '../fields/compare-button';

import { CheckProjectAndExperiment, calculateDuration, missingDocumentError } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <CompareRecentButton key='compare-recent-button' />
            <BackButton key='back-button' resource='run' />
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
    
    const resource = 'run';
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            id: props.match.params.runId
        }
    });

    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(resource);
    
    if (!data.shortReport) {
        data.shortReport = {};
        data.shortReport.contents = {};
        data.shortReport.contents.errors = {};
    }
    
    return (
        <React.Fragment>
            <Title title={data.runId} />
            <TopToolbar>
                <BackButton resource={resource} clear={true} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={resource}>
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
                    <MenuItemLink
                        key='artifact-metadata'
                        to={`/run/${data.runId}/artifact-metadata`}
                        primaryText='ArtifactMetadata'
                        leftIcon={<ListIcon />}
                    />
                    <MenuItemLink
                        key='data-profile'
                        to={`/run/${data.runId}/data-profile`}
                        primaryText='Data profile'
                        leftIcon={<ShortTextIcon />}
                    />
                    <MenuItemLink
                        key='data-resource'
                        to={`/run/${data.runId}/data-resource`}
                        primaryText='Data resource'
                        leftIcon={<ShortTextIcon />}
                    />
                    <MenuItemLink
                        key='run-environment'
                        to={`/run/${data.runId}/run-environment`}
                        primaryText='Run environment'
                        leftIcon={<ShortTextIcon />}
                    />
                    <MenuItemLink
                        key='run-metadata'
                        to={`/run/${data.runId}/run-metadata`}
                        primaryText='Run metadata'
                        leftIcon={<ShortTextIcon />}
                    />
                    <MenuItemLink
                        key='short-report'
                        to={`/run/${data.runId}/short-report`}
                        primaryText='Short report'
                        leftIcon={<ShortTextIcon />}
                    />
                    <MenuItemLink
                        key='short-schema'
                        to={`/run/${data.runId}/short-schema`}
                        primaryText='Short schema'
                        leftIcon={<ShortTextIcon />}
                    />
                </Toolbar>
            </Card>
        </React.Fragment>
    );
}