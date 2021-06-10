import * as React from 'react';

import { List, Datagrid, TextField, DateField, FunctionField } from 'react-admin';
import { useQuery, Loading, Error } from 'react-admin';
import { Title, Toolbar, TopToolbar, ExportButton, MenuItemLink, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import ShortTextIcon from '@material-ui/icons/ShortText';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';

import { CheckProjectAndExperiment, formatDuration } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <ExportButton key='export-button' />
            <BackButton key='back-button' resource='run' />
        </TopToolbar>
    );
}

const getStatus = (data) => {
    if (data.contents.end_status)
        return data.contents.end_status;
    return data.contents.begin_status;
}

const getDuration = (data) => {
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
                <TextField source="run_id" label="Run ID"/>
                <DateField source="created" showTime={true} />
                <TextField source="contents.end_status" label="End status" />
                <TextField source="contents.validation_library" label="Validation library" />
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
            id: props.match.params.run_id
        }
    });

    if (loading) return <Loading />;
    if (error) return <Error />;
    if (!data) return null;
    
    return (
        <React.Fragment>
            <Title title={data.run_id} />
            <TopToolbar>
                <BackButton resource={resource} clear={true} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={resource}>
                            <FunctionField label="Run ID" render={data => <h1> {data.run_id} </h1>} />
                            <FunctionField label="Status" render={getStatus} />
                            <FunctionField label="Duration" render={getDuration} />
                            <TextField source="contents.run_metadata_uri" label="Run metadata URI" />
                            <TextField source="contents.run_artifacts_uri" label="Run artifacts URI " />
                            <TextField source="contents.data_resource_uri" label="Data resource URI" />
                            <TextField source="contents.validation_library_name" label="Validation library" />
                            <TextField source="contents.validation_library_version" label="Validation library version" />
                            <TextField source="contents.profiling_library_name" label="Profiling library version" />
                            <TextField source="contents.profiling_library_version" label="Profiling library version" />
                            <TextField source="contents.created" label="created" />
                            <TextField source="contents.begin_status" label="begin_status" />
                            <TextField source="contents.started" label="started" />
                            <TextField source="contents.end_status" label="end_status" />
                            <TextField source="contents.finished" label="finished" />
                            <TextField source="id" label="Document ID" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    <MenuItemLink
                        key='artifact-metadata'
                        to={`/run/${data.run_id}/artifact-metadata`}
                        primaryText='ArtifactMetadata'
                        leftIcon={<ListIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='data-profile'
                        to={`/run/${data.run_id}/data-profile`}
                        primaryText='Data profile'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='data-resource'
                        to={`/run/${data.run_id}/data-resource`}
                        primaryText='Data resource'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='run-environment'
                        to={`/run/${data.run_id}/run-environment`}
                        primaryText='Run environment'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='short-report'
                        to={`/run/${data.run_id}/short-report`}
                        primaryText='Short report'
                        leftIcon={<ShortTextIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                    <MenuItemLink
                        key='short-report'
                        to={`/run/${data.run_id}/short-schema`}
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