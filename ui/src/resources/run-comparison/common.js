import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';

import { createBaseEntry } from '../../utils/common-functions';

export const contentsLabel = "contents";

export const prepareColumns = (runs) => {
    let columns = [
        <TextField source="label" key="" label="" />
    ];
    
    for (let run of runs)
        columns.push(<TextField source={run.runId} key={run.runId} label={run.runId} />);
    
    return columns;
}

export const addRawData = (sectionData, sectionLabel, rawFieldNames, runs) => {
    for (let fieldName of rawFieldNames) {
        let entry = createBaseEntry(sectionData.length, fieldName);
        
        for (let run of runs) {
            if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
                let contents = run[sectionLabel][contentsLabel];
                entry[run.runId] = contents[entry["label"]];
            }
        }
        
        sectionData.push(entry);
    }
}

export const generateComparisonSection = (columns, data) => {
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