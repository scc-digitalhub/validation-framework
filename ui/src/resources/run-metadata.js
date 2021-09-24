import * as React from 'react';

import { List, Datagrid, TextField, DateField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { Title, Toolbar, TopToolbar, MenuItemLink, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import ShortTextIcon from '@material-ui/icons/ShortText';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';

import { CheckProjectAndExperiment, formatDuration, missingDocumentError } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <BackButton key='back-button' resource='run' />
        </TopToolbar>
    );
}

const getStatus = (data) => {
    if (data.contents.endStatus)
        return data.contents.endStatus;
    return data.contents.beginStatus;
}

const getDuration = (data) => {
    if (!data.contents.created)
        return null;
    
    const created = new Date(data.contents.created);
    
    let upTo = null;
    if (data.contents.finished)
        upTo = new Date(data.contents.finished);
    else
        upTo = Date.now();
    
    return formatDuration(upTo - created);
}

export const RunMetadataList = (props) => {
    if (!CheckProjectAndExperiment())
        return null;
    
    return (
        <List {...props} perPage={50} pagination={false} actions={<ListActions />}>
            <Datagrid rowClick="">
                <TextField source="runId" label="Run ID"/>
                <DateField source="created" showTime={true} />
                <TextField source="contents.endStatus" label="End status" />
                <TextField source="contents.validationLibraryName" label="Validation library" />
                <SelectButton />
            </Datagrid>
        </List>
    );
}

export const RunMetadataOverview = props => {
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
    
    if (!data.contents)
        data.contents = {};
    
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
                            <FunctionField label="Run ID" render={data => <h1> {data.runId} </h1>} />
                            <FunctionField label="Status" render={getStatus} />
                            <FunctionField label="Duration" render={getDuration} />
                            <TextField source="contents.runMetadataUri" label="Run metadata URI" />
                            <TextField source="contents.runArtifactsUri" label="Run artifacts URI " />
                            <TextField source="contents.dataResourceUri" label="Data resource URI" />
                            <TextField source="contents.validationLibraryName" label="Validation library" />
                            <TextField source="contents.validationLibraryVersion" label="Validation library version" />
                            <TextField source="contents.profilingLibraryName" label="Profiling library version" />
                            <TextField source="contents.profilingLibraryVersion" label="Profiling library version" />
                            <TextField source="contents.created" label="created" />
                            <TextField source="contents.beginStatus" label="beginStatus" />
                            <TextField source="contents.started" label="started" />
                            <TextField source="contents.endStatus" label="endStatus" />
                            <TextField source="contents.finished" label="finished" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    <MenuItemLink
                        key='artifact-metadata'
                        to={`/run/${data.runId}/artifact-metadata`}
                        primaryText='ArtifactMetadata'
                        leftIcon={<ListIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='data-profile'
                        to={`/run/${data.runId}/data-profile`}
                        primaryText='Data profile'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='data-resource'
                        to={`/run/${data.runId}/data-resource`}
                        primaryText='Data resource'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='run-environment'
                        to={`/run/${data.runId}/run-environment`}
                        primaryText='Run environment'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='short-report'
                        to={`/run/${data.runId}/short-report`}
                        primaryText='Short report'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='short-report'
                        to={`/run/${data.runId}/short-schema`}
                        primaryText='Short schema'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                </Toolbar>
            </Card>
        </React.Fragment>
    );
}