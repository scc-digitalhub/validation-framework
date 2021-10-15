import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, NumberField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { Title, TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { BackButton } from '../fields/back-button';
import { RESOURCE_DATA_PROFILE } from '../utils/common-constants';
import { CheckProjectAndExperiment, displayAsPercentage, formatBytes, formatDuration, createBaseEntry, missingDocumentError } from '../utils/common-functions';

const getListOfMeasurementFields = (stats) => {
    let results = [];
    if (!stats)
        return results;
    
    results.push(createBaseEntry(0, 'Number of records', stats.n));
    results.push(createBaseEntry(1, 'Number of columns', stats.n_var));
    results.push(createBaseEntry(2, 'Size', formatBytes(stats.memory_size)));
    results.push(createBaseEntry(3, 'Size of a single record', formatBytes(stats.record_size)));
    results.push(createBaseEntry(4, 'Cells with no value', stats.n_cells_missing));
    results.push(createBaseEntry(5, 'Cells with no value (%)', displayAsPercentage(stats.p_cells_missing)));
    results.push(createBaseEntry(6, 'Columns with missing values', stats.n_vars_with_missing));
    results.push(createBaseEntry(7, 'Empty columns', stats.n_vars_all_missing));
    results.push(createBaseEntry(8, 'Duplicate records', stats.n_duplicates));
    results.push(createBaseEntry(9, 'Duplicate records (%)', displayAsPercentage(stats.p_duplicates)));
    
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
        listOfTypes.push(createBaseEntry(i, t, types[t]));
        i++;
    }
    
    return (
        <Card style={{ "display": "inline-block", "marginLeft": "20px" }}>
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
            <Card key={f}>
                <CardContent>
                    <Typography className='MuiFormLabel-root' >
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
    
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: RESOURCE_DATA_PROFILE,
        payload: {
            id: props.match.params.runId
        }
    });
    
    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(RESOURCE_DATA_PROFILE);
    
    if (!data.contents)
        data.contents = {};
    
    return (
        <React.Fragment>
            <Title title="Data profile" />
            <TopToolbar>
                <BackButton resource={RESOURCE_DATA_PROFILE} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={RESOURCE_DATA_PROFILE}>
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