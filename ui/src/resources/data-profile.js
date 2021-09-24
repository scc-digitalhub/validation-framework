import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, NumberField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { BackButton } from '../fields/back-button';
import { CheckProjectAndExperiment, displayAsPercentage, formatBytes, formatDuration, makeFieldObject, missingDocumentError } from '../utils/common-functions';

const getListOfMeasurementFields = (stats) => {
    let results = [];
    if (!stats)
        return results;
    
    results.push(makeFieldObject(0, 'Number of records', stats.n));
    results.push(makeFieldObject(1, 'Number of columns', stats.n_var));
    results.push(makeFieldObject(2, 'Size', formatBytes(stats.memory_size)));
    results.push(makeFieldObject(3, 'Size of a single record', formatBytes(stats.record_size)));
    results.push(makeFieldObject(4, 'Missing cells', stats.n_cells_missing));
    results.push(makeFieldObject(5, 'Missing cells (%)', displayAsPercentage(stats.p_cells_missing)));
    results.push(makeFieldObject(6, 'Columns with missing values', stats.n_vars_with_missing));
    results.push(makeFieldObject(7, 'Empty columns', stats.n_vars_all_missing));
    results.push(makeFieldObject(8, 'Duplicate records', stats.n_duplicates));
    results.push(makeFieldObject(9, 'Duplicate records (%)', displayAsPercentage(stats.p_duplicates)));
    
    return results;
}

const measurements = (data) => {
    if (!data.contents.stats)
        return null;
    
    const listOfMeasurementFields = getListOfMeasurementFields(data.contents.stats);
    
    return (
        <Card style={{ "float": "left" }}>
            <ListContextProvider value={{
                    data: keyBy(listOfMeasurementFields, 'index'),
                    ids: listOfMeasurementFields.map(({ index }) => index),
                    page: 1,
                    perPage: 50,
                    currentSort: { field: 'index', order: 'ASC' }
            }}>
                <Datagrid>
                    <TextField source="label" label="Measure" />
                    <TextField source="value" label="Value" />
                </Datagrid>
            </ListContextProvider>
        </Card>
    );
}

const columnTypeCounts = (data) => {
    if (!data.contents.stats || !data.contents.stats.types)
        return null;
    
    const types = data.contents.stats.types;
    if (!types)
        return null;
    
    let listOfTypes = [];
    let i = 0;
    for (let t in types) {
        listOfTypes.push(makeFieldObject(i, t, types[t]));
        i++;
    }
    
    return (
        <Card style={{ "display": "inline-block", "margin-left": "20px" }}>
            <ListContextProvider value={{
                    data: keyBy(listOfTypes, 'index'),
                    ids: listOfTypes.map(({ index }) => index),
                    page: 1,
                    perPage: 50,
                    currentSort: { field: 'index', order: 'ASC' }
            }}>
                <Datagrid>
                    <TextField source="label" label="Column type" />
                    <NumberField source="value" label="Count" />
                </Datagrid>
            </ListContextProvider>
        </Card>
    );
}

const fullStatistics = (data) => {
    return(
        <React.Fragment>
            {measurements(data)}
            {columnTypeCounts(data)}
        </React.Fragment>
    );
}

const fieldStatistics = (data) => {
    const fields = data.contents.fields;
    if (!fields)
        return null;
    
    let variableCards = [];
    for (let f in fields) {
        variableCards.push(
            <Card>
                <CardContent>
                    <Typography class='MuiFormLabel-root' >
                        {f}
                    </Typography>
                    
                    <Card>
                    
                        <CardContent style={{ "float": "left" }} >
                            <SimpleShowLayout record={fields[f]} >
                                <TextField source="type" label="Type" />
                                <TextField source="is_unique" label="Unique" />
                                <TextField source="hashable" label="Hashable" />
                                <FunctionField label="Memory size" render={data => formatBytes(data.memory_size)} />
                            </SimpleShowLayout >
                        </CardContent>
                        
                        <CardContent style={{ "float": "left", "display": "inline-block" }} >
                            <SimpleShowLayout record={fields[f]} >
                                <TextField source="n_unique" label="Number of unique values" />
                                <TextField source="n_distinct" label="Number of distinct values" />
                                <TextField source="n" label="Number of records where column is present" />
                                <TextField source="count" label="Number of records where this value is not null" />
                                <TextField source="n_missing" label="Number of records where this value is null" />
                            </SimpleShowLayout >
                        </CardContent>
                        
                        <CardContent style={{ "display": "inline-block" }} >
                            <SimpleShowLayout record={fields[f]} >
                                <FunctionField label="Percentage of distinct values" render={data => displayAsPercentage(data.p_unique)} />
                                <FunctionField label="Percentage of unique values" render={data => displayAsPercentage(data.p_distinct)} />
                                <FunctionField label="Percentage of null values" render={data => displayAsPercentage(data.p_missing)} />
                            </SimpleShowLayout >
                        </CardContent>
                        
                    </Card>
                </CardContent>
            </Card>
        );
    }
    
    return (
        <Card>
            {variableCards}
        </Card>
    );
}

export const DataProfileDetail = props => {
    CheckProjectAndExperiment();
    
    const resource = 'data-profile';
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
                        <FunctionField label="Duration" render={data => formatDuration(data.contents.duration*1000)} />
                        <TextField source="contents.dataResourceUri" label="Data resource URI" />
                        <FunctionField label="Statistics" render={fullStatistics} />
                        <FunctionField label="Fields" render={fieldStatistics} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}