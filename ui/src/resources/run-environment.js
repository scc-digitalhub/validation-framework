import * as React from 'react';

import { TextField, FunctionField } from 'react-admin';
import { useQuery, Loading, Error } from 'react-admin';
import { TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, formatBytes } from '../utils/common-functions';

export const RunEnvironmentDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'run-environment';
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            id: props.match.params.run_id
        }
    });
    
    if (loading) return <Loading />;
    if (error) return <Error error={error} />;
    if (!data) return null;
    
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
                        <TextField source="contents.platform" label="Platform" />
                        <TextField source="contents.python_version" label="Python version" />
                        <TextField source="contents.cpu_core" label="Number of CPU cores" />
                        <FunctionField label="RAM" render={data => formatBytes(data.contents.ram)} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}