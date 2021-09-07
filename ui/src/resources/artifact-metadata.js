import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { TopToolbar, Datagrid, TextField } from 'react-admin';
import { useQuery, Loading, Error, ListContextProvider } from 'react-admin'

import Card from '@material-ui/core/Card';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <BackButton key='back-button' resource='artifact-metadata' />
        </TopToolbar>
    );
}

export const ArtifactMetadataList = (props) => {
    CheckProjectAndExperiment();
    
    const resource = 'artifact-metadata';
    const { data, loading, error } = useQuery({
        type: 'getList',
        resource: resource,
        payload: {
            id: props.match.params.runId,
            pagination: {
                page: 1,
                perPage: 50
            },
            sort: {
                field: "name",
                order: "ASC"
            }
        }
    });

    if (loading) return <Loading />;
    if (error) return <Error error={error} />;
    if (!data) return null;
    
    const basePath = '/run/' + props.match.params.runId + '/artifact-metadata';
    
    return (
        <React.Fragment>
            {ListActions()}
            <Card>
                <ListContextProvider value={{
                        data: keyBy(data, 'id'),
                        ids: data.map(({ id }) => id),
                        page: 1,
                        perPage: 50,
                        currentSort: { field: 'name', order: 'ASC' },
                        basePath: { basePath },
                        resource: { resource }
                }}>
                    <Datagrid rowClick="" actions={<ListActions />}>
                        <TextField source="name" />
                        <TextField source="uri" label="URI" />
                    </Datagrid>
                </ListContextProvider >
            </Card>
        </React.Fragment>
    )
};