import { contentsLabel, prepareColumns, addRawData, createBaseEntry, generateComparisonSection } from './common';

import { formatDuration } from '../../utils/common-functions';

const sectionLabel = "dataProfile";
const rawFieldNames = ["profilingLibraryName", "profilingLibraryVersion"];

const profileComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addDerivedProfileData(sectionData, data.runs);
    addRawProfileData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const addRawProfileData = (sectionData, runs) => {
    addRawData(sectionData, sectionLabel, rawFieldNames, runs);
}

const addDerivedProfileData = (sectionData, runs) => {
    let durationEntry = createBaseEntry(sectionData.length, "duration");
    let nRecordsEntry = createBaseEntry(sectionData.length+1, "n of records");
    let nColumnsEntry = createBaseEntry(sectionData.length+2, "n of columns");
    let memorySizeEntry = createBaseEntry(sectionData.length+3, "size");
    let cellsWithNoValueEntry = createBaseEntry(sectionData.length+4, "cells with no value");
    let columnsWithMissingValuesEntry = createBaseEntry(sectionData.length+5, "columns with missing values");
    let emptyColumnsEntry = createBaseEntry(sectionData.length+6, "empty columns");
    let duplicateRowsEntry = createBaseEntry(sectionData.length+7, "duplicate rows");
    
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
    
    sectionData.push(durationEntry);
    sectionData.push(nRecordsEntry);
    sectionData.push(nColumnsEntry);
    sectionData.push(memorySizeEntry);
    sectionData.push(cellsWithNoValueEntry);
    sectionData.push(columnsWithMissingValuesEntry);
    sectionData.push(emptyColumnsEntry);
    sectionData.push(duplicateRowsEntry);
}

export default profileComparison;