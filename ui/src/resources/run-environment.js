import * as React from 'react';

import { TextField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { Title, TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, formatBytes, missingDocumentError } from '../utils/common-functions';

export const RunEnvironmentDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'run-environment';
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
            <Title title="Run environment" />
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={resource}>
                        <TextField source="contents.platform" label="Platform" />
                        <TextField source="contents.pythonVersion" label="Python version" />
                        <TextField source="contents.cpuModel" label="CPU model" />
                        <TextField source="contents.cpuCore" label="Number of CPU cores" />
                        <FunctionField label="RAM" render={data => formatBytes(data.contents.ram)} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}