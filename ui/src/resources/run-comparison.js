import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { useQuery, Loading } from 'react-admin';
import { Datagrid, TextField, FunctionField } from 'react-admin';
import { TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { BackButton } from '../fields/back-button';
import { genericError, calculateDuration, formatDuration } from '../utils/common-functions';

const validationLabel = "shortReport";
const executionLabel = "runMetadata";
const profileLabel = "dataProfile";
const contentsLabel = "contents";

const rawFieldNames = {
    [validationLabel]: ["valid", "validationLibraryName", "validationLibraryVersion"],
    [executionLabel]: ["created", "started", "finished",],
    [profileLabel]: [
        "profilingLibraryName", "profilingLibraryVersion"
    ]
}

const validationComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addRawValidationData(sectionData, data.runs);
    addDerivedValidationData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const executionComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addDerivedExecutionData(sectionData, data.runs);
    addRawExecutionData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const profileComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addDerivedProfileData(sectionData, data.runs);
    addRawProfileData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const prepareColumns = (runs) => {
    let columns = [
        <TextField source="label" key="" label="" />
    ];
    
    for (let run of runs)
        columns.push(<TextField source={run.runId} key={run.runId} label={run.runId} />);
    
    return columns;
}

const createBaseEntry = (index, label) => {
    return {
        "index": index,
        "label": label
    }
}

const addDerivedValidationData = (data, runs) => {
    let sectionLabel = validationLabel;
    
    let nErrorsEntry = createBaseEntry(data.length, "n of errors");
    let durationEntry = createBaseEntry(data.length+1, "duration");
    
    for (let run of runs) {
        if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
            let contents = run[sectionLabel][contentsLabel];
            nErrorsEntry[run.runId] = contents["errors"].length;
            durationEntry[run.runId] = formatDuration(contents["duration"]*1000)
        }
    }
    
    data.push(nErrorsEntry);
    data.push(durationEntry);
}

const addRawValidationData = (data, runs) => {
    addRawData(data, validationLabel, runs);
}

const addDerivedExecutionData = (data, runs) => {
    let sectionLabel = executionLabel;
    
    let statusEntry = createBaseEntry(data.length, "status");
    let durationEntry = createBaseEntry(data.length+1, "duration");
    
    for (let run of runs) {
        if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
            let contents = run[sectionLabel][contentsLabel];
            statusEntry[run.runId] = contents["endStatus"];
            durationEntry[run.runId] = calculateDuration(contents["created"], contents["finished"]);
        }
    }
    
    data.push(statusEntry);
    data.push(durationEntry);
}

const addRawExecutionData = (data, runs) => {
    addRawData(data, executionLabel, runs);
}

const addRawProfileData = (data, runs) => {
    addRawData(data, profileLabel, runs);
}

const addDerivedProfileData = (data, runs) => {
    let sectionLabel = profileLabel;
    
    let durationEntry = createBaseEntry(data.length, "duration");
    let nRecordsEntry = createBaseEntry(data.length+1, "n of records");
    let nColumnsEntry = createBaseEntry(data.length+2, "n of columns");
    let memorySizeEntry = createBaseEntry(data.length+3, "size");
    let cellsWithNoValueEntry = createBaseEntry(data.length+4, "cells with no value");
    let columnsWithMissingValuesEntry = createBaseEntry(data.length+5, "columns with missing values");
    let emptyColumnsEntry = createBaseEntry(data.length+6, "empty columns");
    let duplicateRowsEntry = createBaseEntry(data.length+7, "duplicate rows");
    
    for (let run of runs) {
        if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
            let contents = run[sectionLabel][contentsLabel];
            durationEntry[run.runId] = formatDuration(contents["duration"]*1000);
            nRecordsEntry[run.runId] = contents["stats"]["n"];
            nColumnsEntry[run.runId] = contents["stats"]["n_var"];
            memorySizeEntry[run.runId] = contents["stats"]["memory_size"];
            cellsWithNoValueEntry[run.runId] = contents["stats"]["n_cells_missing"];
            columnsWithMissingValuesEntry[run.runId] = contents["stats"]["n_vars_with_missing"];
            emptyColumnsEntry[run.runId] = contents["stats"]["n_vars_all_missing"];
            duplicateRowsEntry[run.runId] = contents["stats"]["n_duplicates"];
        }
    }
    
    data.push(durationEntry);
    data.push(nRecordsEntry);
    data.push(nColumnsEntry);
    data.push(memorySizeEntry);
    data.push(cellsWithNoValueEntry);
    data.push(columnsWithMissingValuesEntry);
    data.push(emptyColumnsEntry);
    data.push(duplicateRowsEntry);
}

const addRawData = (data, section, runs) => {
    for (let fieldName of rawFieldNames[section]) {
        let entry = createBaseEntry(data.length, fieldName);
        
        for (let run of runs) {
            if (run[section] && run[section][contentsLabel]) {
                let contents = run[section][contentsLabel];
                entry[run.runId] = contents[entry["label"]];
            }
        }
        
        data.push(entry);
    }
}

const generateComparisonSection = (columns, data) => {
    return(
        <React.Fragment>
            <Card>
                <ListContextProvider value={{
                        data: keyBy(data, 'index'),
                        ids: data.map(({ index }) => index),
                        page: 1,
                        perPage: 50,
                        currentSort: { field: 'index', order: 'ASC' }
                }}>
                    <Datagrid>
                        {columns}
                    </Datagrid>
                </ListContextProvider>
            </Card>
        </React.Fragment>
    );
}

export const RunComparisonDetail = props => {
    const resource = 'run-comparison';
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            ids: props.match.params.selectedIds
        }
    });
    
    if (loading)
        return <Loading />;
    if (error || !data || !data.runs)
        return genericError(resource, "Error while retrieving comparison.");
    
    return (
        <React.Fragment>
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={resource}>
                        <FunctionField label="Results of validation" render={validationComparison} />
                        <FunctionField label="Execution information" render={executionComparison} />
                        <FunctionField label="Data profile" render={profileComparison} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}