import { contentsLabel, prepareColumns, addRawData, generateComparisonSection } from './common';

import { calculateDuration, createBaseEntry } from '../../utils/common-functions';

const sectionLabel = "runMetadata";
const rawFieldNames = ["created", "started", "finished"];

const executionComparison = (data) => {
    const columns = prepareColumns(data.runs);
    
    let sectionData = [];
    addDerivedExecutionData(sectionData, data.runs);
    addRawExecutionData(sectionData, data.runs);
    
    return generateComparisonSection(columns, sectionData);
}

const addRawExecutionData = (sectionData, runs) => {
    addRawData(sectionData, sectionLabel, rawFieldNames, runs);
}

const addDerivedExecutionData = (sectionData, runs) => {
    let statusEntry = createBaseEntry(sectionData.length, "status");
    let durationEntry = createBaseEntry(sectionData.length+1, "duration");
    
    for (let run of runs) {
        if (run[sectionLabel] && run[sectionLabel][contentsLabel]) {
            let contents = run[sectionLabel][contentsLabel];
            statusEntry[run.runId] = contents["endStatus"];
            durationEntry[run.runId] = calculateDuration(contents["created"], contents["finished"]);
        }
    }
    
    sectionData.push(statusEntry);
    sectionData.push(durationEntry);
}

export default executionComparison;