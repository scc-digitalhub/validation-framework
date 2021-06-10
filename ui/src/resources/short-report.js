import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, NumberField, FunctionField } from 'react-admin';
import { useQuery, Loading, Error } from 'react-admin';
import { TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, formatDuration } from '../utils/common-functions';

const errorsRender = (data) => {
    if (!data.contents.errors)
        return null;
    
    let errorCodeDict = {};
    
    data.contents.errors.forEach (e => {
        if (e['code'] in errorCodeDict) {
            e['index'] = errorCodeDict[e['code']].count;
            errorCodeDict[e['code']].count++;
            errorCodeDict[e['code']].items.push(e);
        } else {
            e['index'] = 0;
            errorCodeDict[e['code']] = {
                count: 1,
                items: [e]
            }
        }
    });
    
    let errorLists = [];
    for (let e in errorCodeDict) {
        errorLists.push(
            <Card>
                <CardContent>
                    <Typography class='MuiFormLabel-root' >
                        {e}
                    </Typography>
                    
                    <Card>
                        <CardContent>
                            <ListContextProvider value={{
                                    data: keyBy(errorCodeDict[e].items, 'index'),
                                    ids: errorCodeDict[e].items.map(({ index }) => index),
                                    page: 1,
                                    perPage: 50,
                                    currentSort: { field: 'index', order: 'ASC' }
                            }}>
                                <Datagrid>
                                    <NumberField label="Record number" source="rowNumber" />
                                    <TextField source="fieldName" />
                                    <FunctionField label="Description" render={data => `${data.note}: ${data.description}`} />
                                </Datagrid>
                            </ListContextProvider >
                        </CardContent>
                    </Card>
                </CardContent>
            </Card>
        );
    }
    
    return (
        <Card>
            {errorLists}
        </Card>
    );
};

export const ShortReportDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'short-report';
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
                        <TextField source="contents.valid" label="Valid" />
                        <FunctionField label="Number of errors" render={data => data.contents.errors.length} />
                        <TextField source="contents.data_resource_uri" label="Data resource URI" />
                        <FunctionField label="Duration" render={data => formatDuration(data.contents.duration)} />
                        <FunctionField label="Errors" render={errorsRender} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}