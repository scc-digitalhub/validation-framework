import { contentsLabel, prepareColumns, addRawData, createBaseEntry, generateComparisonSection } from './common';

import { formatDuration } from '../../utils/common-functions';

const sectionLabel = "shortReport";
const rawFieldNames = ["valid", "validationLibraryName", "validationLibraryVersion"];

const validationComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addRawValidationData(sectionData, data.runs);
    addDerivedValidationData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const addRawValidationData = (sectionData, runs) => {
    addRawData(sectionData, sectionLabel, rawFieldNames, runs);
}

const addDerivedValidationData = (sectionData, runs) => {
    let nErrorsEntry = createBaseEntry(sectionData.length, "n of errors");
    let durationEntry = createBaseEntry(sectionData.length+1, "duration");
    
    for (let run of runs) {
        if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
            let contents = run[sectionLabel][contentsLabel];
            nErrorsEntry[run.runId] = contents["errors"].length;
            durationEntry[run.runId] = formatDuration(contents["duration"]*1000)
        }
    }
    
    sectionData.push(nErrorsEntry);
    sectionData.push(durationEntry);
}

export default validationComparison;