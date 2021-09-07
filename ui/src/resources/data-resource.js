import * as React from 'react';

import { TextField, FunctionField } from 'react-admin';
import { useQuery, Loading, Error } from 'react-admin';
import { TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, formatBytes } from '../utils/common-functions';

export const DataResourceDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'data-resource';
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            id: props.match.params.runId
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
                        <TextField source="contents.path" label="Path" />
                        <TextField source="contents.name" label="Name" />
                        <TextField source="contents.profile" label="Profile" />
                        <TextField source="contents.format" label="Format" />
                        <TextField source="contents.mediatype" label="Media type" />
                        <TextField source="contents.encoding" label="Encoding" />
                        <FunctionField label="Size" render={data => formatBytes(data.contents.bytes)} />
                        <TextField source="contents.hash" label="Hash" />
                        <TextField source="contents.schema" label="Schema" />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}