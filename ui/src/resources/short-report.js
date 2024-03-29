import * as React from 'react';

import keyBy from 'lodash/keyBy'

import { Datagrid, TextField, NumberField, FunctionField } from 'react-admin';
import { useQuery, Loading } from 'react-admin';
import { Title, TopToolbar, SimpleShowLayout, ListContextProvider } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { BackButton } from '../fields/back-button';
import { RESOURCE_SHORT_REPORT } from '../utils/common-constants';
import { CheckProjectAndExperiment, formatDuration, createBaseEntry, normalizeSeverity, missingDocumentError } from '../utils/common-functions';

import { ToggleWithLabels } from '../components/toggle-with-labels';
import { SeverityIndicator } from '../components/severity_indicator';

const errorStatisticsRender = (data) => {
    if (!data.contents.errors || data.contents.errors.length === 0)
        return "No errors to compute statistics for.";
    
    let errorSeverityCounters = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    };
    
    data.contents.errors.forEach (e => {
        errorSeverityCounters[normalizeSeverity(e['severity'])]++;
    });
    
    let severityList = [];
    for (let e in errorSeverityCounters)
        severityList.push(createBaseEntry(e-1, e, errorSeverityCounters[e]));
    
    return (
        <Card>
            <ListContextProvider value={{
                    data: keyBy(severityList, 'index'),
                    ids: severityList.map(({ index }) => index),
                    page: 1,
                    perPage: 50,
                    currentSort: { field: 'index', order: 'ASC' }
            }}>
                <Datagrid>
                    <TextField source="label" label="Severity level" />
                    <TextField source="value" label="Count" />
                </Datagrid>
            </ListContextProvider>
        </Card>
    );
}

const errorsRenderByCode = (data) => {
    if (!data.contents.errors)
        return null;
    
    let errorDict = {};
    
    data.contents.errors.forEach (e => {
        if (e['code'] in errorDict) {
            e['index'] = errorDict[e['code']].count;
            errorDict[e['code']].count++;
            errorDict[e['code']].items.push(e);
        } else {
            e['index'] = 0;
            errorDict[e['code']] = {
                count: 1,
                items: [e]
            }
        }
    });
    
    let errorLists = [];
    for (let e in errorDict) {
        errorLists.push(
            <Card key={e}>
                <CardContent>
                    <Typography className='MuiFormLabel-root' >
                        {e}
                    </Typography>
                    
                    <Card>
                        <CardContent>
                            <ListContextProvider value={{
                                    data: keyBy(errorDict[e].items, 'index'),
                                    ids: errorDict[e].items.map(({ index }) => index),
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
    
    return (errorLists);
};

const errorsRenderBySeverity = (data) => {
    const severityColors = ["ffff11", "ffdd22", "ffcc00", "ff8800", "ff0000"];
    
    if (!data.contents.errors)
        return null;
    
    let errorDict = {};
    
    data.contents.errors.forEach (e => {
        let severity = normalizeSeverity(e['severity']);
        if (severity in errorDict) {
            e['index'] = errorDict[severity].count;
            errorDict[severity].count++;
            errorDict[severity].items.push(e);
        } else {
            e['index'] = 0;
            errorDict[severity] = {
                count: 1,
                items: [e]
            }
        }
    });
    
    let errorLists = [];
    
    let i = 5;
    while (i > 0) {
        if (i in errorDict) {
            errorLists.push(
                <Card key={i} style={{ "marginBottom": "20px", "border": i + "px solid #" + severityColors[i-1] }}>
                    <CardContent>
                        <Typography className='MuiFormLabel-root' style={{"float": "left"}}>
                            Severity: {i}
                        </Typography>
                        <SeverityIndicator level={i} color={severityColors[i-1]}/>
                        
                        <Card>
                            <CardContent>
                                <ListContextProvider value={{
                                        data: keyBy(errorDict[i].items, 'index'),
                                        ids: errorDict[i].items.map(({ index }) => index),
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
        
        i--;
    }
    
    return (errorLists);
}

const swapErrorsDisplay = () => {
    let divBySeverity = document.getElementById("by_severity");
    let divByCode = document.getElementById("by_code");
    
    if (divBySeverity && divByCode) {
        let display = divBySeverity.style.display;
        divBySeverity.style.display = divByCode.style.display;
        divByCode.style.display = display;
    }
}

const errorsRender = (data) => {
    let bySeverity = (
        <Card id={"by_severity"} style={{ "display": "inline" }}>
            {errorsRenderBySeverity(data)}
        </Card>
    );
    let byCode = (
        <Card id={"by_code"} style={{ "display": "none" }}>
            {errorsRenderByCode(data)}
        </Card>
    );
    
    return (
        <React.Fragment>
            <ToggleWithLabels toggleName="groupErrorsBy" leftLabel="By severity" rightLabel="By type" handleToggle={swapErrorsDisplay} />
            <br/><br/>
            {bySeverity}
            {byCode}
        </React.Fragment>
    );
}

const determineLayoutBasedOnValid = (valid) => {
    let layoutContent = [];
    
    layoutContent.push(<TextField source="contents.valid" label="Valid" />);
    if (!valid) {
        layoutContent.push(<FunctionField label="Number of errors" render={data => data.contents.errors.length} />);
        layoutContent.push(<FunctionField label="Error statistics" render={errorStatisticsRender} />);
    }
    layoutContent.push(<TextField source="contents.dataResourceUri" label="Data resource URI" />);
    layoutContent.push(<FunctionField label="Duration" render={data => formatDuration(data.contents.duration*1000)} />);
    if (!valid)
        layoutContent.push(<FunctionField label="Errors" render={errorsRender} />);
    
    return layoutContent;
}

export const ShortReportDetail = props => {
    CheckProjectAndExperiment();
    
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: RESOURCE_SHORT_REPORT,
        payload: {
            id: props.match.params.runId
        }
    });
    
    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(RESOURCE_SHORT_REPORT);
    
    if (!data.contents)
        data.contents = {};
    
    const layoutContent = determineLayoutBasedOnValid(data.contents.valid);
    
    return (
        <React.Fragment>
            <Title title="Short report" />
            <TopToolbar>
                <BackButton resource={RESOURCE_SHORT_REPORT} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={RESOURCE_SHORT_REPORT}>
                        {layoutContent}
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}