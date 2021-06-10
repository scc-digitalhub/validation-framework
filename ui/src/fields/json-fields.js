import * as React from 'react';

import get from 'lodash/get';

const spanClass = 'MuiTypography-root MuiTypography-body2';

const CONTENTS_REGEX = /^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*$/;

const printDict = (printContainer, dict, indent='') => {
    for (const [key, value] of Object.entries(dict)) {
        if (typeof(value) !== 'object') {
            printContainer.push(<span class={spanClass} style={{"white-space": "pre"}}>{indent}{key}: {value}</span>);
            printContainer.push(<br/>);
        } else {
            printContainer.push(<span class={spanClass} style={{"white-space": "pre"}}>{indent}{key}:</span>);
            printContainer.push(<br/>);
            printDict(printContainer, value, indent + '  ');
        }
    }
}

export const JsonField = ({
    record,
    ...props
}) => {
    let spans = [];
    if (CONTENTS_REGEX.test(props.source)) {
        const dictToPrint = get(record, props.source);
        printDict(spans, dictToPrint);
    }
    return spans;
};

export const JsonArrayField = ({
    record,
    ...props
}) => {
    let content = [];
    if (CONTENTS_REGEX.test(props.source)) {
        const arrayToPrint = get(record, props.source);
        arrayToPrint.forEach(item => {
            printDict(content, item);
            content.push(<br/>);
        });
        content.pop();
    }
    return content
}
