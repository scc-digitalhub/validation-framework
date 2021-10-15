import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Title, TopToolbar, Datagrid, TextField } from 'react-admin';
import { useQuery, Loading, Error, ListContextProvider } from 'react-admin'

import Card from '@material-ui/core/Card';

import { BackButton } from '../fields/back-button';
import { PATH_RUN, PATH_ARTIFACT_METADATA, RESOURCE_ARTIFACT_METADATA } from '../utils/common-constants';
import { CheckProjectAndExperiment } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <BackButton key='back-button' resource={RESOURCE_ARTIFACT_METADATA} />
        </TopToolbar>
    );
}

export const ArtifactMetadataList = (props) => {
    CheckProjectAndExperiment();
    
    const { data, loading, error } = useQuery({
        type: 'getList',
        resource: RESOURCE_ARTIFACT_METADATA,
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
    
    const basePath = PATH_RUN + '/' + props.match.params.runId + PATH_ARTIFACT_METADATA;
    
    return (
        <React.Fragment>
            <Title title="Artifact metadata" />
            {ListActions()}
            <Card>
                <ListContextProvider value={{
                        data: keyBy(data, 'id'),
                        ids: data.map(({ id }) => id),
                        page: 1,
                        perPage: 50,
                        currentSort: { field: 'name', order: 'ASC' },
                        basePath: basePath,
                        resource: { RESOURCE_ARTIFACT_METADATA }
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