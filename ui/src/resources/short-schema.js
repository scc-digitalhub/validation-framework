import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, NumberField, FunctionField } from 'react-admin';
import { useQuery, Loading, Error } from 'react-admin';
import { TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, formatDuration } from '../utils/common-functions';

const renderSchema = (data) => {
    if (!data.contents.fields)
        return null;
    
    let i = 0;
    data.contents.fields.forEach(f => {
        f['index'] = i;
        i++;
    });
    
    return (
        <Card>
            <CardContent>
                <ListContextProvider value={{
                        data: keyBy(data.contents.fields, 'index'),
                        ids: data.contents.fields.map(({ index }) => index),
                        page: 1,
                        perPage: 50,
                        currentSort: { field: 'index', order: 'ASC' }
                }}>
                    <Datagrid>
                        <NumberField source="index" />
                        <TextField source="name" />
                        <TextField source="type" />
                    </Datagrid>
                </ListContextProvider >
            </CardContent>
        </Card>
    );
};

export const ShortSchemaDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'short-schema';
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
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={resource}>
                        <FunctionField label="Duration" render={data => formatDuration(data.contents.duration)} />
                        <TextField source="contents.data_resource_uri" label="Data resource URI" />
                        <FunctionField label="Schema" render={renderSchema} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}