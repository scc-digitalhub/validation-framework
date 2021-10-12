import * as React from 'react';

import { TextField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';

import { CheckProjectAndExperiment, calculateDuration, missingDocumentError } from '../utils/common-functions';

const getStatus = (data) => {
    if (data.contents.endStatus)
        return data.contents.endStatus;
    return data.contents.beginStatus;
}

const getDuration = (data) => {
    return calculateDuration(data.contents.created, data.contents.finished);
}

export const RunMetadataDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'run-metadata';
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
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={resource}>
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
                </CardContent>
            </Card>
        </React.Fragment>
    );
}